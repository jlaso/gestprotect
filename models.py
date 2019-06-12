from datetime import date
from pony.orm import *


db = Database()

D = True
H = False


class Animal(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str, 40)
    birth_date = Optional(date)
    chip = Optional(str)
    expense_account = Optional(int, size=64)
    income_account = Optional(int, size=64)
    male = Optional(bool)
    animal_movements = Set('AnimalMovement')


class Account(db.Entity):
    id = PrimaryKey(int)
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
    member_account = Optional(int, size=64)


class Setting(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    value = Required(str)


class AccountingType(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 50)
    accountings = Set(Accounting)
    entry_template_lines = Set('EntryTemplateLine')


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


class EntryTemplate(db.Entity):
    id = PrimaryKey(int, auto=True)
    desc = Optional(str, 150)
    entry_template_lines = Set('EntryTemplateLine')


class EntryTemplateLine(db.Entity):
    id = PrimaryKey(int, auto=True)
    entry_template = Required(EntryTemplate)
    sign = Optional(bool)
    account = Optional(int, size=64)
    accounting_type = Required(AccountingType)



