import abc
from collections import defaultdict

from PIL import Image

# TODO

class GameObject:

    @classmethod
    @abc.abstractmethod
    def type_id(cls) -> str:
        return ''

    def __init__(self):
        self.resource_id: str = ''

    def res_img(self, res_group: str, suffix: str = None) -> Image.Image:
        """
        返回图像资源
        """


class ManagerBase:
    def __init__(self):
        self.data_dict: dict[type[GameObject], dict[str, GameObject]] = defaultdict(lambda: defaultdict(None))

    def register_type(self, t: type[GameObject]):
        pass

    def register(self, id_: str, obj: GameObject):
        pass


if __name__ == '__main__':
    manager = ManagerBase()
    manager.register_type(GameObject)
