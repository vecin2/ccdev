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

    def add_sqlmodule(self, module_name):
        return SQLModule(self.root / "modules" / module_name).save()

    def sqlmodules(self):
        return [SQLModule(path) for path in (self.root / "modules").iterdir()]


class SQLModule:
    def __init__(self, path):
        self._root = path  # pathlib
        self.name = path.name

    def add_release(self, release_name):
        release_path = self._update_path() / release_name
        release_path.mkdir(parents=True)

        return release_path

    def releases(self):
        return self._update_path().iterdir()

    def _update_path(self):
        return self._root / "sqlScripts/oracle/update"

    def save(self):
        self._root.mkdir(parents=True)

        return self


_emproject = None


def get_emproject():
    return _emproject


def set_emproject(project):
    global _emproject
    _emproject = project
