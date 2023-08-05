
@echo off
@echo SCRIPT: windows_prefix
if "%1"=="" goto default_value_python:
if "%1"=="default" goto default_value_python:
set pythonexe=%1
goto start_script:

:default_value_python:
set pythonexe=c:\Python36_x64\python

@echo ~SET pythonexe=%pythonexe%

:start_script:
set current=%~dp0
if EXIST %current%setup.py goto current_is_setup:
set current=%current%..\
cd ..
if EXIST %current%setup.py goto current_is_setup:
@echo Unable to find %current%setup.py
exit /b 1

:current_is_setup:
@echo ~SET current=%current%


set PYTHONPATH=%PYTHONPATH%;%current%src;%current%\..\pyquickhelper\src;%current%\..\pyensae\src;%current%\..\mlstatpy\src;%current%\..\teachpyx\src;%current%\..\jyquickhelper\src;%current%\..\pymmails\src;%current%\..\ensae_teaching_cs\src
%pythonexe% -u -c "from pyquickhelper.loghelper import fLOG;fLOG(OutputPrint=True);from jupytalk.mokadi import gui_mokadi;gui_mokadi(fLOG)"