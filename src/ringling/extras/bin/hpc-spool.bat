@echo off
:: Figure out the location of this file
set scriptdir=%~dp0
:: script to proxy
set spoolscript="%scriptdir%hpc-spool-script.py"
:: reset PYTHONHOME to keep things fresh
if defined PYTHONHOME (
set OLD_PYTHONHOME=%PYTHONHOME%
set PYTHONHOME=
)
set ipybin="C:\Program Files (x86)\IronPython 2.6 for .NET 4.0\ipy.exe"
:: do it
%ipybin% %spoolscript% %*
:: Restore the PYTHONHOME and PYTHONPATH if it was deleted.
if defined OLD_PYTHONHOME (
set PYTHONHOME=%OLD_PYTHONHOME%
)

