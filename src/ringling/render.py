import os, logging, datetime
from string import Template
from pymel.core import SCENE, mel, workspace, sceneName, Env, window,  rowColumnLayout, frameLayout, uiTemplate, columnLayout, button, optionMenu, menuItem, intField, text, textField, scriptJob
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

__VERSION__ = (0,0,1)
__VERSION_TAG__ = "dev"

# using this global keeps the object alive after it is created -- important!
WINDOW = None # global tracks the GUI instance
# these globals track the user configurable values in the GUI
JOB_THREADS = None
JOB_TITLE = None

def get_version():
    version_string = __name__+' v'+'.'.join([str(n) for n in __VERSION__])
    if __VERSION_TAG__:
        version_string += '-%s' % __VERSION_TAG__
    return version_string

RG = SCENE.defaultRenderGlobals

HPC_SPOOL_BIN = r'hpc-spool.exe' # just use whichever is in the path first
JOB_SCRIPT_DIR = os.path.join('D:\\', 'hpcjobs', Env().user())

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
 
def get_scene_name():
    return os.path.splitext(os.path.basename(sceneName()))[0]

def get_frame_range():
    """Returns a tuple of start and end frame numbers"""
    return (int(RG.startFrame.get()), int(RG.endFrame.get()))


class SubmitGui(object):
    window_title = "Send to HPC Cluster"
    
    _win = None
    _controls = {}
    
    # references to key controls
    @property
    def job_title(self):
        return self._controls['title'].getText()
    @property
    def job_threads(self):
        return int(self._controls['threads'].getValue())

    def build_job_script(self):
        range = get_frame_range()
        data = {
                'date': datetime.datetime.now(),
                'version': get_version(),
                'job_type': get_job_type(),
                'job_name': self.job_title,
                'user': Env().user(),
                'project_path': workspace.getPath(),
                'output_path': SPOOL_LETTER+'/'+Env().user()+'/output/',
                'scene_path': sceneName(),
                'logs': SPOOL_LETTER+'/'+Env().user()+'/logs/'+get_scene_name()+'.*.txt', 
                'start': min(range),
                'end': max(range),
                'threads': self.job_threads,
                'step': int(RG.byFrameStep.get()),
        }
        script = INI_TEMPLATE.substitute(data).replace(SPOOL_LETTER, SPOOL_UNC
                                                    ).replace(
                                                    SPOOL_LETTER.lower(), SPOOL_UNC
                                                    ).replace('/', '\\') 
        return script
    
    def write_job_script(self, data):
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


    
    def submit_job(self, *args, **kwargs):
        if scene_is_dirty():
            LOG.error("File has unsaved changes.  Save before submitting!")
            return
        fp = self.write_job_script(self.build_job_script())
        cmd = '%s "%s" & pause' % (HPC_SPOOL_BIN, fp)
        LOG.debug("job script:")
        LOG.debug(open(fp).read())
        LOG.debug(cmd)
        os.system(cmd)
        
    def __init__(self):
        self._win = window(title=self.window_title, resizeToFitChildren=True)
        with self._win:
            template = uiTemplate('HpcSubmitTemplate', force=True )
            template.define(frameLayout, borderVisible=True, labelVisible=False)
            template.define(text, width=75, align='right')
            with template:
                with columnLayout():
                    with frameLayout():
                        with columnLayout(width=197):
                            with rowColumnLayout(numberOfColumns=2, columnSpacing=(2,3)):
                                
                                text(label="Title:")
                                self._controls['title'] = textField(text=get_scene_name())
                                
                                text(label="Start Frame:")
                                start_field = intField(editable=False, value=get_frame_range()[0])
                                scriptJob(parent=self._win, attributeChange=[RG.startFrame, 
                                    lambda: start_field.setValue(get_frame_range()[0])])
                                                       
                                text(label="End Frame:")
                                end_field = intField(editable=False, value=get_frame_range()[1])
                                scriptJob(parent=self._win, attributeChange=[RG.endFrame, 
                                    lambda: end_field.setValue(get_frame_range()[1])])
                                
                                text(label="By Frame Step:")
                                step_field = intField(editable=False, value=int(RG.byFrameStep.get()))
                                scriptJob(parent=self._win, attributeChange=[RG.byFrameStep, 
                                    lambda: step_field.setValue(int(RG.byFrameStep.get()))])
                                
                                text(label="Cores:")
                                self._controls['threads'] = optionMenu()
                                with self._controls['threads']:
                                    menuItem(label=1)
                                    menuItem(label=2)
                                    menuItem(label=4)
                                    menuItem(label=8)
                                self._controls['threads'].setSelect(4)
                    with frameLayout():
                        with columnLayout(width=200):        
                            submit_btn = button(label="Submit", width=200, height=40, align='center')
                            submit_btn.setCommand(self.submit_job)
        # WINDOW.show() is implied at the end of the `with WINDOW` block
                        
        
    def __del__(self):
        try: self._win.delete()
        except: pass

