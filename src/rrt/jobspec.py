import os, string, getpass, re, datetime
import rrt
from rrt.settings import HPC_SPOOL_BIN, JOBSPEC_DIR, JOB_LOGS_UNC
from rrt.filesystem import get_share
LOG = rrt.get_log('hpcSubmit')

class JobSpec(object):
    INI_TEMPLATE = string.Template("""
    # Created for $user on $date by $version
    renderer = $job_type
    name = $job_name
    project = $project_path
    output = $output_path
    scene = $scene_path
    logs = $logs
    start = $start
    end = $end
    threads = $threads
    step = $step
    uuid = $uuid
    net_drive = $net_drive
    net_share = $net_share
    """)

    _filter_text_pattern = re.compile('[%s]' % re.escape(string.punctuation))
    _allowed_punctuation = r'/\._-'
    _illegal_path = re.sub('[%s]' % re.escape(_allowed_punctuation),'',string.punctuation)
    
    _job_data = {}
    
    def is_valid(self):
        raise NotImplementedError
    
    def _get_data(self):
        return self._job_data
        
    def _set_data(self, data):
        """
        Portions of the job spec should be generated by the system here (each time new data is loaded)
        """
        self._job_data = data
        self._job_data['uuid'] = re.sub('[%s]'% re.escape(' -:'),'', 
                                        str(datetime.datetime.now()).split('.')[0])
        self._job_data['date'] = datetime.datetime.now()
        self._job_data['version'] = rrt.get_version()
        self._job_data['user'] = getpass.getuser()
        if 'logs' not in data or not data['logs']:
            self._job_data['logs'] = os.path.join(JOB_LOGS_UNC, 
                                                  getpass.getuser(), 
                                                  self._job_uuid, 
                                                  self.job_title+'.*.txt')
        self._job_data['net_share'] = get_share(self._job_data['project'])
        self._job_data['net_drive'] = os.path.splitdrive(self._job_data['project'])[0]
     
    data = property(_get_data, _set_data)
    
    def __init__(self, data, validator):
        self._set_data(data)
        self.is_valid = validator
    
    def filter_text(self, s):
        return self._filter_text_pattern.sub('', s).strip()

    def build_ini_file(self, data):
        """
        Generates the content for a job (ini) file.
        """
        return self.INI_TEMPLATE.substitute(data) 

    def write_ini_file(self, data):
        """
        Writes a job definition (ini) string to a file, using the last 
        generated job_uuid (datetime) and scene name.  
        The file's dir is specified in `rrt.settings.JOBSPEC_DIR`, and 
        the creation of that dir is handled by this method (as needed).
        """
        if not os.path.isdir(JOBSPEC_DIR):
            os.makedirs(JOBSPEC_DIR)
        file_path = JOBSPEC_DIR+'\\'+self._job_uuid+'.ini'
        with open(file_path,'w+b') as fh:
            fh.write(data)
        return file_path
    
    def submit_job(self, *args, **kwargs):
        if self.is_valid(): 
            fp = self.write_ini_file(self.build_ini_file())
            cmd = '%s "%s" & pause' % (HPC_SPOOL_BIN, fp)
            LOG.debug("job script:")
            LOG.debug(open(fp).read())
            LOG.debug(cmd)
            os.system(cmd)
