from pydantic import BaseModel

from schemas.vk_user import VkUser


class Config(BaseModel):
    VK_ACCESS_TOKEN: str = "vk1.a.6_ckGOqg1eHPAyoinwfEc_BjplTo6LOcsbk5Fobhh5NZdc33aQ-gV9GZukhgqLRQ9OuDq36ZxLgS9f19TQJZEhHZa8_4Xkub0seBWxhBrUKVjWkARRWxR1RoURcNMbAftyagVUZxzfmpSRy_K33jgMUaw7nYev1W6i5tEYqJ7DyDiy68uYEMA6ShfUnhWD6uZkPxPh9dZ0ZyWuANGTRCkA"
    FIRST_LEVEL_USERS_LIST: list[VkUser] = [
        VkUser(
            id=396854328,
            first_name="Денис",
            last_name="Яценко",
            parent_friend_id=None,
        ),
        VkUser(
            id=151413977,
            first_name="Владислав",
            last_name="Утц",
            parent_friend_id=None,
        ),
        VkUser(
            id=144399122,
            first_name="Александр",
            last_name="Чекунков",
            parent_friend_id=None,
        ),
        VkUser(
            id=270780454,
            first_name="Иван",
            last_name="Никонов",
            parent_friend_id=None,
        ),
    ]


config = Config()
