@echo off
rem = """-*-Python-*- script
python -x "%~f0" %*
goto exit

"""
from runtasks.cmdline import run
run()

DosExitLabel = """
:exit
rem """
