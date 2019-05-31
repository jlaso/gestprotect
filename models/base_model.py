from ..db import db


class BaseModel:
    _query = None
    _id = 0

    def save(self):
        pass
