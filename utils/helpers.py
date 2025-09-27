import time
import requests

def handle_api_errors(func, *args, retries=3, delay=5, **kwargs):
    """
    Calls a function (like requests.get) with retries on failure
    """
    for attempt in range(retries):
        try:
            response = func(*args, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"API request failed ({attempt+1}/{retries}): {e}")
            time.sleep(delay)
    raise Exception("Max retries exceeded")
