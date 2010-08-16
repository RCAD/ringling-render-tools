import os, datetime, re, string

import rrt
from rrt import SPOOL_UNC, SPOOL_LETTER, JOB_LOGS_UNC, JOB_OUTPUT_UNC
from rrt.maya.helpers import ProjectPath, InvalidPathError
from rrt.maya.shortcuts import scene_is_dirty, get_job_type, get_scene_name, get_frame_range

from pymel import versions
from pymel.core import *

LOG = rrt.get_log('hpcSubmit')
JOB_SCRIPT_DIR = os.path.join('D:\\', 'hpc', Env().user(), 'scripts')

# abspath because we can't count on it being in the PATH
HPC_SPOOL_BIN = r'C:\Ringling\HPC\bin\hpc-spool.bat' 

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
step = $step""")

class SubmitGui:
    """ A python singleton """

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if SubmitGui.__instance is None:
            # Create and remember instance
            SubmitGui.__instance = SubmitGui.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_SubmitGui__instance'] = SubmitGui.__instance
    
    @staticmethod
    def destroy():
        try: SubmitGui.__instance.destroy()
        except: pass
        SubmitGui.__instance = None
        
    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
    
    class __impl:
        """
        Manages the window, its data, the ini generation, and submission 
        routines.
        """
        
        window_title = "Send to HPC Cluster"
        
        _win = None
        _controls = {}
        # a regex used to strip out bad chars in filenames
        _filter_text_pattern = re.compile('[%s]' % re.escape(string.punctuation))
        _allowed_punctuation = r'/\._-'
        _illegal_path = re.sub('[%s]' % re.escape(_allowed_punctuation),'',string.punctuation)
        
        _job_uuid = None
        
        def filter_text(self, s):
            return self._filter_text_pattern.sub('', s).strip()

        # references to key controls
        @property
        def job_title(self):
            return self.filter_text(self._controls['title'].getText())
        @property
        def job_threads(self):
            return int(self._controls['threads'].getValue())
    
        def build_ini_file(self):
            self._job_uuid = re.sub('[%s]'% re.escape(' -:'),'', '.'.split(str(datetime.datetime.now())[0]))
            range = get_frame_range()
            proj = ProjectPath(workspace.getPath()).unc
            scene = ProjectPath(sceneName()).unc
            logs = os.path.join(JOB_LOGS_UNC, Env().user(), self._job_uuid, self.job_title+'.*.txt')
            output = os.path.join(JOB_OUTPUT_UNC, Env().user(), self._job_uuid)
            data = {
                    'date': datetime.datetime.now(),
                    'version': rrt.get_version(),
                    'job_type': get_job_type(),
                    'job_name': self.job_title,
                    'user': Env().user(),
                    'project_path': proj,
                    'output_path': output,
                    'scene_path': scene,
                    'logs': logs,
                    'start': min(range),
                    'end': max(range),
                    'threads': self.job_threads,
                    'step': int(SCENE.defaultRenderGlobals.byFrameStep.get()),
            }
            return INI_TEMPLATE.substitute(data) 

        
        def write_ini_file(self, data):
            """
            Creates a file with the HPC job defined inside then 
            returns the path to the file.
            """
            if not os.path.isdir(JOB_SCRIPT_DIR):
                os.makedirs(JOB_SCRIPT_DIR)
            file_path = JOB_SCRIPT_DIR+'\\'+self._job_uuid+'_'+get_scene_name()+'.ini'
            with open(file_path,'w+b') as fh:
                fh.write(data)
            return file_path
        
        def _is_valid(self):
            try: 
                self.build_ini_file()
            except InvalidPathError:
                LOG.error("Cannot submit from this location. Save this file in %s (aka %s) before submitting" % (SPOOL_LETTER, SPOOL_UNC))
                return False
            if not self.job_title:
                LOG.error("Job title must not be blank.")
                return False
            if ' ' in sceneName():
                LOG.error("Scene name or project path contains spaces. Rename/Save As... before submitting.")
                return False
            if re.search('[%s]' % re.escape(self._illegal_path), os.path.splitdrive(sceneName())[1]):
                LOG.error("Scene name or project path contains illegal characters: e.g. %s -- Rename/Save As... before submitting." % self._illegal_path)
                return False
            if scene_is_dirty():
                LOG.error("File has unsaved changes.  Save before submitting.")
                if not confirmBox('Unsaved changes?', 'Scene may have unsaved changes.', 'Submit Anyway', 'Cancel'):
                    return False
            return True
        
        def submit_job(self, *args, **kwargs):
            if self._is_valid(): 
                fp = self.write_ini_file(self.build_ini_file())
                cmd = '%s "%s" & pause' % (HPC_SPOOL_BIN, fp)
                LOG.debug("job script:")
                LOG.debug(open(fp).read())
                LOG.debug(cmd)
                os.system(cmd)
        
        def destroy(self):
            if self._win:
                try: self._win.delete()
                except Exception, e:
                    LOG.debug(e)
        
        def new_window(self):
            self.destroy()
            self.create()
        
        @property
        def window(self): return self._win
        def create(self):
            self._win = window(title=self.window_title, resizeToFitChildren=True)
            with self._win:
                template = uiTemplate('HpcSubmitTemplate', force=True )
                template.define(frameLayout, bs='etchedIn', mw=6, mh=6, labelVisible=False)
                template.define(columnLayout, adj=True, rs=4)
                template.define(formLayout, nd=100)
                # padding adjustment for pre-qt maya versions
                if versions.current() <= versions.v2010:
                    template.define(text, align='right', h=22)
                else:
                    template.define(text, align='right', h=20)
                with template:
                    with formLayout() as mainForm:
                        with frameLayout() as setFrame:
                            with formLayout() as setForm:
                                with columnLayout() as setCol1:
                                    text(label="Title:")
                                    text(label="Start Frame:")
                                    text(label="End Frame:")
                                    text(label="Frame Step:")
                                    text(label="Cores:")
                                with columnLayout() as setCol2:
                                    self._controls['title'] = textField(text=get_scene_name())
                                    
                                    start_field = intField(editable=False, value=get_frame_range()[0])
                                    scriptJob(parent=self._win, attributeChange=[SCENE.defaultRenderGlobals.startFrame, 
                                        lambda: start_field.setValue(get_frame_range()[0])])
                                                           
                                    end_field = intField(editable=False, value=get_frame_range()[1])
                                    scriptJob(parent=self._win, attributeChange=[SCENE.defaultRenderGlobals.endFrame, 
                                        lambda: end_field.setValue(get_frame_range()[1])])
                                    
                                    step_field = intField(editable=False, value=int(SCENE.defaultRenderGlobals.byFrameStep.get()))
                                    scriptJob(parent=self._win, attributeChange=[SCENE.defaultRenderGlobals.byFrameStep, 
                                        lambda: step_field.setValue(int(SCENE.defaultRenderGlobals.byFrameStep.get()))])
                                    
                                    with columnLayout(adj=False):
                                        self._controls['threads'] = optionMenu(w=40)
                                        with self._controls['threads']:
                                            menuItem(label=1)
                                            menuItem(label=2)
                                            menuItem(label=4)
                                            menuItem(label=8)
                                        self._controls['threads'].setSelect(4)
                            
                            setForm.attachForm(setCol1, 'left', 4)
                            setForm.attachControl(setCol1, 'right', 2, setCol2)
                            setForm.attachForm(setCol2, 'right', 4)
                            setForm.attachPosition(setCol2, 'left', 40, 20)
                            
                        with frameLayout() as subFrame:
                            submit_btn = button(label="Submit", width=200, height=40, align='center')
                            submit_btn.setCommand(self.submit_job)
                    
                    mainForm.attachForm(setFrame, 'top', 4)
                    mainForm.attachForm(setFrame, 'left', 4)
                    mainForm.attachForm(setFrame, 'right', 4)
                    mainForm.attachControl(setFrame, 'bottom', 4, subFrame)
                    mainForm.attachForm(subFrame, 'bottom', 4)
                    mainForm.attachForm(subFrame, 'left', 4)
                    mainForm.attachForm(subFrame, 'right', 4)
                    
