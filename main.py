import sys
import json
import time
from loguru import logger
from schemas.vk_user import VkUser
from services.visualize.vizualize_graph import generate_visual_graph
from services.vk_service.client import VkHTTPClient
from config import config
from services.vk_service.parser import VkParser
from usecases.parse_friends import ParseFriendsUsecase


def main(vizualize: bool = False):
    logger.info("Starting...")
    logger.info(f"{vizualize=}")
    vk_client = VkHTTPClient(config.VK_ACCESS_TOKEN)
    vk_parser = VkParser()
    usecase = ParseFriendsUsecase(
        vk_client,
        vk_parser,
        vizualize=vizualize,
        filepath=f"{int(time.time())}_parsed_friends.json",
    )
    friends_graph: list[VkUser] = usecase(config.FIRST_LEVEL_USERS_LIST)  # type: ignore

    logger.info(friends_graph)

    with open("graph.json", "w") as f:
        json.dump([f.model_dump() for f in friends_graph], f)
        if vizualize:
            generate_visual_graph([f.model_dump() for f in friends_graph])


if __name__ == "__main__":
    args = sys.argv
    vizualize = False
    if "-vz" or "--vizualize" in args:
        vizualize = True
    main(vizualize=vizualize)
