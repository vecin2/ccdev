from sql_gen.emproject.em_project import EMConfigID
from sql_gen.emproject.em_project import EMProject as SQLTaskEMProject


class EMProject(object):
    current_project = None

    def __init__(self, root):
        self.root = root

    def config(self, component="ad", machine_name="localhost"):
        sqltask_emproject = SQLTaskEMProject(emprj_path=self.root)

        return sqltask_emproject.config(EMConfigID("localdev", machine_name, component))


current = None
