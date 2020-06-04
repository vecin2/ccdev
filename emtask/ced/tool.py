import os
from pathlib import Path

from emtask.ced import cedobject_factory


class CED(object):
    """Implementents actions similar to those that can be carried with CED"""

    def __init__(self, project_root):
        self.root = project_root

    def new_process(self, path):
        return cedobject_factory.make_process(self.root, path)

    def open(self, path):
        if self.get_realpath(path):
            return cedobject_factory.parse(self, path)

    def get_realpath(self, resource_path):
        return self.root / Path(resource_path.replace(".", os.sep) + ".xml")


class MultiRootCED(object):
    def __init__(self, project_root, product_root):
        self.project_ced = CED(project_root)
        self.product_ced = CED(product_root)
        self.root = project_root

    def new_process(self, path):
        return self.project_ced.new_process(path)

    def open(self, path):
        if self.get_realpath(path).exists():
            return self.project_ced.open(path)
        else:
            return self.product_ced.open(path)

    def get_realpath(self, resource_path):
        return self.project_ced.get_realpath(resource_path)
