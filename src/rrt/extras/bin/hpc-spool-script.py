"""
The hpc-spool.bat file sets up the ipy interpreter then executes this script 
with any additional arguments -- you should not call this script directly!

This standalone script must be run with IronPython (ipy.exe) since it relies on
the Microsoft Hpc .Net assemblies. It will not work if you run it using the 
regular python interpreter. 
"""

import clr, sys, os, getpass

"""
The expected directory structure of this deployment is:
.../bin (this script and the bat file that calls it)
.../Lib (.Net assemblies for HPC)
"""

__ROOT__ = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0,os.path.abspath(os.path.join(__ROOT__,'..', 'Lib')))
clr.AddReferenceToFile("Microsoft.Hpc.Scheduler.dll")
clr.AddReferenceToFile("Microsoft.Hpc.Scheduler.Properties.dll")

from Microsoft.Hpc.Scheduler import *
from Microsoft.Hpc.Scheduler.Properties import *


class Spooler(object):
    RUNAS_USER = None;
    RUNAS_PASSWORD = None;
    
    @property
    def HeadNode(self):
        host = os.getenv("HEAD_NODE", None)
        if None == host: 
            print >> sys.stderr, "\nError!"
            print >> sys.stderr, "HEAD_NODE is null - please set HEAD_NODE."
            print >> sys.stderr, "Exiting..."
            sys.exit(1)
        return host.strip()

    #Looks like Render.exe doesn't like quotes around the remote paths...
    CMD_MAYA_RENDER_SW = "Render.exe -n {threads} -r sw -s * -e * -proj {node_project} -rd {output} {scene}"
    CMD_MAYA_RENDER_RMAN = "Render.exe -n {threads} -r rman -s * -e * -proj {node_project} -rd {output} {scene}"
    CMD_3DSMAX_RENDER = "3dsmaxcmd.exe -frames=*-* -workingFolder:{node_project} -workPath:{node_project} -o:{output} -showRFW:0 {scene}"
    # NODE_PATH = r"C:\Ringling\HPC\bin;C:\Python26;C:\Ringling\Python26\Scripts;C:\Python26\Scripts;C:\Program Files\Autodesk\Maya2010\bin;C:\Program Files\Autodesk\3ds Max Design 2010"
    _renderers = {
        "max": CMD_3DSMAX_RENDER, 
        "maya_render_rman": CMD_MAYA_RENDER_RMAN,
        "maya_render_sw": CMD_MAYA_RENDER_SW
    }
    
    _confFile = None
    
    _conf = {
        "renderer": None,
        "name": None,
        "project": None,
        "node_project": None,
        "output": None,
        "logs": None,
        "scene": None,
        "start": None,
        "end": None,
        "step": "1",
        "threads": "4"
    }

    def ParseConf(self, iniPath):
        if os.path.isfile(iniPath): 
            with open(iniPath, "rb") as iniFile:
                for strLine in iniFile.readlines():
                    strLine = strLine.strip().split('#')[0]
                    if (strLine and '=' in strLine):
                        parts = strLine.split('=')
                        key = parts[0].strip()
                        val = parts[1].strip()
                        self._conf[key] = val
        else: 
            raise RuntimeError("Unable to locate " + iniPath)

    def __init__(self, confFile):
        self._confFile = confFile
        self.ParseConf(self._confFile)
    
    def BuildTaskList(self, job):
        # this guy will need other methods to delegate to so we don't fork for each renderer available.
        render_task = job.CreateTask()
        
        user_dir = r"D:\hpc\%s" % getpass.getuser()
        self._conf["user_dir"] = user_dir

        node_project = user_dir + r"\jobs\%CCP_JOBID%"
        render_task.SetEnvironmentVariable("INIT_WD", node_project)
        self._conf["node_project"] = node_project

        #Main Render Task
        # basic info
        render_task.Name = "Render *"
        render_task.Type = TaskType.ParametricSweep

        #task iteration
        render_task.StartValue = int(self._conf["start"])
        render_task.EndValue = int(self._conf["end"])
        render_task.IncrementValue = int(self._conf["step"])

        # thread limits
        render_task.MinimumNumberOfCores = int(self._conf["threads"])
        render_task.MaximumNumberOfCores = int(self._conf["threads"])

        # log redirection
        render_task.StdErrFilePath = self._conf["logs"]
        render_task.StdOutFilePath = self._conf["logs"]

        # run the render command
        render_task.CommandLine = self._renderers[self._conf["renderer"]].format(**self._conf)

        # Setup Task
        setup_task = job.CreateTask()
        setup_task.Type = TaskType.NodePrep
        setup_task.Name = "Setup"
        setup_task.CommandLine = "cmd.exe /X /C hpc-node-prep"

        # TearDown Task
        cleanup_task = job.CreateTask()
        cleanup_task.Type = TaskType.NodeRelease
        cleanup_task.Name = "Cleanup"
        cleanup_task.CommandLine = "cmd.exe /X /C hpc-node-release"

        # Add Env Vars
        self.SetJobEnv(setup_task)
        self.SetJobEnv(render_task)
        self.SetJobEnv(cleanup_task)

        # Task Assignment
        job.AddTask(setup_task)
        job.AddTask(render_task)
        job.AddTask(cleanup_task)

    def SetJobEnv(self,task):
        task.SetEnvironmentVariable("MAYA_APP_DIR", self._conf["user_dir"])
        task.SetEnvironmentVariable("TEMP", self._conf["user_dir"])
        task.SetEnvironmentVariable("TMP", self._conf["user_dir"])        
        task.SetEnvironmentVariable("OWNER", getpass.getuser())
        task.SetEnvironmentVariable("USER_DIR", self._conf["user_dir"])
        task.SetEnvironmentVariable("NODE_PROJECT", self._conf["node_project"])
        # self override enables us to apply per-job dirmaps on maya jobs
        task.SetEnvironmentVariable("MAYA_SCRIPT_PATH", self._conf["node_project"]+ r"\scripts;"+os.getenv("MAYA_SCRIPT_PATH", ''))
        task.SetEnvironmentVariable("PROJECT", self._conf["project"])
        task.SetEnvironmentVariable("SCENE", self._conf["scene"])
        task.SetEnvironmentVariable("RENDERER", self._conf["renderer"])
        task.SetEnvironmentVariable("LOGS", self._conf["logs"])
        task.SetEnvironmentVariable("OUTPUT", self._conf["output"])

    def DoIt(self):
        scheduler = Scheduler()
        # make a connection to the cluster
        print "Connecting to cluster at: %s" % self.HeadNode
        try:
            scheduler.Connect(self.HeadNode)
        except:
            print >> sys.stderr, "\nError!"
            print >> sys.stderr, "Unable to reach cluster head node: %s" % self.HeadNode
            print >> sys.stderr, "Exiting..."
            sys.exit(2)

        job = scheduler.CreateJob()
        
        # job properties
        job.Name = self._conf["name"]
        
        #job.NodeGroups.Add("ComputeNodes")
        job.IsExclusive = True
        
        # attach tasks to job
        self.BuildTaskList(job)
        
        # ship it out to the head node
        scheduler.SubmitJob(job, self.RUNAS_USER, self.RUNAS_PASSWORD)
        print "Submitted job %d to %s." % (job.Id, self.HeadNode)
        sys.exit(0)


# Command Line Entry Point
def main():
    conf_path = None
    try:
        conf_path = os.path.abspath(sys.argv[1])
    except IndexError:
        print >> sys.stderr, "\nError!"
        print >> sys.stderr, "Must specify an ini file."
        print >> sys.stderr, "Exiting..."
        sys.exit(3)
    print "Spooling job from %s" % conf_path
    try:
        spool = Spooler(conf_path)
        spool.DoIt()
    except Exception, e:
        print >> sys.stderr, e
        sys.exit(-1)

if '__main__' == __name__:
    main()