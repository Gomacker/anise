import abc
import enum
from pathlib import Path
from typing import Type

from PIL import Image


class ResourceType(enum.Enum):
    PNG = 1
    # JPEG = 2
    GIF = 3


class ResourceGroup:
    def __init__(self, id_: str, type_: ResourceType):
        self.id = id_
        self.type = type_


class GameObject:
    def __init__(self):
        self.resource_id: str = ''

    @classmethod
    @abc.abstractmethod
    def type_id(cls) -> str:
        return ''

    def res(self, res_group: ResourceGroup) -> Image.Image | None:
        """
        返回资源
        """
        from manager import manager
        return manager.res.get(res_group, self)


class ResourceManager:
    def __init__(self, path: Path):
        self.path = path

    def register(self, type_: Type[GameObject], res_group: ResourceGroup):
        pass

    def get(self, res_group: ResourceGroup, obj: GameObject) -> Image.Image | None:
        if res_group.type == ResourceType.PNG:
            path = self.path / res_group.id / f'{obj.resource_id}.png'
        elif res_group.type == ResourceType.GIF:
            path = self.path / res_group.id / f'{obj.resource_id}.gif'
        else:
            return None
        if path.exists():
            return Image.open(path)
        else:
            return None
