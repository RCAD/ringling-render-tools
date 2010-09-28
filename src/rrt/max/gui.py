import sys, zipfile
from PyQt4 import QtGui
from rrt.max.ui.submit import Ui_SubmitMainWindow
from rrt.jobspec import JobSpec

class SubmitGui(QtGui.QDialog, Ui_SubmitMainWindow):
    def __init__(self, parent=None):
        super(SubmitGui, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('hpc-submit-max')
        self.setWindowIcon(QtGui.QIcon("C:/Ringling/hpc/icons/hpcicon3-01.png"))
    
    def browse(self):
        filename = QtGui.QFileDialog.getOpenFileName(directory='Z:\\', filter="*.zip")
        if filename:
            self.scene_field.clear()
            self.project_field.setText(filename)
            zf = zipfile.ZipFile(open(filename,'rb'))
            self.scene_field.addItems([f for f in zf.namelist() if f.lower().endswith('.max')])
    @property
    def job_data(self):
        return {
                'project': self.project_field.getText()
                }
    
    def submit_job(self): 
        # TODO: validate
        spec = JobSpec(self.job_data, lambda x: True)
        # TODO: os.system(hpc-spool....)
        self.quit()
    
    def quit(self): 
        print self.job_data
        self.done(0)

def submit_gui():
    app = QtGui.QApplication(sys.argv)
    gui = SubmitGui()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__': 
    submit_gui()
