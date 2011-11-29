"""
Blessed  file system locations
"""

import os, getpass
# location to dump jobspec files
JOBSPEC_DIR = os.path.join('D:\\', 'hpc', 'jspec', getpass.getuser())

# abspath because we can't count on it being in the PATH
HPC_SPOOL_BIN = r'C:\Ringling\HPC\bin\hpc-spool.bat'

HEAD_NODES = ['testcluster', 'idmasternode']

# TODO: replace these "constants" with functions that generate a prefix based on HEAD_NODE
JOB_LOGS_UNC = "\\\\hpc\\results"
JOB_OUTPUT_UNC = "\\\\hpc\\results"
