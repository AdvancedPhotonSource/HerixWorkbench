#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.

This file is used to create an executable of the program.
"""
import sys
from cx_Freeze import Executable, setup

base = None
if sys.platform == "win32":
        base = "Win32GUI"

build_exe_options = {"packages": ["os"], }

setup(
    name="Herix Workbench",
    version="0.0.1",
    options={"build_exe": build_exe_options,},
    executables=[Executable("HerixWorkbench/workbenchWindow.py", base=base)]
)