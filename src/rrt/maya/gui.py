import os, re, string, getpass

import rrt
from rrt.maya.shortcuts import scene_is_dirty, get_job_type, get_scene_name,\
    get_frame_range

from pymel import versions
from pymel.core.system import workspace, sceneName
from pymel.core.general import Scene
from pymel.core import frameLayout, button, menuItem, columnLayout,\
    optionMenu, intField, textField, text, formLayout, uiTemplate, window,\
    confirmBox, checkBox
from pymel.core.language import scriptJob #@UnresolvedImport
from rrt.jobspec import JobSpec
from rrt.settings import JOB_OUTPUT_UNC, HEAD_NODES

LOG = rrt.get_log('hpcSubmit')

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
        
        def filter_text(self, s):
            return self._filter_text_pattern.sub('', s).strip()

        # references to key controls
        @property
        def job_title(self):
            """
            Read-only filtered version of the job title.
            """
            return self.filter_text(self._controls['title'].getText())
        
        @property
        def job_threads(self):
            """
            Number of threads to render with, as specified by the control in the 
            submit window.
            """
            return int(self._controls['threads'].getValue())
        
        @property
        def job_start(self):
            return min((int(self._controls['start'].getValue()),int(self._controls['end'].getValue())))
        
        @property
        def job_end(self):
            return max((int(self._controls['start'].getValue()),int(self._controls['end'].getValue())))
        
        @property
        def job_step(self):
            return int(self._controls['step'].getValue())
        
        @property
        def job_data(self):
            return {
                    'renderer': get_job_type(),
                    'title': self.job_title,
                    'project': os.path.normpath(workspace.getPath()),
                    'output': os.path.join(JOB_OUTPUT_UNC, getpass.getuser(), '{job_id}', 'output'), # job_id is injected by hpc-spool when the submission happens
                    'scene': os.path.normpath(sceneName()),
                    'start': self.job_start,
                    'end': self.job_end,
                    'threads': self.job_threads,
                    'step': self.job_step,
            }
        
        def _is_valid(self):
            LOG.info("Validating submission:")
            try:
                JobSpec(**self.job_data)
            except Exception, err:
                LOG.warning('Could not build job file...')
                LOG.error(err)
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
                LOG.warning("File has unsaved changes.  Save before submitting.")
                if not confirmBox('Unsaved changes?', 'Scene may have unsaved changes.', 'Submit Anyway', 'Cancel'):
                    return False
            return True
        
        def submit_job(self, *args, **kwargs):
            if self._is_valid():
                spec = JobSpec(**self.job_data)
                LOG.debug(spec.ini_data) 
                try:
                    os.environ['HEAD_NODE'] = self._controls['head_node'].getValue()
                    os.environ['RRT_DEBUG'] = '1' if self._controls['debug'].getValue() else ''
                    spec.submit_job(pause=self._controls['pause'].getValue())
                except Exception, e:
                    LOG.error(e)
        
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
            """
            Generates a new maya window object and binds it to the singleton 
            instance.
            """
            SCENE = Scene()
            self._win = window(title=self.window_title, 
                               resizeToFitChildren=True)
            with self._win:
                template = uiTemplate('HpcSubmitTemplate', force=True )
                template.define(frameLayout, bs='etchedIn', mw=6, mh=6, 
                                labelVisible=False)
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
                                    text(label="Head Node:")
                                    text(label="Title:")
                                    text(label="Start Frame:")
                                    text(label="End Frame:")
                                    text(label="Frame Step:")
                                    text(label="Cores:")
                                with columnLayout() as setCol2:
                                    self._controls['head_node'] = optionMenu()
                                    with self._controls['head_node']:
                                        for host in HEAD_NODES: 
                                            menuItem(label=host)
                                    self._controls['title'] = textField(text=get_scene_name())
                                    self._controls['start'] = intField(value=get_frame_range()[0])
                                    self._controls['end'] = intField(value=get_frame_range()[1])
                                    self._controls['step'] = intField(value=int(SCENE.defaultRenderGlobals.byFrameStep.get()))
                                    
                                    with columnLayout(adj=False):
                                        self._controls['threads'] = optionMenu(w=40)
                                        with self._controls['threads']:
                                            menuItem(label=2)
                                            menuItem(label=4)
                                        self._controls['threads'].setSelect(1)
                                    self._controls['pause'] = checkBox(label="Pause before exit")
                                    self._controls['debug'] = checkBox(label="Show debug messages")
                            
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
                    
                    """
                    We force the closure of an open submit window on scene open 
                    to ensure the new scene's settings are reflected.
                    """
                    scriptJob(parent=self._win, runOnce=True, 
                              event=('SceneOpened', SubmitGui.destroy))
