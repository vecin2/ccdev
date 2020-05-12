from sql_gen.commands import CreateSQLTaskCommand
from sql_gen.database import Connector, EMDatabase


class Verb:

    """Matches EVAVerb in EM"""

    def __init__(self, entity_keyname=None, name=None, repository_path=None):
        self._entity_keyname = entity_keyname
        self._name = name
        self._repository_path = repository_path

    def rewire(self, new_path):
        _run_template(
            "rewire_verb.sql",
            entity_def_id=self._entity_keyname,
            verb_name=self._name,
            new_pd_path=new_path,
        )

    @staticmethod
    def search(path):
        v_by_repo_path = """SELECT ci.KEYNAME as ENTITY_KEYNAME,v.NAME, pd.REPOSITORY_PATH 
FROM CCADMIN_IDMAP ci , EVA_VERB v, EVA_PROCESS_DESC_REFERENCE pdr, EVA_PROCESS_DESCRIPTOR PD
WHERE v.PROCESS_DESC_REF_ID  = pdr.id
AND pdr.PROCESS_DESCRIPTOR_ID  = pd.id
AND ci.KEYSET ='ED'
AND ci.ID =v.ENTITY_DEF_ID
AND pd.REPOSITORY_PATH ='{}';"""
        connector = Connector(
            "localhost",
            "FP8_HFR2_DEV_AD",
            "FP8_HFR2_DEV_AD",
            "XEPDB1",
            "1521",
            "oracle",
        )
        db = EMDatabase(connector)
        table = db.fetch(v_by_repo_path.format(path))
        v = Verb(table[0]["ENTITY_KEYNAME"], table[0]["NAME"], path)

        return [v]


def rewire_verb(current_path=None, new_path=None):
    verbs = Verb.search(current_path)
    verbs[0].rewire(new_path or extension_path(current_path))


def _run_template(*args, **kwargs):
    template_values = dict(**kwargs)
    CreateSQLTaskCommand(
        template_name=args[0], run_once=True, template_values=template_values
    ).run()


def extension_path(otb_process_path):
    return "TODO implement"
