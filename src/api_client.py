import logging
from typing import Any
import requests
from base64 import b64encode
import os
from dotenv import load_dotenv
from ruamel.yaml import YAML

from exception.WakatimeCredentialsMissingErrro import WakatimeCredentialsMissingError

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

_ = load_dotenv()


def get_last_7_days_data() -> dict[str, dict[str, Any] | list[dict[str, Any]]]:
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


def get_github_languages_info() -> list[dict[str, Any]]:
    url = "https://raw.githubusercontent.com/github-linguist/linguist/master/lib/linguist/languages.yml"

    response = requests.get(url)

    log.debug(f"Response status code: {response.status_code}")

    yaml = YAML()
    languages: dict[str, Any] = yaml.load(response.text)

    languages_data: list[dict[str, Any]] = []

    for key in languages.keys():
        language = {"name": key, **languages.get(key)}
        languages_data.append(language)

    return languages_data


if __name__ == "__main__":
    # _ = get_last_7_days_data()
    _ = get_github_languages_info()
