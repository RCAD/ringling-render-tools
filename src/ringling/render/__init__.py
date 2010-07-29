"""
This "render" package will most likely be removed due to the vague nature of the
name.  This move was motivated by the desire to prevent pymel from being loaded
before it is actually needed.

The contents have here by been moved to ringling.maya.gui and 
ringling.maya.shortcuts.

This import is for backwards compatibility (until the hpc-submit.py maya plugin 
is updated to use the full import path.
"""
from ringling.maya.gui import SubmitGui # backwards compatibility import
