import json
import os


def get_firebase_credentials():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        credentials_path = os.path.join(base_dir, "./serviceAccountKey.json")

        with open(credentials_path, "r") as file:
            credentials = json.load(file)
            return credentials.get("api_key")
    except Exception as e:
        raise Exception(f"Error reading Firebase credentials: {str(e)}")
