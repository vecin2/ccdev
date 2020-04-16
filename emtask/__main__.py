#!/usr/bin/env python3

import sys
from nubia import Nubia, Options
#from nubia_plugin import NubiaExamplePlugin
import example.commands
import  emtask.sql.nubia_commands

def main():
    #plugin = NubiaExamplePlugin()
    shell = Nubia(
        name="nubia_example",
        command_pkgs=[emtask.sql.nubia_commands],
        options=Options(persistent_history=False)
    )
    sys.exit(shell.run())


if __name__ == "__main__":
    main()
