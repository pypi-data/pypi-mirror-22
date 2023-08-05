
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
@echo ~SET current=%current%
set PYTHONPATH=%current%\src

%pythonexe% -u %current%..\setup.py update_grammars MokadiGrammar_fr.g4
if %errorlevel% neq 0 exit /b %errorlevel%