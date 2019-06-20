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


def get_accounts(lambda_filter=None):
    with db_session:
        if lambda_filter:
            accounts = Account.select(lambda_filter)
        else:
            accounts = Account.select()
        return [{'id': a.id, 'name': a.name} for a in accounts.order_by(lambda p: str(p.id))]


def add_account(**kwargs):
    if 'id' not in kwargs or 'name' not in kwargs:
        raise Exception('cuenta y nombre son obligatorios')
    _id = int(kwargs['id'])
    _name = kwargs['name']
    print("%d %s" % (_id, _name))
    with db_session:
        if Account.get(name=_name) or Account.get(id=_id):
            raise Exception('Ya existe una cuenta con ese código o nombre')
        Account(id=_id, name=_name)
        flush()


def change_account(**kwargs):
    if 'id' not in kwargs or 'name' not in kwargs:
        raise Exception('cuenta y nombre son obligatorios')
    _id = int(kwargs['id'])
    _name = kwargs['name']
    print("%d %s" % (_id, _name))
    with db_session:
        if not Account.get(id=_id):
            raise Exception('No existe una cuenta con ese código')
        Account.get(id=_id).name = _name
        flush()


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
