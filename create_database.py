from p import *
from models import *
from fixtures import *


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

# sql_debug(True)
db.generate_mapping(create_tables=True)

do_account_fixtures(db_session)
do_accounting_type_fixtures(db_session)
do_entry_template_fixtures(db_session)
do_movement_type_fixtures(db_session)
do_setting_fixtures(db_session)