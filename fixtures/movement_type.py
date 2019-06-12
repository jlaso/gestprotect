from models import MovementType
from pony.orm import flush

MT_ABANDON = 1
MT_RESCUE = 2
MT_FOSTER = 3
MT_ADOPTION = 4
MT_BIRTH = 5
MT_DEATH = 6
MT_DELIV_AUTH = 7
MT_PICKED_UP = 8

"""Spanish words"""
data = {
    MT_ABANDON: "Abandono",
    MT_RESCUE: "Rescate",
    MT_FOSTER: "Acogida",
    MT_ADOPTION: "Adopción",
    MT_BIRTH: "Nacimiento",
    MT_DEATH: "Defunción",
    MT_DELIV_AUTH: "Entregado Autoridades",
    MT_PICKED_UP: "Recogido",
}


def do_movement_type_fixtures(session):
    with session:
        for i in data:
            if not MovementType.get(id=i):
                MovementType(id=i, name=data[i])
            else:
                MovementType[i].name = data[i]
        flush()
