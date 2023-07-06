import asyncio

from PIL import Image

from config import MAIN_URL
from object import GameObject
from resource import ResourceGroupLocal, ResourceTypeImage, ResourceGroupNetwork


def _url_getter_worldflipper(suffix: str):
    def temp(id_: str, obj: GameObject):
        return f'{MAIN_URL.removesuffix("/")}/static/{obj.type_id()}/{id_}/{obj.resource_id}.{suffix}'

    return temp


class Icon(GameObject):
    @classmethod
    def type_id(cls) -> str:
        return 'worldflipper/icon'

    RES = ResourceGroupNetwork('', ResourceTypeImage, _url_getter_worldflipper('png'))


class Character(GameObject):
    @classmethod
    def type_id(cls) -> str:
        return 'worldflipper/character'

    class Res:
        square212x = ResourceGroupLocal('square212x', ResourceTypeImage, 'png')
        full = ResourceGroupLocal('full', ResourceTypeImage, 'png')
        full_resize = ResourceGroupLocal('full_resize', ResourceTypeImage, 'png')
        party_main = ResourceGroupLocal('party_main', ResourceTypeImage, 'png')
        party_unison = ResourceGroupLocal('party_unison', ResourceTypeImage, 'png')
        pixelart__special = ResourceGroupLocal('pixelart/special', ResourceTypeImage, 'gif')
        pixelart__walk_front = ResourceGroupLocal('pixelart/walk_front', ResourceTypeImage, 'gif')


class Equipment(GameObject):
    pass


if __name__ == '__main__':
    async def main():
        img: Image.Image = await Icon('fire').res(Icon.RES)
        img.show()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    asyncio.set_event_loop(loop)
