from collections import defaultdict

from object import GameObject


class AliasManager:
    def __init__(self):
        self.alias2obj: dict[str, GameObject] = defaultdict(None)

    def get_obj(self, s: str) -> GameObject | None:
        return self.alias2obj.get(s)
