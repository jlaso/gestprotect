from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from settings import settings
from models import *


class DB:
    SCHEMA = "public"
    # db = None

    def open(self):
        global db
        kind = settings.value('DB_KIND', 'sqlite')
        server = settings.value('DB_SERVER', 'database.sqlite')
        _db = settings.value('DB_NAME', None)
        user = settings.value('DB_USER', None)
        password = settings.value('DB_PASSWORD', None)
        kind = "Q%s" % kind.upper()
        print(kind, server, _db, user, password)
        # self.db = QSqlDatabase.addDatabase(kind)
        # self.db.setDatabaseName(_db)
        # if kind != 'QSQLITE':
        #     self.db.setHostName(server)
        #     self.db.setUserName(user)
        #     self.db.setPassword(password)
        # r = self.db.open()
        # print("db.open result", r)
        # return r
        if kind != 'QSQLITE':
            db.bind(provider=kind.lower(), user=user, password=password, host=server, database=_db)
        else:
            db.bind(provider='sqlite', filename=server, create_db=True)

        # sql_debug(True)
        db.generate_mapping(create_tables=True)

    def last_error(self):
        return self.db.lastError()

    def get_accounts(self, where=None):
        return [{'id': a.id, 'name': a.name} for a in Account.select().order_by(lambda p: str(p.id))]
        # q = "select * from %s.account" % self.SCHEMA
        # if where:
        #     q += " " + where
        # q += " order by id asc"
        # query = QSqlQuery()
        # result = []
        # query.exec_(q)
        # while query.next():
        #     _id = int(query.value(0))
        #     name = str(query.value(1))
        #     result.append({
        #         'id': _id,
        #         'name': name,
        #     })
        # return result

    def add_account(self, **kwargs):
        if 'id' not in kwargs or 'name' not in kwargs:
            raise Exception('cuenta y nombre son obligatorios')
        _id = int(kwargs['id'])
        _name = kwargs['name']
        print("%d %s" % (_id, _name))
        if self.get_accounts(where="`id`=%d or `name`='%s'" % (_id, _name)):
            raise Exception('Ya existe una cuenta con ese código o nombre')
        query = QSqlQuery()
        query.prepare("INSERT INTO %s.account (id, name) " % self.SCHEMA +
                      "VALUES (:id, :name)")
        query.bindValue(":id", _id)
        query.bindValue(":name", _name)
        query.exec_()


db = DB()
