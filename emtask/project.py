from pathlib import Path

from sql_gen.emproject.em_project import EMConfigID
from sql_gen.emproject.em_project import EMProject as SQLTaskEMProject


class EMProject(object):
    current_project = None

    def __init__(self, root):
        self.root = Path(root)

    def config(self, component="ad", machine_name="localhost"):
        sqltask_emproject = SQLTaskEMProject(emprj_path=self.root)

        return sqltask_emproject.config(EMConfigID("localdev", machine_name, component))

    def get_repo(self):
        return self.root / "repository/default"

    def get_product_repo(self):
        return Path(self.config()["product.home"]) / "repository/default"

    def get_ced(self):
        return

    # ced = MultiRootCED(sample_project().get_repo(), sample_project().get_product_repo())


_emproject = None


def get_emproject():
    return _emproject


def set_emproject(project):
    global _emproject
    _emproject = project
