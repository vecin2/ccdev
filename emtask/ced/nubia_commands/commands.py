from termcolor import cprint
from nubia import command, argument, context
from emtask.sql.tasks import rewire_verb

templates=["test", "toast", "toad"]
#@argument("template", description="Pick a style", choices=templates)
@command
def override_verb():
    """
    This will generate an sql script from a template and will run it on db
    """
    ctx = context.get_context()
    cprint("Verbose? {}".format(ctx.args.verbose), "yellow")
    rewire_verb(entity_def_id="Customer",
                verb_name="inlineCreate",
                new_pd_path="a.path.to.create.customer"
               )
    return 0# optional, by default it's 0


