import os
from pathlib import Path

import emtask
from emtask import project
from emtask.project import EMProject

testfolder = Path(os.path.dirname(emtask.__file__)) / ".testproject"


def create_file(path, contents=None, lines=None):
    if lines:
        contents = "\n".join(lines)
    finalpath = fullpath(path)
    os.makedirs(os.path.dirname(finalpath), exist_ok=True)
    with open(finalpath, "w+") as f:
        f.write(contents)

    return finalpath


def fullpath(relativepath):
    return testfolder / relativepath


def sample_project():
    return SampleProjectBuilder()


class SampleProjectBuilder(object):
    def build(self):
        lines = [
            "database.host=localhost",
            "database.user=FP8_HFR2_DEV_AD",
            "database.pass=FP8_HFR2_DEV_AD",
            "database.name=XEPDB1",
            "database.port=1521",
            "database.type=oracle",
        ]
        create_file(
            "work/config/show-config-txt/localdev-localhost-ad.txt", lines=lines
        )
        root = testfolder
        project.set_emproject(EMProject(root))

        return project.get_emproject()
