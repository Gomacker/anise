import abc
from typing import Any

from PIL import Image
from pydantic import BaseModel


class GameObject(BaseModel):
    resource_id: str

    def __init__(self, resource_id: str = '', **data: Any):
        data['resource_id'] = resource_id
        super().__init__(**data)
        # self.resource_id: str = resource_id

    @classmethod
    @abc.abstractmethod
    def type_id(cls) -> str:
        return ''

    async def res(self, res_group: "ResourceGroup") -> Image.Image | None:
        """
        返回资源
        """
        return await res_group.get(self)
