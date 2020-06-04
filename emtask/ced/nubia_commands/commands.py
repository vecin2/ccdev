from nubia import argument, command, context

import emtask.ced.tasks as ced_task
from emtask.ced.tool import CED


@command
@argument(
    "wrapper_path", description="dot separated path where the wrapper will be created",
)
@argument(
    "process_to_wrap",
    description="dot separated path (e.g CoreContact.Implementation.Verbs.View)",
)
def wrap_process(process_to_wrap: str, wrapper_path: str = None):
    """"""
    ced = CED("/mnt/c/em/projects/fp8_hfr2/repository/default")
    ced.open(process_to_wrap).wrapper(wrapper_path)


@command
@argument(
    "current_path",
    description="e.g. CoreEntities.Implementation.Customer.Verbs.InlineSearch",
)
@argument("new_path", description="This is optional, it prefixes project prefix")
def rewire_verb(current_path: str, new_path: str = None):
    """
    It changes the verb repository path on db and the relevant CED process
    """
    # ctx = context.get_context()
    # cprint("Verbose? {}".format(ctx.args.verbose), "yellow")
    ced_task.rewire_verb(current_path=current_path, new_path=new_path)

    return 0  # optional, by default it's 0


@command
@argument(
    "process_to_wrap",
    description="e.g. CoreEntities.Implementation.Customer.Verbs.InlineSearch",
)
@argument("wrapper_path", description="This is optional, it prefixes project prefix")
def wrap_process(process_to_wrap: str, wrapper_path: str = None):
    """
    It changes the verb repository path on db and the relevant CED process
    """
    ced = CED("/mnt/c/em/projects/fp8_hfr2/repository/default")
    ced.open(process_to_wrap).wrapper(wrapper_path).save()
