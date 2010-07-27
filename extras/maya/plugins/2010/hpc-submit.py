import maya.OpenMayaMPx as OpenMayaMPx
import ringling
from ringling.render import SubmitGui

GUI = None

kPluginCmdName="hpcSubmit"

class scriptedCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
    
    def doIt(self,args):
        global GUI
        GUI = SubmitGui()
        GUI.new_window()
        
def cmdCreator():
    return OpenMayaMPx.asMPxPtr(scriptedCommand())


# Runs when plug-in is enabled
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Ringling College", ringling.get_version(), "Any")
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
        raise
# Runs when plug-in is disabled
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    global GUI
    try: GUI.window.delete()
    except: pass
    GUI = None
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )
        raise
