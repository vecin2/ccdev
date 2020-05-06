
from termcolor import cprint
from nubia import command, argument, context
#from example.commands.nubia_plugin import NubiaExamplePlugin
#import example.nubia_plugin



@command
def hotupdates():
    """
    This will configure the ced for hotupdates
    """
    ctx = mypepe()
    cprint("Verbose? {}".format(ctx.args.verbose), "yellow")

    # optional, by default it's 0
    return 0

def mypepe():
    ctx = context.get_context()
    return ctx

