import os
from pathlib import Path

from emtask.ced import cedobject_factory


class CED(object):
    """Implementents actions similar to those that can be carried with CED"""

    def __init__(self, root):
        self.root = root

    def new_process(self, path):
        return cedobject_factory.make_process(self.root, path)

    def open(self, path):
        return cedobject_factory.parse(self, path)

    def get_realpath(self, resource_path):
        return self.root / Path(resource_path.replace(".", os.sep) + ".xml")
