"""
Node Prep/Release script entry points for jobs ran with `Render.exe -r rman ...`
"""
import os, sys, shutil, platform, datetime, rrt
from rrt.hpc.maya.sw import prep as sw_prep, release as sw_release
from rrt.hpc import env
from rrt import RinglingException, get_log

LOG = get_log(platform.uname()[1], True)

"""
Right now, we have one renderman specific tasks to execute, but we do
need to make sure all the maya.sw stuff happens regardless.
"""
def prep():    
    sw_prep()

def release():
    sw_release()