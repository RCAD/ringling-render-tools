"""
The hpc-spool.bat file sets up the ipy interpreter then executes this script 
with any additional arguments -- you should not call this script directly!

This standalone script must be run with IronPython (ipy.exe) since it relies on
the Microsoft Hpc .Net assemblies. It will not work if you run it using the 
regular python interpreter. 
"""

import clr, sys, os, getpass, logging, re, datetime

RRT_DEBUG = (os.getenv('RRT_DEBUG', False) == '1')

__LOG_LEVEL__ = logging.DEBUG if  RRT_DEBUG else logging.INFO
LOG = logging.getLogger('hpc-spool')
LOG.setLevel(__LOG_LEVEL__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s: %(message)s")
handler.setFormatter(formatter)
LOG.addHandler(handler)

clr.AddReference("Microsoft.Hpc.Scheduler")
clr.AddReference("Microsoft.Hpc.Scheduler.Properties")

from Microsoft.Hpc.Scheduler import *
from Microsoft.Hpc.Scheduler.Properties import *

MAYA_TIMEOUT = 60 * 60
MAX_TIMEOUT = MAYA_TIMEOUT * 3

class Spooler(object):
    REQUIRED_SERVER_VERSION = (3, 2, 3716, 0)
    RUNAS_USER = None;
    RUNAS_PASSWORD = None;

    @property
    def HeadNode(self):
        host = os.getenv("HEAD_NODE", None)
        if None == host:
            LOG.error("HEAD_NODE is null - please set HEAD_NODE.")
            LOG.info("Exiting...")
            sys.exit(1)
        return host.strip()

    # Looks like Render.exe doesn't like quotes around the remote paths...
    CMD_MAYA_RENDER_SW = "Render.exe -n {threads} -r sw -s * -e * -proj {node_project} -rd {output} {scene}"
    # Note: -jpf is job phase filter, we do phase 1 during node prep, phase 2 during parametric sweep, and skip the 3rd (cleanup)
    # since we will blow away the entire directory during node release
    CMD_MAYA_RENDER_RMAN = "Render.exe -jpf 2 -r rman -setAttr rman__riopt__statistics_endofframe 1 -setAttr rman__riopt__statistics_xmlfilename {stats} -s * -e * -proj {node_project} -rd {output} {scene}"
    CMD_3DSMAX_RENDER = "3dsmaxcmd.exe -frames=*-* -workPath:{node_project} -o:{output} -showRFW:0 -continueOnError:1 {node_project}\{scene}"
    CMD_C4D_RENDER = '"C:\\Program Files\\MAXON\\CINEMA 4D R13\\CINEMA 4D 64 Bit.exe" -nogui -render "{node_project}\{scene}" -frame * * -oimage "{output}" '

    _renderers = {
        "max": CMD_3DSMAX_RENDER,
        "maya_render_rman": CMD_MAYA_RENDER_RMAN,
        "maya_render_sw": CMD_MAYA_RENDER_SW,
        "md": CMD_C4D_RENDER
    }
    
    _jobTemplate = {
        "max": "IDTemplate",
        "maya_render_rman": "CATemplate",
        "maya_render_sw": "CATemplate",
        "md": "C4DTemplate"
    }

    _confFile = None

    _conf = {
        "renderer": None,
        "name": None,
        "project": None,
        "node_project": None,
        "output": None,
        "logs": None,
        "stats": None,
        "scene": None,
        "start": None,
        "end": None,
        "step": "1",
        "threads": "4",
        "net_share": None,
        "net_drive": None,
        "ext": None,
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
        for k, v in self._conf.items():
            LOG.debug("%s = %s" % (k, v))

    def __init__(self, confFile):
        self._confFile = confFile
        self.ParseConf(self._confFile)

    def BuildTaskList(self, job, scheduler):
        # this guy will need other methods to delegate to so we don't fork for each renderer available.
        render_task = job.CreateTask()
        render_task.SetEnvironmentVariable("INIT_WD", self._conf['node_project'])

        #Main Render Task
        # basic info
        render_task.Name = "Render *"
        render_task.Type = TaskType.ParametricSweep

        #render_task.Runtime = MAX_TIMEOUT if self._conf['renderer'] == 'max' else MAYA_TIMEOUT

        #task iteration
        render_task.StartValue = int(self._conf["start"])
        render_task.EndValue = int(self._conf["end"])
        render_task.IncrementValue = int(self._conf["step"])

        # thread/node limits
        if not (self._conf["renderer"] == "max" or self._conf["renderer"] == "md"):
            render_task.MinimumNumberOfCores = 4 #int(self._conf["threads"])
            render_task.MaximumNumberOfCores = 4 #int(self._conf["threads"])

        # log redirection
        render_task.StdErrFilePath = self._conf["logs"].format(job_id=self._conf['job_id'])
        render_task.StdOutFilePath = self._conf["logs"].format(job_id=self._conf['job_id'])

        # run the render command
        if self._conf["renderer"] == "md":
            if os.getenv("MULTIPASS", None) == "True":
                self._renderers["md"] += '-omultipass "{output}" '
            if not self._conf["ext"] == "-Other":
                self._renderers["md"] += '-oformat {ext}'                
        render_task.CommandLine = self._renderers[self._conf["renderer"]].format(**self._conf)

        # Setup Task
        setup_task = job.CreateTask()
        setup_task.Type = TaskType.NodePrep
        setup_task.Name = "Setup"
        setup_task.CommandLine = "net use %s %s && hpc-node-prep" % (self._conf['net_drive'], self._conf['net_share'])

        # we will do a preflight phase render to generate tex files, etc
        if self._conf["renderer"] == "maya_render_rman":            
            prepStr = r"{logs}".format(**self._conf).rsplit('\\',1)[0]
            setup_task.CommandLine += " & Render.exe -n {threads} -r rman -jpf 1 -proj {node_project} {scene} >> ".format(**self._conf)+prepStr+"\\nodeprep.%computername%.log 2>&1"
        
        #Stats Task: creates the task for all task stats and renderman stats if renderer is renderman
        stats_task = job.CreateTask()
        stats_task.Type = TaskType.Basic
        stats_task.Name = "Stats Gathering"
        stats_task.Runtime = 600
        dependent = scheduler.CreateStringCollection()
        dependent.Add(render_task.Name)
        stats_task.DependsOn = dependent
        stats_dir = r"{stats}".format(**self._conf).rsplit('\\',1)[0]
        jID = r"{job_id}".format(**self._conf).rsplit('.',1)[0]
        stats_task.CommandLine = 'powershell.exe -command "add-pssnapin microsoft.hpc; (get-hpctask -scheduler '+self.HeadNode+' -jobid '+jID+' | select Name, type, state, elapsedtime, maxcores, allocatednodes, stderr, exitcode, errormessage, subtaskid | convertto-xml -notypeinformation).Save(\''+stats_dir+'\\raw.xml\');" & python \\\\hpc\statsbin\cleanXML.py '+stats_dir

        if self._conf["renderer"] == "maya_render_rman":
            stats_task.CommandLine +=r" & python \\hpc\statsbin\stats_grapher_hpc1.py "+stats_dir+r" & python \\hpc\statsbin\stats_tasks_hpc.py "+stats_dir
            stats_task.MinimumNumberOfCores = 4
            stats_task.MaximumNumberOfCores = 4
        else:
            stats_task.CommandLine +=r" & python \\hpc\statsbin\stats_tasks_hpc.py "+stats_dir
            if self._conf["renderer"] == "maya_render_sw":
                stats_task.MinimumNumberOfCores = 4
                stats_task.MaximumNumberOfCores = 4

        # TearDown Task
        cleanup_task = job.CreateTask()
        cleanup_task.Type = TaskType.NodeRelease
        cleanup_task.Name = "Cleanup"
        #cleanup_task.CommandLine = "net use %s /delete /y" % self._conf['net_drive']
        cleanup_task.CommandLine = "hpc-node-release & net use %s /delete /y" % self._conf['net_drive']

        for task in [setup_task, render_task, cleanup_task, stats_task]:
            self.SetJobEnv(task)
            job.AddTask(task)
        
    def SetJobEnv(self, task):
        global RRT_DEBUG
        if RRT_DEBUG: task.SetEnvironmentVariable("RRT_DEBUG", str(RRT_DEBUG))

        task.SetEnvironmentVariable("MAYA_APP_DIR", self._conf["node_project"])
        task.SetEnvironmentVariable("TEMP", self._conf["node_project"])
        task.SetEnvironmentVariable("TMP", self._conf["node_project"])
        task.SetEnvironmentVariable("OWNER", getpass.getuser())
        task.SetEnvironmentVariable("NODE_PROJECT", self._conf["node_project"])
        # script path override enables us to apply per-job dirmaps on maya jobs
        task.SetEnvironmentVariable("MAYA_SCRIPT_PATH", self._conf["node_project"] + r"\scripts;" + os.getenv("MAYA_SCRIPT_PATH", ''))
        task.SetEnvironmentVariable("PROJECT", self._conf["project"])
        task.SetEnvironmentVariable("SCENE", self._conf["scene"])
        task.SetEnvironmentVariable("RENDERER", self._conf["renderer"])
        task.SetEnvironmentVariable("LOGS", self._conf["logs"])
        task.SetEnvironmentVariable("OUTPUT", self._conf["output"])
        task.SetEnvironmentVariable("STATS", self._conf["stats"])
        task.SetEnvironmentVariable("NET_SHARE", self._conf["net_share"])
        task.SetEnvironmentVariable("NET_DRIVE", self._conf["net_drive"])
        if self._conf["renderer"] == "md": #not really needed but for debugging
            task.SetEnvironmentVariable("MULTIPASS", os.getenv("MULTIPASS", None))
        task.SetEnvironmentVariable("EXT", self._conf["ext"])

    def DoIt(self):
        scheduler = Scheduler()

        try:
            # make a connection to the cluster
            LOG.info("Connecting to cluster at: %s" % self.HeadNode)
            try:
                scheduler.Connect(self.HeadNode)
            except Exception, e:
                LOG.error("Unable to reach cluster head node: %s" % self.HeadNode)
                LOG.exception(e)
                LOG.info("Exiting...")
                sys.exit(2)
            # check the cluster api version
            server_version = scheduler.GetServerVersion()
            serv = '.'.join([str(d) for d in (server_version.Major,
                              server_version.Minor,
                              server_version.Build,
                              server_version.Revision)])
            reqv = '.'.join([str(d) for d in self.REQUIRED_SERVER_VERSION])
            if serv != reqv:
                scheduler.Close()
                raise RuntimeError('HPC API mismatch: got %s, but required %s' % (serv, reqv))
            job = scheduler.CreateJob()
            scheduler.AddJob(job) # creates the job on the HEAD_NODE, but in a configuring state.
            # since we have more than one cluster, we user HEAD_NODE to ensure the job id's don't overlap
            self._conf['job_id'] = "%d.%s" % (job.Id, self.HeadNode)

            node_job_dir = r"D:\hpc"
            self._conf["node_job_dir"] = node_job_dir
            node_project = os.path.join(node_job_dir, '{job_id}')
            self._conf["node_project"] = node_project

            for i in ['output', 'logs', 'node_project', 'stats']:
                # inject job_id into logs/output/node_project/stats
                self._conf[i] = self._conf[i].format(job_id=self._conf['job_id'])

            # set the job properties
            job.Name = self._conf["name"]
            # task by node granularity setting for 3ds Max
            if self._conf["renderer"] == "max":
                job.UnitType = JobUnitType.Node
            elif self._conf["renderer"] == "md":
                job.UnitType = JobUnitType.Socket
            else:
                job.UnitType = JobUnitType.Core
            #job.NodeGroups.Add("ComputeNodes")
            job.IsExclusive = True
            job.SetJobTemplate(self._jobTemplate[self._conf["renderer"]])
            self.BuildTaskList(job, scheduler) # attach tasks to job
            job.Commit() # sync job data back to the HEAD_NODE (still configuring).
            scheduler.SubmitJob(job, self.RUNAS_USER, self.RUNAS_PASSWORD) # submit the job to get it queued.
            LOG.info("Submitted job %d to %s." % (job.Id, self.HeadNode))
            scheduler.Close()
        except Exception, e:
            try:
                scheduler.CancelJob(job.Id, "Job canceled because of submission error.")
            except:
                pass
            LOG.exception(e)
            LOG.error("exiting...")
            sys.exit(5)
        finally:
            scheduler.Dispose()
        sys.exit(0)


# Command Line Entry Point
def main():
    LOG.info('Starting local-spool for MS HPC v' + '.'.join([str(v) for v in Spooler.REQUIRED_SERVER_VERSION]))
    conf_path = None
    try:
        conf_path = os.path.abspath(sys.argv[1])
    except IndexError:
        LOG.error("Must specify an ini file.")
        LOG.info("Exiting...")
        sys.exit(3)
    LOG.info("Spooling job from %s" % conf_path)
    try:
        spool = Spooler(conf_path)
        spool.DoIt()
    except Exception, e:
        LOG.error(e)
        sys.exit(-1)

if '__main__' == __name__:
    main()
