#!/usr/bin/env python3

import sys

import colorama
from nubia import Nubia, Options

import emtask.ced.nubia_commands
import emtask.misc
import emtask.sql.nubia_commands

colorama.init()  # allow termcolor to show colors on windows


def main():
    shell = Nubia(
        name="nubia_example",
        command_pkgs=[
            emtask.sql.nubia_commands,
            emtask.ced.nubia_commands,
            emtask.misc,
        ],
        options=Options(persistent_history=True),
    )
    sys.exit(shell.run())


if __name__ == "__main__":
    main()
