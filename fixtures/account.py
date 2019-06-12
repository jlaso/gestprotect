import csv
import os
import math
from models import Account
from pony.orm import *


def gen_account(base, index, digits):
    """generates an account with digits based on base and ending in index"""
    d1 = math.ceil(math.log(base, 10))
    return base * pow(10, digits-d1) + index


def do_account_fixtures(session, _file="es_pyme_esfl_2013.csv"):
    with session:
        if True:
            delete(i for i in Account.select())
            flush()
            path = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(path, _file)) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    c = int(row[0])
                    n = row[1]
                    # print(c, n)
                    if not Account.get(id=c):
                        Account(id=c, name=n)

        for a in Account.select().order_by(lambda p: str(p.id)):
            print(a.id, a.name)
