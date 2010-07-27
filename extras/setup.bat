mkdir C:\Ringling\Python26\Lib\site-packages
mkdir C:\Ringling\Python26\Scripts
mkdir C:\Ringling\HPC\extras
robocopy %CD% C:\Ringling\HPC\extras /S
#setx PYTHONPATH C:\Ringling\Python26\Lib\site-packages /M
#setx MAYA_PLUG_IN_PATH C:\Ringling\HPC\extras\maya\plugins\2010;C:\Program Files\Pixar\RenderManStudio-2.0.2-maya2010\ /M
#setx MAYA_SCRIPT_PATH C:\Ringling\HPC\extras\maya\shelves\;%MAYA_SCRIPT_PATH% /M
#setx MAYA_SHELF_PATH C:\Ringling\HPC\extras\maya\shelves\;%MAYA_SHELF_PATH% /M
#setx HEAD_NODE sgi0node1 /M

