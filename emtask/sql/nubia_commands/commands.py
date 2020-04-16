from termcolor import cprint
from nubia import command, argument, context
from sql_gen.commands import RunSQLCommand

templates=["test", "toast", "toad"]
#@argument("template", description="Pick a style", choices=templates)
@command
def run_sql():
    """
    This will generate an sql script from a template and will run it on db
    """
    ctx = context.get_context()
    cprint("Verbose? {}".format(ctx.args.verbose), "yellow")
    return RunSQLCommand().run()

    # optional, by default it's 0
    return 0

