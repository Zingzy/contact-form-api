
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

### Installation

1. Clone this repository
2. Create a `.env` file based on `.env.example`:
    - `WEBHOOK_URI`: Your Discord webhook URI
    - `HCAPTCHA_SECRET`: Your hCaptcha secret key, obtained from the [hCaptcha dashboard](https://dashboard.hcaptcha.com/)
3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

The application is configured via `config.toml`. Key settings include:

- Server: host, port, debug mode
- Rate limits: requests per minute/hour/day
- Logging: levels, rotation, retention

## API Endpoints

### POST /contact

Accepts form submissions with the following parameters:
- `email`: Sender's email address
- `subject`: Message subject
- `message`: Message content
- `h-captcha-response`: hCaptcha token

Returns:
- **200**: Message sent successfully
- **400**: Missing/invalid fields or failed hCaptcha verification
- **429**: Rate limit exceeded
- **500**: Error sending webhook

## Deployment

This project is configured for deployment on Vercel using the [vercel.json](vercel.json) configuration.

## Development

Start the server locally:

```bash
pip install uv
uv venv
uv run main.py
```
