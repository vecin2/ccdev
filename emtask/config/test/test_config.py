from pathlib import Path

import pytest
from nubia import command


@command
def config_hotupdates_attachonstart():
    block = "hotupdates.attachonstart=true"
    filepath = "config/tooling/ced/ced.properties"
    blockinfile(filepath, block)


# from em.config.files import blockinfile
# def test_hotupdate_attachonstart_ced(project):
#    shell = TestShell(commands=[config_hotupdates_attachonstart])
#    shell.run_interactive_line("test_shell config_hotupdates_attachonstart")
#
#    ced_properties_file= project.get_file(filepath=filepath)
#    assert true == ced_properties_file.contains_once(block)
class TestProject(object):

    """Allows to test project files on the filesystem"""

    def __init__(self, root):
        self.root = root

    def get_file(self, filepath=None):
        return ProjectFile(filepath)


class ProjectFile(object):

    """Provides base functionality for files within project"""

    def __init__(self, filepath):
        self.filepath = filepath

    def contains_once(self, block):
        with open("example.txt") as f:
            if "blabla" in f.read():
                return True


@pytest.fixture
def project(capsys):
    project = TestProject("/tmp/emProject")
    yield project


@pytest.mark.skip
def test_some(project):
    block = "hotupdates.attachonstart=true"
    filepath = "config/tooling/ced/ced.properties"
    ced_properties_path = project.get_path(filepath=filepath)
    assert ced_properties_file.contains_once(block)
