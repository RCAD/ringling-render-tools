from ringling.render import SubmitGui, get_version
import maya.OpenMayaMPx as OpenMayaMPx
kPluginCmdName="hpcSubmit"

GUI = None

class scriptedCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
    
    def doIt(self,args):
        global GUI
        GUI = None
        GUI = SubmitGui()
        
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
    try:
        global GUI
        del GUI
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )
        raise
