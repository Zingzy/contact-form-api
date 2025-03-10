
# Contact Form API

A secure, rate-limited API for handling contact form submissions.

## Overview

This API receives contact form submissions, validates them, and forwards the content to a **Discord webhook**. It includes:

- Email validation
- hCaptcha integration for bot protection
- Rate limiting to prevent abuse
- Logging for monitoring and debugging

## Setup

### Prerequisites

- Python 3.10 or later
- Discord webhook URL
- hCaptcha secret key

## Deployment

This project is configured for deployment on Vercel using the [vercel.json](vercel.json) configuration.

**Click on the button below to deploy instantly**. After deploying, you can just copy the URL of the deployment and use it as the base URL for your contact form.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FZingzy%2Fcontact-form-api&env=WEBHOOK_URI,HCAPTCHA_SECRET)

### Installation

1. Clone this repository
2. Create a `.env` file based on `.env.example`:
    - `WEBHOOK_URI`: Your Discord webhook URI
    - `HCAPTCHA_SECRET`: Your hCaptcha secret key, obtained from the [hCaptcha dashboard](https://dashboard.hcaptcha.com/)
3. Install the dependencies:

    ```bash
    pip install uv
    uv venv
    uv pip install -r requirements.txt
    ```

### Configuration

The application is configured via `config.toml`. Key settings include:

- **Server**: host, port, debug mode
- **Rate limits**: requests per minute/hour/day
- **Logging**: levels, rotation, retention

## API Endpoints

### POST /contact

Accepts `form-data` submissions with the following parameters:
- `email`: Sender's email address
- `subject`: Message subject
- `message`: Message content
- `h-captcha-response`: hCaptcha token

Returns:
- `200`: Message sent successfully
- `400`: Missing/invalid fields or failed hCaptcha verification
- `429`: Rate limit exceeded
- `500`: Error sending webhook

## Development

Start the server locally:

```bash
pip install uv
uv venv
uv run main.py
```

---

<h6 align="center">
<img src="https://avatars.githubusercontent.com/u/90309290?v=4" height=30 title="zingzy Copyright">
<br>
© zingzy . 2025

All Rights Reserved</h6>

<p align="center">
	<a href="https://github.com/zingzy/contact-form-api/blob/master/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&logoColor=d9e0ee&colorA=363a4f&colorB=b7bdf8"/></a>
</p>
