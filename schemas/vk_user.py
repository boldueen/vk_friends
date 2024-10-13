from pydantic import BaseModel


class VkUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    parent_friend_id: int | None
    friend_ids: list[int] | None = None
