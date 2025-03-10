import aiohttp
import os
import dotenv
from datetime import datetime, timezone
import re

dotenv.load_dotenv(override=True)

hcaptcha_secret: str = os.environ["HCAPTCHA_SECRET"]
EMAIL_REGEX: re.Pattern[str] = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)


def validate_email(email) -> bool:
    if not EMAIL_REGEX.match(email):
        return False
    return True


async def verify_hcaptcha(token) -> bool:
    hcaptcha_verify_url = "https://hcaptcha.com/siteverify"

    async with aiohttp.ClientSession() as session:
        async with session.post(
            hcaptcha_verify_url,
            data={
                "response": token,
                "secret": hcaptcha_secret,
            },
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data["success"]
            return False


async def send_webhook(url: str, email: str, subject: str, message: str) -> None:
    data = {
        "embeds": [
            {
                "title": subject,
                "description": message,
                "author": {
                    "name": email,
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status >= 400:
                raise Exception(f"Webhook request failed with status {response.status}")
