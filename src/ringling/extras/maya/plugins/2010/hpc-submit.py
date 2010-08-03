import maya.OpenMayaMPx as OpenMayaMPx
from ringling import get_version
from ringling.maya.gui import SubmitGui

kPluginCmdName="hpcSubmit"

class scriptedCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
    
    def doIt(self,args):
        SubmitGui().new_window()
        
def cmdCreator():
    return OpenMayaMPx.asMPxPtr(scriptedCommand())


# Runs when plug-in is enabled
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Ringling College", get_version(), "Any")
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
        raise
# Runs when plug-in is disabled
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    """
    Note: it's SubmitGui.destroy() not SubmitGui().destroy() since it's static.
    """
    SubmitGui.destroy() 
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )
        raise
