from ringling.render import SubmitGui, get_version
import maya.OpenMayaMPx as OpenMayaMPx
kPluginCmdName="hpcSubmit"

class scriptedCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
    
    def doIt(self,args):
        # build the gui and display
        gui = SubmitGui()
        gui.show()
        
def cmdCreator():
    # Create the command
    return OpenMayaMPx.asMPxPtr( scriptedCommand() )

# I believe this method only needs to exist if the scripted command takes args
# since I think it's used to generate the response of MEL's "help commandName"
# Syntax creator
#    def syntaxCreator():
#        syntax = OpenMaya.MSyntax()
#        return syntax

# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Ringling", get_version(), "Any")
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
        raise
# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )
        raise
