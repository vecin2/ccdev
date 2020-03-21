#!/usr/bin/env python3

import sys
from nubia import Nubia, Options
#from nubia_plugin import NubiaExamplePlugin
import example.commands
import em.config.commands
import em.sql.commands

if __name__ == "__main__":
    #plugin = NubiaExamplePlugin()
    shell = Nubia(
        name="nubia_example",
        command_pkgs=[em.config.commands,em.sql.commands],
        #command_pkgs=example.commands,
        options=Options(persistent_history=False),
    )
    sys.exit(shell.run())
