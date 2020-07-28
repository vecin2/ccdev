from nubia import argument, command, context
from termcolor import cprint

import emtask.ced.tasks as ced_task
from emtask.ced.tool import MultiRootCED


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
    ced = MultiRootCED(
        "/mnt/c/em/projects/fp8_hfr2/repository/default",
        "/mnt/c/em/products/agent-desktop_15.3-FP8-HFR2_5.8.2/repository/default",
    )
    ced.open(process_to_wrap).wrapper(wrapper_path).save()
