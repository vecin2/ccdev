from sql_gen.database import Connector, EMDatabase

from emtask import project

_addb = None

host = "database.host"
user = "database.user"
password = "database.pass"
dbname = "database.name"
port = "database.port"
dbtype = "database.type"


def addb():
    dbfactory = _DatabaseFactory()

    return dbfactory.addb()


class _DatabaseFactory(object):
    def addb(self):
        global _addb
        _addb = self._get_db_from_properties(
            host="database.host",
            user="database.user",
            password="database.pass",
            dbname="database.name",
            port="database.port",
            dbtype="database.type",
        )

        return _addb

    def _get_db_from_properties(
        self, host=None, user=None, password=None, dbname=None, port=None, dbtype=None
    ):
        config = project.get_emproject().config()
        connector = Connector(
            config[host],
            config[user],
            config[password],
            config[dbname],
            config[port],
            config[dbtype],
        )

        return EMDatabase(connector)
