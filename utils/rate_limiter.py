import time

from config import RATE_LIMIT_WINDOW, RATE_LIMIT

request_timestamps = []

def check_rate_limit():
    """
    Check if the rate limit has been exceeded.
    """
    global request_timestamps
    now = time.time()
    request_timestamps = [t for t in request_timestamps if now - t < RATE_LIMIT_WINDOW]
    if len(request_timestamps) >= RATE_LIMIT:
        raise Exception(f"Rate limit exceeded. Please try again after {RATE_LIMIT_WINDOW} seconds.")
    request_timestamps.append(now)
