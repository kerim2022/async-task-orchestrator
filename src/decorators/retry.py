"""Custom resilience decorators for transient error recovery."""

import asyncio
import functools
import logging
from typing import Callable, Any, Type

logger = logging.getLogger(__name__)


def exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
):
    """Decorator applying exponential backoff retry logic to async functions."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = initial_delay
            for attempt in range(1, max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as err:
                    if attempt == max_retries:
                        logger.error(f"Execution failed after {max_retries} attempts. Error: {err}")
                        raise
                    logger.warning(
                        f"Attempt {attempt}/{max_retries} failed for '{func.__name__}': {err}. "
                        f"Retrying in {delay}s..."
                    )
                    await asyncio.sleep(delay)
                    delay *= backoff_factor

        return wrapper

    return decorator