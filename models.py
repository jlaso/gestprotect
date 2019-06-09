from datetime import date
from pony.orm import *


db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)


class Animal(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str, 40)
    birth_date = Optional(date)
    chip = Optional(str)
    expense_account = Optional(int, size=24)
    income_account = Optional(int, size=24)
    male = Optional(bool)
    animal_movements = Set('AnimalMovement')


class Account(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str, 100)
    accountings = Set('Accounting')


class Accounting(db.Entity):
    id = PrimaryKey(int, auto=True)
    entry = Required('Entry')
    sign = Required(bool)
    account = Required(Account)
    accounting_type = Required('AccountingType')


class Entry(db.Entity):
    id = PrimaryKey(int, auto=True)
    date = Optional(date)
    num = Optional(int)
    desc = Optional(str, 150)
    accountings = Set(Accounting)


class Member(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 100)
    member_account = Optional(int, size=24)


class Setting(db.Entity):
    id = Required(int)
    name = Required(str)
    value = Required(str)
    PrimaryKey(id, name)


class AccountingType(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 50)
    accountings = Set(Accounting)


class MovementType(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 60)
    animal_movements = Set('AnimalMovement')


class AnimalMovement(db.Entity):
    id = PrimaryKey(int, auto=True)
    date = Required(date)
    movement_type = Required(MovementType)
    animal = Required(Animal)
    third_party = Required('ThirdParty')


class ThirdParty(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 100)
    animal_movements = Set(AnimalMovement)
    phone = Optional(str)
    city = Optional(str)
    address = Optional(str)


sql_debug(True)
db.generate_mapping(create_tables=True)


with db_session:
    if not MovementType[1]:
        MovementType(id=1, name="Abandono")
    if not MovementType[2]:
        MovementType(id=2, name="Recuperación")
    if not MovementType[3]:
        MovementType(id=3, name="Acogida")
    if not MovementType[4]:
        MovementType(id=4, name="Adopción")
    if not MovementType[5]:
        MovementType(id=5, name="Nacimiento")
    if not MovementType[6]:
        MovementType(id=6, name="Fallecimiento")
    if not MovementType[7]:
        MovementType(id=7, name="Entregado Autoridades")
    if not MovementType[8]:
        MovementType(id=8, name="Recogido")
