# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need fine tuning.
main_script = "main.py"
includes = ["matplotlib.backends.backend_qt4agg"]
excludes = ["tkinter"]
base = "Console"  # Win32GUI or Console
build_dir = "build"


# Call setup
setup(  
    name = "<unnamed>",
    version = "1.0",
    description = "Python Application!",
    options = {
        "build_exe": {
            "build_exe": build_dir,
            "includes": includes,
            "excludes": excludes,
            "compressed": True,
           }
        },
    executables = [Executable(main_script, base=base, targetDir=build_dir)]
    )