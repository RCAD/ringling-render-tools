import os, logging, datetime
from string import Template
from pymel.core import SCENE, mel, workspace, sceneName, Env, window, checkBox, columnLayout, button, intField, text
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


__VERSION__ = (0,0,1)
__VERSION_TAG__ = "dev"

def get_version():
    version_string = __name__+' v'+'.'.join([str(n) for n in __VERSION__])
    if __VERSION_TAG__:
        version_string += '-%s' % __VERSION_TAG__
    return version_string

HPC_SPOOL_BIN = r'C:\Users\onelson\Documents\Visual Studio 2010\Projects\hpc-spool\hpc-spool\bin\Release\hpc-spool.exe'

RG = SCENE.defaultRenderGlobals

JOB_SCRIPT_DIR = os.path.join('D:\\', 'hpcjobs', Env().user())
OUTPUT_DIR = '/'.join(['S:', Env().user(), 'output'])

SPOOL_UNC = "//desmond/spool"
SPOOL_LETTER = "S:"

INI_TEMPLATE = Template("""
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
step = $step""")

def scene_is_dirty():
    return mel.eval('file -q -amf')

def get_job_type():
    if RG.currentRenderer.get() == 'renderMan':
        return 'maya_render_rman'
    return 'maya_render_sw'
 
def get_proj_dir():
    """workspace -q -dir;"""
    workspace.getPath()

def get_proj_name():
    workspace.getName()

def get_scene_path(norm=False):
    if not norm:
        return sceneName()
    else: return os.path.normpath(sceneName())

def get_scene_name():
    return os.path.splitext(os.path.basename(sceneName()))[0]

def get_frame_range():
    """Returns a tuple of start and end frame numbers"""
    return (RG.startFrame.get(), RG.endFrame.get())

def build_job_script():
    range = get_frame_range()
    data = {
            'date': datetime.datetime.now(),
            'version': get_version(),
            'job_type': get_job_type(),
            'job_name': get_scene_name(),
            'user': Env().user(),
            'project_path': workspace.getPath(),
            'output_path': None,
            'scene_path': sceneName(),
            'logs': SPOOL_LETTER+'/'+Env().user()+'/logs/'+get_scene_name()+'.txt', 
            'start': int(min(range)),
            'end': int(max(range)),
            'threads': 8,
            'step': int(RG.byFrameStep.get()),
    }
    script = INI_TEMPLATE.substitute(data).replace(SPOOL_LETTER, SPOOL_UNC
                                                   ).replace('/', '\\') 
    return script

def submit_job(*args, **kwargs):
    fp = write_job_script(build_job_script())
    os.environ['HEAD_NODE'] = '216.38.182.22'
    os.environ['PATH'] = os.path.dirname(HPC_SPOOL_BIN)
    cmd = '%s "%s" & pause' % (os.path.basename(HPC_SPOOL_BIN), fp)
    LOG.debug("job script:")
    LOG.debug(open(fp).read())
    LOG.debug(cmd)
    os.system(cmd)
    

def write_job_script(data):
    """
    Creates a file with the HPC job defined inside then 
    returns the path to the file.
    """
    if not os.path.isdir(JOB_SCRIPT_DIR):
        os.makedirs(JOB_SCRIPT_DIR)
    file_path = JOB_SCRIPT_DIR+'\\'+get_scene_name()+'_'+datetime.datetime.now().isoformat().split('.')[0].replace(':','')+'.ini'
    with open(file_path,'w+b') as fh:
        fh.write(data)
    return file_path


class SubmitGui(object):
    def show(self):
        win = window(title="Send to HPC Cluster")
        layout = columnLayout()
        local_ribgen = checkBox(label = "Local Ribgen", value=True, parent=layout)
        chunk_label = text(label="Frames per server:")
        chunk_size = intField(value=5)
        submit_btn = button(label="Submit", parent=layout)
        submit_btn.setCommand(submit_job)
        win.show()