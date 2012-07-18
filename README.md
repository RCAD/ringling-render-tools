Overview
========

*Disclaimer:* 
*This document (and package) has been designed with our (Ringling's) needs in mind.*
*The installation/deployment is outrageously specific to our architecture and overall infrastructure.*
*Use with caution!*

`ringling-render-tools` is a suite of python packages and scripts (under the **rrt** namespace) to ease the submission of *Maya* and *3dsmax* render jobs to a Windows HPC cluster.


Definitions
-----------

* Compute Node: a node that will be doing rendering (usually, but not always, running windows hpc).
* Submit Client: a workstation that can submit new jobs to a hpc cluster - these workstations can also be compute nodes.
* hpc-spool: An IronPython script that parses a short ini-style file to submit a job to a hpc cluster.
* ringling-render-tools (**rrt**): This python package (provides modules and scripts that deal with an assortment of render tasks).
* hpcSubmit: A mel command (provided by our hpc-submit.py maya plugin) that presents the submission UI to the user. It is really just a wrapper for code inside `ringling-render-tools`.


Compute Node Installation Notes
===============================

Python Installation
-------------------
**new in rc17** with the move to maya 2011, we're now using the matching python
version: *2.6.4*

1. Download and install Python 2.6.4 (x64) <http://www.python.org/ftp/python/2.6.4/python-2.6.4.amd64.msi>
1. Add the following directories to the `PATH`: `C:\Python26;C:\Ringling\Python26\Scripts;C:\Python26\Scripts` *(These need to be at the front of the list - - and absolutely need to be before the path to Maya's bin dir)*
1. Add a new environment variable called `PYTHONPATH`: `C:\Ringling\Python26\Lib\site-packages`
1. Verify these steps completed properly by starting a fresh cmd (so the env is updated)

Create the Ringling Python dirs by running at a cmd prompt: 

    mkdir C:\Ringling\Python26\Lib\site-packages & mkdir C:\Ringling\Python26\Scripts & mkdir C:\Ringling\Python26\Data

Verify the python installation:

    python --version
    Python 2.6.4

To verify the `PYTHONPATH` was set correctly:

    python -c "import sys; print 'Ringling' in ''.join(sys.path)"
    True

Setuptools Installation
-----------------------

1. Download and extract <http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz#md5=7df2a529a074f613b509fb44feefe74e>
1. Once extracted, you should see a file called setup.py -- shift-right-click in the window and do open command prompt here. Then type:

    python setup.py install --prefix C:\Ringling\Python26

To confirm this step worked:

    python -c "import setuptools;print setuptools.__version__"
    0.6c11

Setup Render command line tools
-------------------------------

Ensure that the Maya bin and 3dsmax directories are in the PATH (probably place 
these at the back): `C:\Program Files\Autodesk\Maya2010\bin;C:\Program Files\Autodesk\3ds Max Design 2010`

To confirm:

    mayabatch -v
    Maya 2010 x64, Cut Number 200907280308

and...

    3dsmaxcmd foo
    7/29/2010 10:14:05 AM; Error opening scene file: "D:\foo"

Deploy the ringling-render-tools python package
-----------------------------------------------

1. Add C:\Ringling\HPC\maya\plugins to the `MAYA_PLUG_IN_PATH` environment variable
1. Add C:\Ringling\HPC\maya\scripts to both `MAYA_SCRIPT_PATH` and `MAYA_SHELF_PATH`

Run the following:

    easy_install -U --prefix C:\Ringling\Python26 ringling-render-tools
    

*Since this package is not available on pypi or any other index, you'll need to supply a location to download from.*
*I have a dist directory where I'm dumping developemnt snapshots here on campus, so contact me for the current location.*

*The usage would be like:*
    
    easy_install -U --prefix C:\Ringling\Python26 --find-links <OUR DIST LOCATION> ringling-render-tools

> **New in 0.0.1rc15**
> The code that drives the maya plugin relies on `pymel`.  **Maya 2010** needs 
> `pymel` to be installed, whereas in **Maya 2011**, it is bundled with `mayapy`.
> 
> I've added pymel as an **optional dependency**, which means installing 
> ringling-render-tools by default *will not* install pymel for you.
> If you are installing rrt for Maya <2011, then use `ringling-render-tools[pymel]`
> instead of just `ringling-render-tools` on the `easy_install` command line. Like so:

	easy_install -U --prefix C:\Ringling\Python26 --find-links <OUR DIST LOCATION> ringling-render-tools[pymel]

If it finished cleanly, the following should work:

    mayapy -c "import pymel;print pymel.__version__"
    1.0.2
    
    mayapy -c "import rrt;print rrt.get_version()"
    rrt 0.0.1
    
    python -c "import rrt;print rrt.get_version()"
    rrt 0.0.1


Submit Client Installation Notes
================================

General Notes
-------------

The client will follow the same procedure as the compute node, but with one 
addition: the **"extras"**.

The extras include:

* the hpc-spool script(s)
* the hpc-submit maya plugin
* a *Ringling* maya shelf with a button to load/launch the plugin

All of this stuff should *just work* once deployed, so long as the environment 
variables mentioned in the steps above have all been set correctly.

The `hpc-spool` application is built with the dot net HPC library, and requires 
dot net 4, and IronPython.

If they are not installed yet, get them and install them:

> <http://www.microsoft.com/downloads/details.aspx?FamilyID=9cfb2d51-5ff4-4491-b0e5-b386f32c0992&displaylang=en> (dot net 4)
 
> <http://ironpython.codeplex.com/releases/view/36280#DownloadId=116507> (IronPython: must be version 2.6.1 for dot net 4)

Once dot net 4 and IronPython are installed run `hpc-deploy-extras` in a cmd prompt.

`hpc-deploy-extras` is a command that is a part of the ringling-render-tools 
package. 
It uncompresses files inside the package and copies them to `C:\Ringling\HPC`. 
Verify the installation by opening a cmd prompt and typing the following:

    C:\Ringling\HPC\bin\hpc-spool.bat

Output should look like:

    Error!
    Must specify an ini file.
    Exiting...

If you get an error saying `file not found`, or something like that, it probably
means you don't have IronPython installed.  The batch file passes arguments 
directly to our scripts, called with the IronPython interpreter - if the 
interpreter not there, you'll see an error like that.

If instead, you get an error about dot net, a reboot might be required. 
Reboot the machine and run the command again. If your output still doesn't 
match **find me**.

3dsmax Notes
-------------

The submission tool for 3dsmax is built with `PyQt4` (which needs to be installed).
I built the UI for the tool with `PyQt 4.7.7` (built against `Qt 4.6.2`).  

Since this package needs to be built from source, I've prepared a binary 
installer for win x64 (to make our lives easier).  The installer has been 
modified (I think it was made for the 32bit version of the package), so it's a 
little buggy.  Press on with the installation and ignore it when it says 
it can't find python 2.6 installed on the system.  Also make sure you install it
using the default paths - we want PyQt installed with the `C:\Python26` prefix 
**not** the `C:\Ringling\Python26` prefix we use for most of our custom scripts.

To confirm the install worked correctly, run `hpc-submit-max.exe` to launch the 
tool (requires the `rrt` package to be installed already). 

Client Configuration
--------------------
`hpc-spool` will not function if the environment variable `HEAD_NODE` has not 
been set to a **windows name**, **ip**, or **dns** name of a valid *Windows HPC 
cluster head node*.

> **New in 0.0.5**
>
> `HEAD_NODE` is now set by the submission app before it passes the jobspec file 
> to `hpc-spool`, and no longer needs to be set system wide.
> It will need to be set manually if you plan to call `hpc-spool` directly. 