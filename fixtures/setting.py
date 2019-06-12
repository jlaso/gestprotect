from models import Setting
from pony.orm import flush


SETT_NUM_DIGITS = "num_digits"

data = {
    SETT_NUM_DIGITS: "10",
}


def do_setting_fixtures(session):
    with session:
        for i in data:
            if not Setting.get(name=i):
                Setting(name=i, value=data[i])
            else:
                Setting.get(name=i).value = data[i]
        flush()

