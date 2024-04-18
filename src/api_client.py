import logging as log
import requests
from base64 import b64encode
import os
from dotenv import load_dotenv

log.basicConfig(
    format="%(asctime)s -- %(levelname)s -- [%(module)s]: %(message)s",
    datefmt="%Y-%m-%d @ %H:%M:%S",
    level=log.DEBUG,
)


def get_last_7_days_data():
    _ = load_dotenv()

    base_url: str | None = os.getenv("WAKATIME_BASE_URL")
    api_key: str | None = os.getenv("WAKATIME_API_KEY")

    if api_key is None:
        log.error("WAKATIME_API_KEY couldn't be obtained from the .env file")
        return

    if base_url is None:
        log.error("WAKATIME_BASE_URL couldn't be obtained from the .env file")
        return

    api_key_encoded = b64encode(api_key.encode())

    headers = {"Authorization": f"Basic {api_key_encoded.decode()}"}

    response = requests.get(
        f"{base_url}/users/krios2146/stats/last_7_days", headers=headers
    )

    log.debug(f"Response status code: {response.status_code}")

    return response.json()["data"]


if __name__ == "__main__":
    _ = get_last_7_days_data()
