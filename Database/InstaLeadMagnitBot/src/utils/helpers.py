"""Helper utility functions."""

import asyncio
import random
import re
import sys
from pathlib import Path
from typing import Optional

from loguru import logger


def extract_post_id_from_url(url: str) -> Optional[str]:
    """Extract Instagram post shortcode from URL.

    Args:
        url: Instagram post URL

    Returns:
        Post shortcode or None if not found
    """
    patterns = [
        r"instagram\.com/p/([A-Za-z0-9_-]+)",
        r"instagram\.com/reel/([A-Za-z0-9_-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


async def random_delay(min_sec: int, max_sec: int) -> None:
    """Async random delay between min and max seconds.

    Args:
        min_sec: Minimum delay in seconds
        max_sec: Maximum delay in seconds
    """
    delay = random.uniform(min_sec, max_sec)
    logger.debug(f"Delay {delay:.1f} seconds")
    await asyncio.sleep(delay)


def format_template(template: str, **kwargs) -> str:
    """Format message template with variables.

    Supported variables: {username}, {post_url}, {keyword}

    Args:
        template: Message template string
        **kwargs: Variables to substitute

    Returns:
        Formatted message string
    """
    try:
        return template.format(**kwargs)
    except KeyError as e:
        logger.warning(f"Missing variable in template: {e}")
        return template


def setup_logging(log_level: str, log_file: str) -> None:
    """Configure loguru logging.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Path to log file
    """
    # Remove default handler
    logger.remove()

    # Console handler
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{module}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )

    # Create log directory if needed
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # File handler
    logger.add(
        log_file,
        rotation="10 MB",
        retention="7 days",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {module}:{line} | {message}",
    )
