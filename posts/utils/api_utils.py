import requests

BASE_URL = "https://dev.codeleap.co.uk/careers/"


def verify_post_exists(post_id):
    try:
        response = requests.get(f"{BASE_URL}{post_id}/")
        return response.status_code == 200
    except Exception:
        return False
