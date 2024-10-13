from aiohttp import ClientSession

from config import config
from loguru import logger

import requests

from tenacity import retry


class VkHTTPClient:
    _access_token: str
    _api_version: str = "5.81"

    def __init__(self, access_token: str) -> None:
        self.base_url = "https://api.vk.com/method"
        self._access_token = access_token
        self._auth_token = f"BEARER {access_token}"

    def get_friends(self, user_id: int) -> str:
        response = requests.get(
            f"{self.base_url}/friends.get?user_id={user_id}&access_token={self._access_token}&v={self._api_version}&fields=nickname"
        )
        logger.info(response.status_code)
        if "access_token has expired" in response.text:
            self.refresh_access_token()
            response = requests.get(
                f"{self.base_url}/friends.get?user_id={user_id}&access_token={self._access_token}&v={self._api_version}&fields=nickname"
            )
        logger.info(response.status_code)

        return response.text

    def refresh_access_token(self) -> None:
        new_token = input("Press Enter new access token to continue...")
        self._access_token = new_token
