from nubia import argument, command, context
from termcolor import cprint


@command
@argument(
    "sql_release_name",
    description="New folders are created under each sql module, "
    + "e.g Pacificorp_R_0_0_4",
    choices=["Pacificorp_R_0_0_4"],
)
def post_upgrade(sql_release_name: str):
    """
    Creates folders with new release name and updates patches version
    """
    ctx = context.get_context()
    cprint("Verbose? {}".format(ctx.args.verbose), "yellow")

    return 0  # optional, by default it's 0
