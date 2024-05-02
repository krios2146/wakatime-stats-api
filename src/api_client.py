import logging
from typing import Any
import requests
from base64 import b64encode
import os
from dotenv import load_dotenv

from exception.WakatimeCredentialsMissingErrro import WakatimeCredentialsMissingError

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

_ = load_dotenv()


def get_last_7_days_data() -> dict[str, dict[str, Any]]:
    base_url: str | None = os.getenv("WAKATIME_BASE_URL")
    api_key: str | None = os.getenv("WAKATIME_API_KEY")

    if api_key is None:
        log.error("WAKATIME_API_KEY couldn't be obtained from the .env file")
        raise WakatimeCredentialsMissingError(
            "WAKATIME_API_KEY is None, aborting API call"
        )

    if base_url is None:
        log.error("WAKATIME_BASE_URL couldn't be obtained from the .env file")
        raise WakatimeCredentialsMissingError(
            "WAKATIME_BASE_URL is None, aborting API call"
        )

    api_key_encoded = b64encode(api_key.encode())

    headers = {"Authorization": f"Basic {api_key_encoded.decode()}"}

    response = requests.get(
        f"{base_url}/users/krios2146/stats/last_7_days", headers=headers
    )

    log.debug(f"Response status code: {response.status_code}")

    return response.json()["data"]


def get_github_languages_info() -> str:
    url = "https://raw.githubusercontent.com/github-linguist/linguist/master/lib/linguist/languages.yml"

    response = requests.get(url)

    log.debug(f"Response status code: {response.status_code}")

    return response.text


if __name__ == "__main__":
    # _ = get_last_7_days_data()
    _ = get_github_languages_info()
