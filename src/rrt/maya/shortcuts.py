import os
from pymel.core import *

def scene_is_dirty():
    """Checks to see if the scene has unsaved changes"""
    return mel.eval('file -q -amf')

def get_job_type():
    """Determine if we are using renderman or maya software"""
    if SCENE.defaultRenderGlobals.currentRenderer.get() == 'renderMan':
        return 'maya_render_rman'
    return 'maya_render_sw'
 
def get_scene_name():
    """Returns the filename (no extension) of the current scene"""
    return os.path.splitext(os.path.basename(sceneName()))[0]

def get_frame_range():
    """Returns a tuple of start and end frame numbers"""
    return (int(SCENE.defaultRenderGlobals.startFrame.get()), int(SCENE.defaultRenderGlobals.endFrame.get()))