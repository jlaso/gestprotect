from models import AccountingType
from pony.orm import flush

ACC_T_PURCHASE = 1
ACC_T_DEPOSIT = 2
ACC_T_EXPENSE = 3

"""Spanish words"""
data = {
    ACC_T_PURCHASE: "Compra",
    ACC_T_DEPOSIT: "Ingreso",
    ACC_T_EXPENSE: "Gasto",
}


def do_accounting_type_fixtures(session):
    with session:
        for i in data:
            if not AccountingType.get(id=i):
                AccountingType(id=i, name=data[i])
            else:
                AccountingType[i].name = data[i]
        flush()
