from collections import deque
import json

from loguru import logger

from schemas.vk_user import VkUser
from services.vk_service.client import VkHTTPClient
from services.vk_service.parser import VkParser

from services.visualize.vizualize_graph import generate_visual_graph


class ParseFriendsUsecase:
    def __init__(
        self,
        vk_http_client: VkHTTPClient,
        vk_parser: VkParser,
    ):
        self.vk_http_client: VkHTTPClient = vk_http_client
        self.vk_parser: VkParser = vk_parser

        self._mem: dict = {}

    def __call__(
        self,
        first_level_users: list[VkUser],
        depth: int | None = 2,
    ):
        result_friends: list[VkUser] = []
        users_to_parse_q = deque(first_level_users)

        for i in range(depth):
            logger.info(f"iteration {i}")
            tmp_users_storage = []
            while len(users_to_parse_q) > 0:
                user = users_to_parse_q.popleft()

                friends = self._get_friends(user.id)[:10]

                if len(friends) == 0:
                    logger.error(f"no friends for {user.id}")
                    continue

                user.friend_ids = [friend.id for friend in friends]

                result_friends.extend(friends)
                tmp_users_storage.extend(friends)

                logger.success(f"got {len(friends)} friends for {user.id}")

            users_to_parse_q += tmp_users_storage

        return result_friends

    def _exclude_parent_friend(
        self, parent_friend_id: int, friends: list[VkUser]
    ) -> list[VkUser]:
        return [friend for friend in friends if friend.id != parent_friend_id]

    def _get_friends(self, user_id: int) -> list[VkUser]:
        if user_id in self._mem:
            return self._mem[user_id]

        raw_data = self.vk_http_client.get_friends(user_id=user_id)
        friends = self.vk_parser.parse_friends(user_id, raw_data)
        self._mem[user_id] = friends
        return friends
