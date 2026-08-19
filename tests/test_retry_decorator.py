"""Unit tests for resilient exponential backoff retry decorator."""

import pytest
from src.decorators.retry import exponential_backoff


@pytest.mark.asyncio
async def test_retry_success():
    call_count = 0

    @exponential_backoff(max_retries=3, initial_delay=0.01)
    async def transient_func():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise ValueError("Transient error")
        return "success"

    result = await transient_func()
    assert result == "success"
    assert call_count == 2


@pytest.mark.asyncio
async def test_retry_failure_max_attempts():
    call_count = 0

    @exponential_backoff(max_retries=3, initial_delay=0.01, exceptions=(ValueError,))
    async def always_fails():
        nonlocal call_count
        call_count += 1
        raise ValueError("Persistent failure")

    with pytest.raises(ValueError):
        await always_fails()

    assert call_count == 3