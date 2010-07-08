from pymel.all import *
import os, uuid, logging
from string import Template
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

ALF_SCRIPT_DIR = os.path.join('D:\\', 'rfmjobs', os.environ['USERNAME'])
LOCAL_PROJECT_DIR = '/'.join(['D:', os.environ['USERNAME'], 'MAYA', 'projects', 'default'])
OUTPUT_DIR = '/'.join(['S:', os.environ['USERNAME'], 'output'])

def chunks(l, n):
    """ Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


def get_render_globals():
    return core.SCENE.defaultRenderGlobals

def get_frame_range():
    rg = get_render_globals()
    return (rg.startFrame.get(), rg.endFrame.get())

def submit_job(*args):
    frange = get_frame_range()
    fcount = len(range(int(frange[0]),int(frange[1])))+1
    chunk = chunk_size.getValue()
    if fcount < chunk:
        log.warning('Chunk size is higher than frame range!')
        log.warning('Setting chunk size to frame count.')
        chunk = fcount
    do_ribgen_now = local_ribgen.getValue()     
    if do_ribgen_now:
        mel.rman('genrib')
    else:
        chunk_task_template = Template("""
        Task -title {Chunk $chunk (Frames $s-$e)} -cmds {
            RemoteCmd {%D(mayabatch) -command "renderManBatchRenderScript(1,$s,$e,1,2)" -proj "%D($proj)" -file "%D($scene)"} -service {pixarmtor}
            RemoteCmd {%D(Render) -proj "%D($proj)" -s $s -e $e -r rman -rd "%D($output)" "%D($scene)"} -service {pixarmtor}
        }
        
        """)
        frame_list = chunks(range(frange[0],frange[1]+1), chunk)
        alf = ""
        for k,v in enumerate(frame_list):
            alf += chunk_task_template.substitute(proj=LOCAL_PROJECT_DIR, output=OUTPUT_DIR, chunk=k+1, s=v[0], e=v[-1],scene=mel.rmanGetSceneFile())
        
        log.debug(alf)

def write_alf_script(data):
    """
    Creates a file with the alf job defined inside.
    """
    if not os.path.isdir(ALF_SCRIPT_DIR):
        os.makedirs(ALF_SCRIPT_DIR)
    file_path = ALF_SCRIPT_DIR + '\\' + mel.rmanGetSceneName()+'_'+str(uuid.uuid4())+'.alf'
    with open(file_path,'w+b') as fh:
        fh.write(data)
    return file_path

win = window(title="Send to Farm")
layout = columnLayout()
local_ribgen = checkBox(label = "Local Ribgen", value=True, parent=layout)
chunk_label = text(label="Frames per server:")
chunk_size = intField(value=5)
submit_btn = button(label="Submit", parent=layout)
submit_btn.setCommand(submit_job)
win.show()