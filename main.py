import sys
import json
import time
from loguru import logger
from schemas.vk_user import VkUser
from services.vk_service.client import VkHTTPClient
from config import config
from services.vk_service.parser import VkParser
from usecases.parse_friends import ParseFriendsUsecase


def main():
    logger.info("Starting...")

    vk_client = VkHTTPClient(config.VK_ACCESS_TOKEN)
    vk_parser = VkParser()
    usecase = ParseFriendsUsecase(
        vk_client,
        vk_parser,
    )
    friends_graph: list[VkUser] = usecase(config.FIRST_LEVEL_USERS_LIST)  # type: ignore

    with open(f"{int(time.time())}_parsed_friends.json", "w") as f:
        json.dump([f.model_dump() for f in friends_graph], f)


if __name__ == "__main__":
    main()
