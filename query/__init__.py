class QueryManager:
    def __init__(self):
        self.query_map: list[dict] = list()
        self.query_types: dict[str, type[QuerySet]] = dict()

