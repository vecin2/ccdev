import os
import shutil
from pathlib import Path

from emtask import project
from emtask.project import EMProject


def sample_project(db_connector=None):
    return SampleProjectBuilder(db_connector=db_connector).build()


def sample_product():
    return SampleProjectBuilder(project_name="sample_product").build()


class SampleProjectBuilder(object):
    def __init__(self, project_name="sample_project", db_connector=None):
        self.db_connector = db_connector
        script_dir = os.path.dirname(__file__)
        path = script_dir + os.sep + project_name
        self._default_root = Path(path)

        if self._default_root.exists():
            shutil.rmtree(self._default_root)
        # todo use /dev/shm for faster tests (check rope testutils::sample_project)

    def build(self):
        if self.db_connector:
            conn_details = self._setup_dbconnector()
            self.append_to_config(namevalue_pairs=conn_details)

        users_dat_content = "admin,admin,Administrator\ngtx_system, gtx_system"
        self.append_to_file("repository/users.dat", contents=users_dat_content)
        self.create_folder("repository/default")
        project.set_emproject(EMProject(self.get_root()))

        return project.get_emproject()

    def _setup_dbconnector(self):
        conn_details = {
            "database_host": "localhost",
            "database_user": "FP8_HFR2_DEV_AD",
            "database_pass": "FP8_HFR2_DEV_ADkk",
            "database_name": "XEPDB1",
            "database_port": "1521",
            "database_type": "oracle",
        }
        self.db_connector.with_connection_details(**conn_details)

        return conn_details

    def get_root(self):

        return self._default_root

    def append_to_config(self, contents=None, lines=None, namevalue_pairs=None):
        self.append_to_file(
            "work/config/show-config-txt/localdev-localhost-ad.txt",
            contents=contents,
            lines=lines,
            namevalue_pairs=namevalue_pairs,
        )

    def append_to_file(
        self, relativepath, contents=None, lines=None, namevalue_pairs=None
    ):
        if not self.realpath(relativepath).exists():
            self.touch_path(relativepath)
        finalpath = self.realpath(relativepath)

        contents = self._get_content(contents, lines, namevalue_pairs)
        with finalpath.open("a") as f:
            f.write(contents)

        return finalpath

    def touch_path(self, path):
        finalpath = self.realpath(path)
        os.makedirs(os.path.dirname(finalpath), exist_ok=True)
        finalpath.touch()

        return finalpath

    def _get_content(self, contents, lines, namevalue_pairs):
        if namevalue_pairs:
            lines = self._convert_to_lines(namevalue_pairs)

        if lines:
            contents = "\n".join(lines)

        return contents

    def _convert_to_lines(self, namevalue_pairs):
        lines = []

        for key, value in namevalue_pairs.items():
            lines.append(key.replace("_", ".") + "=" + value)

        return lines

    def realpath(self, relativepath):
        return self._default_root / relativepath

    def create_folder(self, relativepath):
        os.makedirs(self.realpath(relativepath), exist_ok=True)
