"""
Node Prep/Release script entry points for jobs ran with `3dsmaxcmd.exe ...`
"""
from rrt.hpc import env
from rrt.hpc.scripts import LOG
ENV = env()
import os

"""
>>> import zipfile
>>> f = 'Z:\\MAX\\test.zip'
>>> z = zipfile.ZipFile
>>> z = zipfile.ZipFile(f)
>>> z.namelist()
['test.max', 'MAXFILES.TXT']
>>> node_project = "D:\\hpc\\maxtest\\"
>>> import os
>>> os.makedirs(node_project)
>>> os.chdir(node_project)
>>> z.extractall()
>>> os.listdir(node_project)
['MAXFILES.TXT', 'test.max']
>>> 
"""

def prep():
    pass
def release():
    pass