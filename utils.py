import requests
import os
import dotenv

dotenv.load_dotenv(override=True)

hcaptcha_secret = os.environ["HCAPTCHA_SECRET"]

def verify_hcaptcha(token):
    hcaptcha_verify_url = "https://hcaptcha.com/siteverify"

    response = requests.post(
        hcaptcha_verify_url,
        data={
            "response": token,
            "secret": hcaptcha_secret,
        },
    )

    if response.status_code == 200:
        data = response.json()
        return data["success"]
    else:
        return False
