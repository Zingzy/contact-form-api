from quart import Quart, request, jsonify
from quart_cors import cors
from quart_rate_limiter import RateLimiter, rate_limit
from datetime import timedelta
from utils import verify_hcaptcha, validate_email, send_webhook
from dotenv import load_dotenv
from logger_config import setup_logger
from config import config

# Initialize logger
logger = setup_logger()

load_dotenv(override=True)

app = Quart(__name__)
app: Quart = cors(app)
limiter = RateLimiter(app)

logger.info(
    "Application started",
    host=config.server["host"],
    port=config.server["port"],
    debug=config.server["debug"],
)


@app.route("/contact", methods=["POST"])
@rate_limit(config.ratelimit["day_limit"], period=timedelta(days=1))  # per day
@rate_limit(config.ratelimit["hour_limit"], period=timedelta(hours=1))  # per hour
@rate_limit(config.ratelimit["minute_limit"], period=timedelta(minutes=1))  # per minute
async def contact():
    ip_address: str | None = request.remote_addr
    logger.info("Received contact request", ip_address=ip_address)

    form = await request.form
    email: str | None = form.get("email")
    subject: str | None = form.get("subject")
    message: str | None = form.get("message")
    hcaptcha_token: str | None = form.get("h-captcha-response")

    if not email or not message or not subject:
        logger.warning(
            "Missing required fields",
            ip_address=ip_address,
            email=bool(email),
            subject=bool(subject),
            message=bool(message),
        )
        return jsonify({"error": "Email, Subject and message are required"}), 400

    if not validate_email(email):
        logger.warning("Invalid email format", ip_address=ip_address, email=email)
        return jsonify({"error": "Invalid email format"}), 400

    if not hcaptcha_token:
        logger.warning("Missing hCaptcha token", ip_address=ip_address)
        return jsonify({"error": "hCaptcha token is required"}), 400

    is_valid: bool = await verify_hcaptcha(hcaptcha_token)
    if not is_valid:
        logger.warning("hCaptcha verification failed", ip_address=ip_address)
        return jsonify({"error": "hCaptcha verification failed"}), 400

    try:
        await send_webhook(
            config.webhook_uri,
            email,
            subject,
            message,
        )
        logger.info("Successfully sent message", ip_address=ip_address, email=email)

    except Exception as e:
        logger.error("Error sending webhook", ip_address=ip_address, error=str(e))
        return jsonify({"error": "Error sending message"}), 500

    return jsonify({"message": "Message sent successfully"}), 200


@app.errorhandler(429)
async def ratelimit_handler(e):
    ip_address: str | None = request.remote_addr
    logger.warning("Rate limit exceeded", ip_address=ip_address, error=str(e))

    return (
        jsonify(
            {
                "error": "Rate limit exceeded",
            }
        ),
        429,
    )


@app.route("/health")
async def health():
    logger.debug("Health check request", ip_address=request.remote_addr)
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(
        host=config.server["host"],
        port=config.server["port"],
        debug=config.server["debug"],
    )
