import os
from subprocess import Popen, PIPE
# Blessed  file system locations
def __get_homeshare(letter):
    try:
        p = Popen(['net', 'use', letter], stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[1].split()[2]
        return line.strip()
    except Exception, e:
        raise e

SPOOL_LETTER = "Z:"
SPOOL_UNC = __get_homeshare(SPOOL_LETTER)

JOB_LOGS_UNC = "\\\\clogs\\clogs"
JOB_OUTPUT_UNC = "\\\\coutput\\coutput"

if os.getenv('RRT_USE_DESMOND', False):
    SPOOL_UNC = "\\\\desmond\\spool" # note the native \ style separators
    JOB_LOGS_UNC = "\\\\desmond\\spool\\logs"
    JOB_OUTPUT_UNC = "\\\\desmond\\spool\\output"