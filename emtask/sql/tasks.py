from sql_gen.commands import CreateSQLTaskCommand

def rewire_verb(**kwargs):
    _run_template('rewire_verb.sql',**kwargs)

def _run_template(*args,**kwargs):
    template_values=dict(**kwargs)
    CreateSQLTaskCommand(template_name=args[0],
                         run_once=True,
                         template_values= template_values
                        ).run()

