from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from settings import settings


class DB:
    SCHEMA = "public"
    db = None

    def open(self):
        kind = settings.value('DB_KIND', 'MySQL')
        server = settings.value('DB_SERVER', 'localhost')
        _db = settings.value('DB_NAME', 'db')
        user = settings.value('DB_USER', 'user')
        password = settings.value('DB_PASSWORD', 'psw')
        kind = 'QPSQL' if kind != 'MySQL' else 'QMYSQL'
        print(kind, server, _db, user, password)
        self.db = QSqlDatabase.addDatabase(kind)
        self.db.setHostName(server)
        self.db.setDatabaseName(_db)
        self.db.setUserName(user)
        self.db.setPassword(password)
        r = self.db.open()
        print("db.open result", r)

    def last_error(self):
        return self.db.lastError()

    def get_accounts(self, where=None):
        q = "select * from %s.account" % self.SCHEMA
        if where:
            q += " " + where
        q += " order by id asc"
        query = QSqlQuery()
        result = []
        query.exec_(q)
        while query.next():
            _id = int(query.value(0))
            name = str(query.value(1))
            result.append({
                'id': _id,
                'name': name,
            })
        return result

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
