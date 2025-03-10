from loguru import logger
import sys
import json
from config import config


def serialize_extra(record) -> str:
    """Convert extra dict to JSON string if present"""
    if record["extra"]:
        try:
            return f"| metadata={json.dumps(record['extra'])}"
        except Exception:
            return f"| metadata={str(record['extra'])}"
    return ""


def setup_logger():
    # Remove default handler
    logger.remove()

    # Console format with JSON metadata
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level> "
        "{extra}"
    )

    # File format (machine readable)
    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message} "
        "{extra}"
    )

    # Add console handler with colored output
    logger.add(
        sys.stderr,
        format=console_format,
        serialize=serialize_extra,
        level=config.logging["console_level"],
    )

    # Try to add file logging
    try:
        logger.add(
            config.logging["file_path"],
            rotation=config.logging["file_rotation"],
            retention=config.logging["file_retention"],
            format=file_format,
            serialize=serialize_extra,
            enqueue=True,
        )
    except PermissionError:
        logger.warning("Unable to create log file - permission denied")
    except Exception as e:
        logger.warning(f"Unable to set up file logging: {e}")

    return logger
