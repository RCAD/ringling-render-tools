"""
Node Prep/Release script entry points for jobs ran with `Render.exe -r rman ...`
"""

from rrt.hpc.maya.sw import prep as sw_prep, release as sw_release
"""
Right now, we don't have any renderman specific tasks to execute, but we do
need to make sure all the maya.sw stuff happens regardless.
"""
def prep():
    sw_prep()

def release():
    sw_release()