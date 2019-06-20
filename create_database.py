from p import *
from models import *
from fixtures import *
from settings import settings

kind = settings.value('DB_KIND', 'sqlite')
server = settings.value('DB_SERVER', 'database.sqlite')
_db = settings.value('DB_NAME', None)
user = settings.value('DB_USER', None)
password = settings.value('DB_PASSWORD', None)

if kind == 'sqlite':
    db.bind(provider='sqlite', filename=server, create_db=True)
else:
    db.bind(provider=kind.lower(), user=user, password=password, host=server, database=_db)

# sql_debug(True)
db.generate_mapping(create_tables=True)

do_account_fixtures(db_session)
do_accounting_type_fixtures(db_session)
do_entry_template_fixtures(db_session)
do_movement_type_fixtures(db_session)
do_setting_fixtures(db_session)