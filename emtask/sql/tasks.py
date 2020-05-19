from sql_gen.commands import CreateSQLTaskCommand
from sql_gen.database import Connector, EMDatabase


class RewireVerbSQLTask(object):
    def create_rewire_verb_template(self, verb, new_path):
        self._create_sql(
            "rewire_verb.sql",
            entity_def_id=verb._entity_keyname,
            verb_name=verb._name,
            new_pd_path=new_path,
        )

    def _create_sql(self, *args, **kwargs):
        template_values = dict(**kwargs)
        CreateSQLTaskCommand(
            template_name=args[0], run_once=True, template_values=template_values
        ).run()


class VerbDB(object):
    def __init__(self, entity_keyname=None, name=None, repository_path=None):
        self._entity_keyname = entity_keyname
        self._name = name
        self._repository_path = repository_path

    def fetch(self, repository_path=None):
        v_by_repo_path = (
            "SELECT ci.KEYNAME as ENTITY_KEYNAME, v.NAME, pd.REPOSITORY_PATH"
            " FROM CCADMIN_IDMAP ci , EVA_VERB v, EVA_PROCESS_DESC_REFERENCE pdr,"
            " EVA_PROCESS_DESCRIPTOR PD"
            " WHERE v.PROCESS_DESC_REF_ID  = pdr.id"
            " AND pdr.PROCESS_DESCRIPTOR_ID  = pd.id"
            " AND ci.KEYSET ='ED'"
            " AND ci.ID =v.ENTITY_DEF_ID"
            " AND pd.REPOSITORY_PATH ='{}';"
        )
        connector = Connector(
            "localhost",
            "FP8_HFR2_DEV_AD",
            "FP8_HFR2_DEV_AD",
            "XEPDB1",
            "1521",
            "oracle",
        )
        db = EMDatabase(connector)

        return self.convert_from_db_fetch(
            db.fetch(v_by_repo_path.format(repository_path))
        )

    def convert_from_db_fetch(self, table):
        result = []

        for row in table:
            result.append(
                VerbDB(row["ENTITY_KEYNAME"], row["NAME"], self._repository_path)
            )

        return result
