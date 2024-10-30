from pydantic import BaseModel

from schemas.vk_user import VkUser


class Config(BaseModel):
    VK_ACCESS_TOKEN: str = ""
    FIRST_LEVEL_USERS_LIST: list[VkUser] = [
        VkUser(
            id="396854328",
            name="Денис Яценко",
            parent_friend_id=None,
        ),
        VkUser(
            id="151413977",
            name="Владислав Утц",
            parent_friend_id=None,
        ),
        VkUser(
            id="144399122",
            name="Александр Чекунков",
            parent_friend_id=None,
        ),
        VkUser(
            id="270780454",
            name="Иван Никонов",
            parent_friend_id=None,
        ),
    ]


config = Config()
