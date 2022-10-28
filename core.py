import sqlalchemy as sql
import cx_Oracle


def connect_oracle(username, password, host, service_name):
    dsn = cx_Oracle.makedsn(host, 1521, service_name).replace('SID', 'SERVICE_NAME')
    return sql.create_engine('oracle+cx_oracle://{}:{}@{}'.format(username, password, dsn))
