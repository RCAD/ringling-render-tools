"""
Blessed  file system locations
"""

import os
# location to dump jobspec files
JOBSPEC_DIR = os.path.join('D:\\', 'hpc', getpass.getuser(), 'scripts')

# abspath because we can't count on it being in the PATH
HPC_SPOOL_BIN = r'C:\Ringling\HPC\bin\hpc-spool.bat'

JOB_LOGS_UNC = "\\\\clogs\\clogs"
JOB_OUTPUT_UNC = "\\\\coutput\\coutput"

if os.getenv('RRT_USE_DESMOND', False):
    SPOOL_UNC = "\\\\desmond\\spool" # note the native \ style separators
    JOB_LOGS_UNC = "\\\\desmond\\spool\\logs"
    JOB_OUTPUT_UNC = "\\\\desmond\\spool\\output"
