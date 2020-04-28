#!/usr/bin/env python3

import sys
from nubia import Nubia, Options
import  emtask.sql.nubia_commands
import  emtask.ced.nubia_commands
import colorama

colorama.init()

def main():
    shell = Nubia(
        name="nubia_example",
        command_pkgs=[emtask.sql.nubia_commands,
                      emtask.ced.nubia_commands
                      ],
        options=Options(persistent_history=False)
    )
    sys.exit(shell.run())


if __name__ == "__main__":
    main()
