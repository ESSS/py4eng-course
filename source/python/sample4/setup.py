import sys
from cx_Freeze import setup, Executable


# Exclude Tkinter since we are using Qt
build_exe_options = {"excludes": ["Tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
if sys.platform == "win32":
    base = "Win32GUI"
else:
    base = None

setup(name = "guifoo",
      version = "0.1",
      description = "My GUI application!",
      options = {"build_exe": build_exe_options},
      executables = [Executable("test.py", base=base)])
      