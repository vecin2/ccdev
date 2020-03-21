
from termcolor import cprint
from nubia import command, argument, context


@command
def hotupdates():
    """
    This will configure the ced for hotupdates
    """
    ctx = context.get_context()
    cprint("Verbose? {}".format(ctx.verbose), "yellow")

    # optional, by default it's 0
    return 0

