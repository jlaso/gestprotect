from .base_model import BaseModel


class Account(BaseModel):
    code = ""
    name = ""

    def save(self):
        if self._id == 0:
            print("save new")
        else:
            print("save update")
