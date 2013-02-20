"""
This file sets up and builds a batch file thaqt runs a local or cluster equivalent render
"""

import sys, os, getpass, logging, re, datetime, uuid

EMULATE = (os.getenv('EMULATE', False) == '1')
RRT_DEBUG = True

__LOG_LEVEL__ = logging.DEBUG if  RRT_DEBUG else logging.INFO
LOG = logging.getLogger('hpc-spool')
LOG.setLevel(__LOG_LEVEL__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s: %(message)s")
handler.setFormatter(formatter)
LOG.addHandler(handler)


class Spooler(object):
    RUNAS_USER = None;
    RUNAS_PASSWORD = None;

    # Looks like Render.exe doesn't like quotes around the remote paths...
    CMD_MAYA_RENDER_SW = "Render.exe -n {threads} -r sw -s * -e * -proj {node_project} -rd {output} {scene} >> {logs}"
    CMD_MAYA_RENDER_RMAN = "Render.exe -n {threads} -jpf 2 -r rman -setAttr rman__riopt__statistics_endofframe 1 -setAttr rman__riopt__statistics_xmlfilename {stats} -s * -e * -proj {node_project} -rd {output} {scene} >> {logs}"
    CMD_MAYA_RENDER_SW_LOCAL = "Render.exe -n {threads} -r sw -s {start} -e {end} -b {step} -rd {output} {scene} >> {logs}"
    CMD_MAYA_RENDER_RMAN_LOCAL = "Render.exe -n {threads} -jpf 2 -r rman -setAttr rman__riopt__statistics_endofframe 1 -setAttr rman__riopt__statistics_xmlfilename {stats} -s {start} -e {end} -b {step} -rd {output} {scene} >> {logs}"   

    _renderers = {
        "maya_render_rman": CMD_MAYA_RENDER_RMAN,
        "maya_render_sw": CMD_MAYA_RENDER_SW,
        "maya_render_rman_local": CMD_MAYA_RENDER_RMAN_LOCAL,
        "maya_render_sw_local": CMD_MAYA_RENDER_SW_LOCAL
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

    def BuildTaskList(self):
        # Setup Task
        setup_task = []
        setup_task.append("@echo off")
        setup_task.append("setlocal")
        setup_task.append("echo Setting envorinment variables")
        setup_task += self.SetJobEnv()
        setup_task.append('echo Starting Setup Task')        
        setup_task.append("echo Setting up node project directory: %s" % self._conf["node_project"])
        setup_task.append('mkdir "%s"' % self._conf["node_project"])
        setup_task.append("echo Creating directory %s" % os.path.dirname(self._conf['logs']))
        setup_task.append('mkdir "%s"' % os.path.dirname(self._conf['logs']))
        setup_task.append("echo Creating directory %s" % self._conf['output'])
        setup_task.append('mkdir "%s"' % self._conf['output'])
        if self._conf["renderer"] == "maya_render_rman" or self._conf["renderer"] == "maya_render_rman_local":
            setup_task.append("echo Creating directory %s" % os.path.dirname(self._conf['stats']))
            setup_task.append('mkdir "%s"' % os.path.dirname(self._conf['stats']))
        
        # prep steps when emulation is enabled
        if EMULATE:
            src = os.path.join(self._conf['project'],'workspace.mel')
            dst = os.path.join(self._conf['node_project'],'workspace.mel')
            setup_task.append('copy /Y "%s" "%s"' % (src, dst))
            setup_task.append("echo File copied: %s into %s" % (src,dst))
            
            setup_task.append("echo Copying any fur data...")
            for name in os.listdir(self._conf['project']):
                src = os.path.join(self._conf['project'], name)
                if name.startswith('fur') and os.path.isdir(src):
                    dst = os.path.join(self._conf['node_project'], name)
                    setup_task.append('echo d | xcopy /S /Q "%s" "%s"' % (src, dst))
                    setup_task.append("echo Files copied: %s into %s" % (src,dst))
                    LOG.debug("File copied: %s into %s" % (src,dst))
            
            dst = os.path.join(self._conf['node_project'],'scripts','userSetup.mel')
            setup_task.append("echo Writing %s" % dst)
            setup_task.append('mkdir "%s"' % os.path.dirname(dst))
            setup_task.append('echo python("import rrt.hpc.maya.startup"); > %s' % dst)
        
        setup_task.append('echo Opening project space on file browser')
        setup_task.append('%SystemRoot%\explorer.exe "'+self._conf["node_project"]+'"')
        
        # we will do a preflight phase render to generate tex files, etc        
        if self._conf["renderer"] == "maya_render_rman":
            setup_task.append("echo Setting up Preflight Render")
            prepStr = os.path.dirname(self._conf['logs'])
            setup_task.append("Render.exe -n {threads} -r rman -jpf 1 -proj {node_project} {scene} >> ".format(**self._conf)+prepStr+"\\nodeprep.%computername%.log 2>&1")

        if self._conf["renderer"] == "maya_render_rman_local":
            setup_task.append("echo Setting up Preflight Render")
            prepStr = os.path.dirname(self._conf['logs'])
            setup_task.append("Render.exe -n {threads} -r rman -jpf 1 {scene} >> ".format(**self._conf)+prepStr+"\\nodeprep.%computername%.log 2>&1")
        
        
        #Main Render Task
        render_task = []
        render_task.append("echo Setting up render commands for frames %s to %s with %s interval" % (str(self._conf['start']),str(self._conf['end']), str(self._conf['step'])))
        # run the render command
        if EMULATE:
            for frame in range(int(self._conf["start"]), int(self._conf["end"])+1, int(self._conf['step'])):
                render_task.append('echo Rendering frame #%s' % str(frame))
                render_task.append(str(self._renderers[self._conf["renderer"]].format(**self._conf)).replace('*', str(frame)))
        else:
            renderCmd = str(self._renderers[self._conf["renderer"]].format(**self._conf))
            renderCmd = renderCmd.replace('.*.', '.')
            render_task.append(renderCmd)
        
        # TearDown Task
        cleanup_task = []        
        cleanup_task.append("echo Cleaning up")
        cleanup_task.append("endlocal")
        cleanup_task.append("echo Rendering complete")
        cleanup_task.append("pause")
        
        batchFile = os.path.join('D:', 'hpc', 'jspec', str(getpass.getuser()))+'\\'+str(uuid.uuid4())+'.bat'
        f = open(batchFile, 'w')
        for task in [setup_task, render_task, cleanup_task]:
            for line in task:
                f.write("%s\n" % line)
        f.close()
        return batchFile

    def SetJobEnv(self):
        environments = []
        global RRT_DEBUG
        if RRT_DEBUG: environments.append("set RRT_DEBUG=%s" % str(RRT_DEBUG))
        environments.append("set MAYA_APP_DIR=%s" % self._conf["node_project"])
        environments.append("set TEMP=%s" % self._conf["node_project"])
        environments.append("set TMP=%s" % self._conf["node_project"])
        environments.append("set OWNER=%s" % getpass.getuser())
        environments.append("set NODE_PROJECT=%s" % self._conf["node_project"])
        environments.append("set MAYA_SCRIPT_PATH=%s" % (self._conf["node_project"] + r"\scripts;" + os.getenv("MAYA_SCRIPT_PATH", '')))
        environments.append("set PROJECT=%s" % self._conf["project"])
        environments.append("set SCENE=%s" % self._conf["scene"])
        environments.append("set RENDERER=%s" % self._conf["renderer"])
        environments.append("set LOGS=%s" % self._conf["logs"])
        environments.append("set OUTPUT=%s" % self._conf["output"])
        environments.append("set STATS=%s" % self._conf["stats"])
        environments.append("set NET_SHARE=%s" % self._conf["net_share"])
        environments.append("set NET_DRIVE=%s" % self._conf["net_drive"])
        environments.append("set EXT=%s" % self._conf["ext"])
        return environments

    def DoIt(self):

        try:            
            self._conf['job_id'] = "%s.%s" % (str(uuid.uuid4()).split('-')[0], 'local')

            node_job_dir = r"D:\hpc"
            self._conf["node_job_dir"] = node_job_dir
            node_project = os.path.join(node_job_dir, getpass.getuser(), '{job_id}')
            self._conf["node_project"] = node_project

            for i in ['output', 'logs', 'node_project', 'stats']:
                # inject job_id into logs/output/node_project/stats
                self._conf[i] = self._conf[i].format(job_id=self._conf['job_id'])

            cmd = self.BuildTaskList() # build batch file
            os.startfile(cmd)
            LOG.info("Submitted local job %s" % (self._conf['job_id']))
        except Exception, e:
            try:
                LOG.error("Job canceled because of submission error.")
            except:
                pass
            LOG.exception(e)
            LOG.error("exiting...")
            sys.exit(5)
        finally:
            LOG.info("Process Closed")
        sys.exit(0)


# Command Line Entry Point
def main():
    LOG.info('Starting hpc-spool for Local launch')
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
