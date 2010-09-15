"""
Blessed  file system locations
"""

import os

JOB_LOGS_UNC = "\\\\clogs\\clogs"
JOB_OUTPUT_UNC = "\\\\coutput\\coutput"

if os.getenv('RRT_USE_DESMOND', False):
    SPOOL_UNC = "\\\\desmond\\spool" # note the native \ style separators
    JOB_LOGS_UNC = "\\\\desmond\\spool\\logs"
    JOB_OUTPUT_UNC = "\\\\desmond\\spool\\output"
