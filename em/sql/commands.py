from termcolor import cprint
from nubia import command, argument, context

templates=["test", "toast", "toad"]
@argument("template", description="Pick a style", choices=templates)
@command
def run_sql(template: str):
    """
    This will generate an sql script from a template and will run it on db
    """
    ctx = context.get_context()
    cprint("Verbose? {}".format(ctx.verbose), "yellow")

    # optional, by default it's 0
    return 0

