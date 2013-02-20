import sys, os, zipfile, getpass
from PyQt4 import QtGui, QtCore
from rrt.max.ui.submit import Ui_SubmitMainWindow
from rrt.jobspec import JobSpec
from rrt.settings import JOB_OUTPUT_UNC, HEAD_NODES
from random import randint

IMAGE_EXT = sorted([
#    '.avi', 
    '.bmp', 
    '.cin', 
    '.eps', '.ps', 
    '.exr', '.fxr', '.hdr', 
    '.pic', 
    '.jpg', '.jpe', '.jpeg', 
    '.png', 
    '.rgb', '.rgba', 
    '.sgi', '.int', '.inta', '.bw', 
    '.rla', 
    '.rpf', 
    '.tga', '.vda', '.icb', 
    '.vst', 
    '.tif', 
    '.dds'
])

class SubmitGui(QtGui.QDialog, Ui_SubmitMainWindow):
    def __init__(self, parent=None):
        super(SubmitGui, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('3DSMax Submission Tool')
        self.setWindowIcon(QtGui.QIcon("C:/Ringling/hpc/icons/hpcicon3-01.png"))
        self.head_node_field.addItems(HEAD_NODES)
        self.head_node_field.setCurrentIndex(randint(0,len(HEAD_NODES)-1))
        self.output_ext_field.addItems(IMAGE_EXT)
        self.output_ext_field.setCurrentIndex(IMAGE_EXT.index('.tga'))
        self._setup_validators()

    def _setup_validators(self):
        """
        Regex validators for title/output
        """
        self.title_field.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('^[A-Za-z0-9_\-\s]+$'), self))
        self.output_base_field.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('^[A-Za-z0-9_\-\.]+$'), self))
        
    def browse(self):
        filename = QtGui.QFileDialog.getOpenFileName(directory='Z:\\', filter="*.zip")
        if filename:
            self.scene_field.clear()
            self.project_field.setText(filename)
            zf = zipfile.ZipFile(open(filename,'rb'))
            self.scene_field.addItems([f for f in zf.namelist() if f.lower().endswith('.max')])
    
    @property
    def job_data(self):
        start_frame = min((int(self.start_field.value()), int(self.end_field.value())))
        end_frame = max((int(self.start_field.value()), int(self.end_field.value())))
        image_filename = str(self.output_base_field.text()) + str(self.output_ext_field.currentText())
        return {
                'renderer'  : 'max',
                'title'     : str(self.title_field.text()), 
                'project'   : os.path.normpath(str(self.project_field.text())),
                'scene'     : os.path.basename(str(self.scene_field.currentText())),
                'output'    : os.path.join(JOB_OUTPUT_UNC, getpass.getuser(), '{job_id}', 'output', image_filename), # job_id is injected by hpc-spool at the last minute 
                'start'     : start_frame,
                'end'       : end_frame,
                'step'      : str(self.step_field.value()),
                'threads'   : 0,
                'ext'       : str(self.output_ext_field.currentText())[1:]
                }
    
    def submit_job(self):
        try:
            spec = JobSpec(**self.job_data)
            # TODO: find a better place to do this.
            if not str(self.output_base_field.text()):
                raise RuntimeError("Output cannot be blank.")
            
            # Key env vars that influence submission
            os.environ['HEAD_NODE'] = str(self.head_node_field.currentText())
            spec.submit_job(pause=True if os.getenv('RRT_DEBUG', False) else False)
            self.quit()
            
        except Exception, e:
            alert = QtGui.QMessageBox(self)
            alert.setWindowTitle('Error')
            alert.setIcon(QtGui.QMessageBox.Warning)
            alert.setText(str(e))
            alert.exec_()
    
    def quit(self): 
        self.done(0)

def submit_gui():
    app = QtGui.QApplication(sys.argv)
    gui = SubmitGui()
    gui.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__': submit_gui()
