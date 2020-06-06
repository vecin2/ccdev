from emtask.sql.tasks import RewireVerbSQLTask, VerbDB


def rewire_verb(current_path=None, new_path=None):
    """The most common way to rewire a verb is by selecting the current path"""

    rewire_verb_task = RewireVerbTask()
    rewire_verb_task.rewire_from_current_path(current_path, new_path)


class RewireVerbTask(object):
    def __init__(self):
        self.sqltask = RewireVerbSQLTask()

    def rewire_from_current_path(self, current_path, new_path):
        verbs = VerbDB().fetch(repository_path=current_path)
        self.sqltask.create_rewire_verb_template(
            verbs[0], new_path or self._extension_path(current_path)
        )

    def _extension_path(self, otb_process_path):
        return "TODO implement"


class GenerateProcessWrapper(object):
    """docstring for ClassName"""

    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg
