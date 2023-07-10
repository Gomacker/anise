import asyncio
import urllib.parse
from enum import Enum

from PIL import Image
from pydantic import BaseModel

from config import MAIN_URL
from object import GameObject
from resource import ResourceGroupLocal, ResourceTypeImage, ResourceGroupNetwork


def _url_getter_worldflipper(suffix: str):
    def temp(id_: str, obj: GameObject):
        url = urllib.parse.urljoin(MAIN_URL, f'/static/{obj.type_id()}/{id_}/{obj.resource_id}.{suffix}')
        print(url)
        return url

    return temp


class Icon(GameObject):

    @classmethod
    def type_id(cls) -> str:
        return 'worldflipper/icon'

    class Res:
        base = ResourceGroupNetwork('', ResourceTypeImage, _url_getter_worldflipper('png'))


class Element(Enum):
    ALL = -1
    FIRE = 0
    WATER = 1
    THUNDER = 2
    WIND = 3
    LIGHT = 4
    DARK = 5


class SpecialityType(Enum):
    KNIGHT = 0
    FIGHTER = 1
    RANGED = 2
    SUPPORTER = 3
    SPECIAL = 4


class Race(Enum):
    HUMAN = 0
    BEAST = 1
    MYSTERY = 2
    ELEMENT = 3
    DRAGON = 4
    MACHINE = 5
    DEVIL = 6
    PLANTS = 7
    AQUATIC = 8
    UNDEAD = 9


# class Gender(Enum):
#     FEMALE = 0
#     MALE = 1
#     UNKNOWN = 2


class SkillBase(BaseModel):
    name: str
    weight: int
    description: str


class Character(GameObject):
    @classmethod
    def type_id(cls) -> str:
        return 'worldflipper/unit'
        # return 'worldflipper/character'

    class Res:
        square212x_0__ = ResourceGroupNetwork('square212x/base', ResourceTypeImage, _url_getter_worldflipper('png'))
        square212x_0 = ResourceGroupLocal('square212x/base', ResourceTypeImage, 'png')
        square212x_1 = ResourceGroupLocal('square212x/awakened', ResourceTypeImage, 'png')
        full_0 = ResourceGroupLocal('full/base', ResourceTypeImage, 'png')
        full_1 = ResourceGroupLocal('full/awakened', ResourceTypeImage, 'png')
        full_resized_0 = ResourceGroupLocal('full_resized/base', ResourceTypeImage, 'png')
        full_resized_1 = ResourceGroupLocal('full_resized/awakened', ResourceTypeImage, 'png')
        party_main = ResourceGroupLocal('party_main', ResourceTypeImage, 'png')
        party_unison = ResourceGroupLocal('party_unison', ResourceTypeImage, 'png')
        pixelart_special = ResourceGroupLocal('pixelart/special', ResourceTypeImage, 'gif')
        pixelart_walk_front = ResourceGroupLocal('pixelart/walk_front', ResourceTypeImage, 'gif')

    names: list[str]
    rarity: int
    element: Element
    type: SpecialityType
    race: list[Race]
    # gender: Gender
    gender: str  # 因为莉莉的原因，暂时不做枚举

    skill: SkillBase

    abilities: list[str]
    description: str
    obtain: str
    tags: list[str]


class Equipment(GameObject):
    @classmethod
    def type_id(cls) -> str:
        return 'worldflipper/equipment'

    class Res:
        pass


if __name__ == '__main__':
    async def main():
        print(_url_getter_worldflipper('png')('', Icon('fire')))
        img: Image.Image = await Icon('fire').res(Icon.Res.base)
        img.show()


    icon = Icon('fire')
    print(icon.model_dump())
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    asyncio.set_event_loop(loop)
