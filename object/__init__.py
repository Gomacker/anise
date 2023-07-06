import abc
from PIL import Image


class GameObject:
    def __init__(self, resource_id: str):
        self.resource_id: str = resource_id

    @classmethod
    @abc.abstractmethod
    def type_id(cls) -> str:
        return ''

    async def res(self, res_group: "ResourceGroup") -> Image.Image | None:
        """
        返回资源
        """
        return await res_group.get(self)

