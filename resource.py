import abc
import asyncio
import io
from pathlib import Path
from typing import Any, Callable

import httpx
from PIL import Image

from config import RES_PATH, MAIN_URL
from object import GameObject


class ResourceType(abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    async def read(cls, bytes_: bytes) -> Any:
        """处理二进制数据"""

    @classmethod
    @abc.abstractmethod
    async def write(cls, bytes_: bytes, path: Path) -> None:
        """保存数据"""


class ResourceTypeImage(ResourceType):

    @classmethod
    @abc.abstractmethod
    async def read(cls, bytes_: bytes) -> Image.Image:
        return Image.open(io.BytesIO(bytes_))

    @classmethod
    @abc.abstractmethod
    async def write(cls, bytes_: bytes, path: Path) -> None:
        path.write_bytes(bytes_)


class ResourceGroup:
    def __init__(self, id_: str, type_: type[ResourceType]):
        self.id: str = id_
        self.type: type[ResourceType] = type_

    @abc.abstractmethod
    async def get(self, obj: GameObject) -> Any:
        return None


class ResourceGroupLocal(ResourceGroup):
    def __init__(self, id_: str, type_: type[ResourceType], suffix: str):
        super().__init__(id_, type_)
        self.suffix = suffix

    async def get(self, obj: GameObject) -> Any:
        path = RES_PATH / obj.type_id() / self.id / f'{obj.resource_id}.{self.suffix}'
        # os.makedirs(path.parent, exist_ok=True)
        if path.exists():
            return await self.type.read(path.read_bytes())
        else:
            return None


class ResourceGroupNetwork(ResourceGroup):
    def __init__(self, id_: str, type_: type[ResourceType], url_getter: Callable[[str, GameObject], str]):
        super().__init__(id_, type_)
        self.url_getter = url_getter

    async def get(self, obj: GameObject) -> Any:
        url = self.url_getter(self.id, obj)
        if not url:
            return None
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
        return await self.type.read(r.content)


class ResourceGroupNetworkCacheable(ResourceGroupNetwork):
    def __init__(self, id_: str, type_: type[ResourceType], suffix: str, url_getter: Callable[[str, GameObject], str]):
        super().__init__(id_, type_, url_getter)
        self.suffix = suffix

    async def get(self, obj: GameObject) -> Any:
        path = RES_PATH / obj.type_id() / self.id / f'{obj.resource_id}.{self.suffix}'
        # if not path.exists():
        #     a = await super().get(obj)
        #     io.BytesIO(bytes(a))

if __name__ == '__main__':
    async def main():
        class TestObject(GameObject):
            @classmethod
            def type_id(cls) -> str:
                return 'worldflipper/icon'

        img: Image.Image = await ResourceGroupNetwork('', ResourceTypeImage, lambda id_, obj: f'{MAIN_URL.removesuffix("/")}/static/{obj.type_id()}/{id_}/{obj.resource_id}.png').get(TestObject('fire'))
        img.show()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    asyncio.set_event_loop(loop)