import os, string, getpass, datetime, uuid
import rrt
from rrt.settings import HPC_SPOOL_BIN, JOBSPEC_DIR, JOB_LOGS_UNC
from rrt.filesystem import get_share
from rrt import RinglingException

class JobSpecError(RinglingException): pass

class JobSpec(object):
    
    INI_TEMPLATE = string.Template("""
    # Created for $user on $date by $version
    renderer = $renderer
    name = $title
    project = $project
    output = $output
    scene = $scene
    logs = $logs
    start = $start
    end = $end
    threads = $threads
    step = $step
    net_drive = $net_drive
    net_share = $net_share
    """)

    _job_data = {}
    
    def _get_data(self):
        return self._job_data
        
    def _set_data(self, data):
        """
        Portions of the job spec should be generated by the system here (each time new data is loaded)
        """
        now = str(datetime.datetime.now())
        self._job_data = data
        self._job_data['date'] = now
        self._job_data['version'] = rrt.get_version()
        self._job_data['user'] = getpass.getuser()
        self._job_data['logs'] = os.path.join(JOB_LOGS_UNC, 
                                                  getpass.getuser(), 
                                                  '{job_id}', # we're going to let hpc-spool inject the job id into the path right before the job is submitted 
                                                  self._job_data['title']+'.*.txt')
        
        for k in ['renderer', 'title', 'project', 'scene', 'start', 'end', 'step', 'output']:
            if not self._job_data.get(k, False):
                raise JobSpecError("%s cannot be blank." % k)
        try:
            self._job_data['net_share'] = get_share(self._job_data['project'])+"hpc"
        except Exception:
            raise JobSpecError("Can't find network share for project '%s'." % self._job_data['project'])
        try:
            self._job_data['net_drive'] = os.path.splitdrive(self._job_data['project'])[0]
        except Exception:
            raise JobSpecError("Can't find drive letter in project path: '%s'" % self._job_data['project'])
     
    data = property(_get_data, _set_data)
    
    def __init__(self, title, project, scene, start, end, step=1, **kwargs):
        data = dict(title=title, project=project, scene=scene, start=start, end=end, step=step)
        data.update(kwargs)
        self._set_data(data)
    
    def filter_text(self, s):
        return self._filter_text_pattern.sub('', s).strip()
    
    @property
    def ini_data(self):
        """
        Generates the content for a job (ini) file.
        """
        return self.INI_TEMPLATE.substitute(self._job_data) 

    def _write_ini_file(self):
        """
        Writes a job definition (ini) string to a temp file.  
        The file's dir is specified in `rrt.settings.JOBSPEC_DIR`, and 
        the creation of that dir is handled by this method (as needed).
        """
        if not os.path.isdir(JOBSPEC_DIR):
            os.makedirs(JOBSPEC_DIR)
        file_path = os.path.join(JOBSPEC_DIR, str(uuid.uuid4())+'.ini')
        with open(file_path,'w+b') as fh:
            fh.write(self.ini_data)
        return file_path
    
    def submit_job(self, pause=False):
        fp = self._write_ini_file()
        cmd = '%s "%s"' % (HPC_SPOOL_BIN, fp)
        if pause:
            cmd += " & pause"
        os.system(cmd)
