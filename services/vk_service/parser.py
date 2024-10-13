import json
from schemas.vk_user import VkUser

from loguru import logger


class VkParser:
    @staticmethod
    def parse_friends(parent_user_id: int | None, raw_data: str) -> list[VkUser]:
        data: dict = json.loads(raw_data)
        raw_users = data.get("response", {}).get("items", [])
        if len(raw_users) == 0:
            logger.info(f"{data=}")
            logger.warning(f"No friends found for {parent_user_id=}")
            return []

        return [
            VkUser(
                id=user.get("id"),
                first_name=user.get("first_name"),
                last_name=user.get("last_name"),
                parent_friend_id=parent_user_id,
            )
            for user in raw_users
        ]
