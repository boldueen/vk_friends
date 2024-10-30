import sys
import json
import time
from loguru import logger
from schemas.vk_user import VkUser
from services.vk_service.client import VkHTTPClient
from config import config
from services.vk_service.parser import VkParser
from usecases.parse_friends import ParseUserFriendsUsecase


def main():
    logger.info("Starting...")

    vk_client = VkHTTPClient(config.VK_ACCESS_TOKEN)
    usecase = ParseUserFriendsUsecase(
        vk_client,
    )
    filename = f"{int(time.time())}_parsed_friends.json"

    for user in config.FIRST_LEVEL_USERS_LIST:
        logger.info(f"parsing {user.name}")
        friends = usecase(user)

        with open(filename, "w") as f:
            json.dump([friend.model_dump() for friend in friends], f)


if __name__ == "__main__":
    main()
