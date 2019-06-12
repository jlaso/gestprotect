from models import EntryTemplate, EntryTemplateLine, D, H
from .accounting_type import *
from .account import gen_account
from pony.orm import flush


def do_entry_template_fixtures(session):
    first_cash_acc = gen_account(570, 1, 10)
    first_bank_acc = gen_account(572, 1, 10)
    with session:
        i = 1
        if not EntryTemplate.get(id=i):
            EntryTemplate(id=i, desc="Ingreso")
            EntryTemplateLine(entry_template=i,
                              sign=D,
                              account=first_bank_acc,
                              accounting_type=ACC_T_DEPOSIT)
            EntryTemplateLine(entry_template=i,
                              sign=H,
                              account=first_cash_acc,
                              accounting_type=ACC_T_DEPOSIT)
        flush()
