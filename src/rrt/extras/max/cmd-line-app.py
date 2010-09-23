import datetime
import getpass
import os
import re
import string
import sys
import rrt
from rrt.settings import JOB_LOGS_UNC
from rrt.filesystem import get_share

# path to python submit bat
HPC_SPOOL_BIN = r'C:\Ringling\HPC\bin\hpc-spool.bat' 

JOB_SCRIPT_DIR = os.path.join('D:\\', 'hpc', getpass.getuser(), 'scripts')

OUT_UNC = r'\\chome\coutput'

INI_TEMPLATE = string.Template("""# Created for $user on $date by $version
renderer = $job_type
name = $job_name
project = $project_path
output = $output_path
scene = $scene_path
logs = $logs
start = $start
end = $end
step = $step
uuid = $uuid
net_drive = $net_drive
net_share = $net_share
""")

def getUuid():
    now = datetime.datetime.now()
    date = []
    date.append(re.sub('[%s]'% re.escape(' -:'),'', str(now).split('.')[0]))
    date.append(str(now))
    return date
    
def writeIni(content, uuid, name):
    if not os.path.isdir(JOB_SCRIPT_DIR):
        os.makedirs(JOB_SCRIPT_DIR)
    file_path = JOB_SCRIPT_DIR+'\\'+uuid+'_'+name+'.ini'
    with open(file_path,'w+b') as fh:
        fh.write(content)
    return file_path


"""
Main now, will probably change it once integration of 
the rest of the app starts to come up
"""
def main():
    # checks for command line arguments.
    # sys.argv[] = {python call, .zip, title, frame start, frame end, step}
    if len(sys.argv) != 6:
        sys.exit(2)
    
    _dates = getUuid()
    _uuid = _dates[0]
    _zipFilePath = sys.argv[1]
    
    vars = {
        'user':getpass.getuser(),
        'date':_dates[1],
        'version':rrt.get_version(),
        'job_type':"max",
        'job_name':sys.argv[2],
        'project_path':_zipFilePath[0:_zipFilePath.rfind('\\')],
        'output_path':os.path.join(OUT_UNC, getpass.getuser(), _uuid, sys.argv[2]+'.jpg'),
        'scene_path':_zipFilePath, #looking into the zipfile?
        'logs':os.path.join(JOB_LOGS_UNC, getpass.getuser(), _uuid, sys.argv[2]+'.*.txt'),
        'start':sys.argv[3],
        'end':sys.argv[4],
        'step':sys.argv[5],
        'uuid':_uuid,
        'net_drive':_zipFilePath.split("\\")[0],
        'net_share':get_share(_zipFilePath),
    }
    
    iniFile = writeIni(INI_TEMPLATE.substitute(vars), _uuid, sys.argv[2])
    
    

if __name__ == '__main__':
    main()