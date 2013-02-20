"""
Blessed  file system locations

build commands:
X:\Program Files (x86)\LightTPD\htdocs\dist\beta\ringling_render_tools-0.0.5b-20-g4540\ringling_render_tools-0.0.5b-5-g4540>C:\Python26\Lib\site-packages\PyQt4\bin\pyuic4.bat .\src\rrt\md\ui\submit.ui --output=.\src\rrt\md\ui\submit.py

X:\Program Files (x86)\LightTPD\htdocs\dist\beta\ringling_render_tools-0.0.5b-20-g4540\ringling_render_tools-0.0.5b-5-g4540>python setup.py sdist

"""

import os, getpass
# location to dump jobspec files
JOBSPEC_DIR = os.path.join('D:\\', 'hpc', 'jspec', getpass.getuser())

# abspath because we can't count on it being in the PATH
HPC_SPOOL_BIN = r'C:\Ringling\HPC\bin\hpc-spool.bat'

HEAD_NODES = ['Alpha', 'Omega']

# TODO: replace these "constants" with functions that generate a prefix based on HEAD_NODE
JOB_LOGS_UNC = "\\\\hpc\\results"
JOB_OUTPUT_UNC = "\\\\hpc\\results"
JOB_STATS_UNC = "\\\\hpc\\results"
