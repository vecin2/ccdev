from emtask.sql.tasks import RewireVerbSQLTask


def rewire_verb(current_path=None, new_path=None):
    """The most common way to rewire a verb is by selecting the current path"""

    rewire_verb_task = RewireVerbTask()
    rewire_verb_task.rewire_from_current_path(current_path, new_path)


class RewireVerbTask(object):
    def __init__(self):
        self.sqltask = RewireVerbSQLTask()

    def rewire_from_current_path(self, current_path, new_path):
        self.sqltask.rewire_verb(current_path, new_path)
