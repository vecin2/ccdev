from nubia import argument, command, context

import emtask.sql.tasks as sqltask


@command
@argument(
    "current_path",
    description="e.g. CoreEntities.Implementation.Customer.Verbs.InlineSearch",
)
@argument("new_path", description="This is optional, it prefixes project prefix")
def rewire_verb(current_path: str, new_path: str = None):
    """
    It changes the verb repository path while creating a new process desc ref
    """
    # ctx = context.get_context()
    # cprint("Verbose? {}".format(ctx.args.verbose), "yellow")
    sqltask.rewire_verb(current_path=current_path, new_path=new_path)

    return 0  # optional, by default it's 0
