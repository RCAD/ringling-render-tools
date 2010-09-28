import sys, zipfile
from PyQt4 import QtGui
from rrt.max.ui.submit import Ui_SubmitMainWindow
from pkg_resources import Requirement, resource_filename

class SubmitGui(QtGui.QDialog, Ui_SubmitMainWindow):
    def __init__(self, parent=None):
        super(SubmitGui, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('hpc-submit-max')
        icon = resource_filename(Requirement.parse("ringling-render-tools"), "rrt/extras/hpcicon3-01.png")
        self.setWindowIcon(QtGui.QIcon(icon))
    
    def browse(self):
        filename = QtGui.QFileDialog.getOpenFileName(directory='Z:\\', filter="*.zip")
        if filename:
            self.scene_field.clear()
            self.project_field.setText(filename)
            zf = zipfile.ZipFile(open(filename,'rb'))
            self.scene_field.addItems([f for f in zf.namelist() if f.lower().endswith('.max')])
    
    def submit_job(self): 
        # TODO: validate
        # TODO: generate ini
        # TODO: os.system(hpc-spool....)
        self.quit()
    
    def quit(self): 
        self.done(0)

def submit_gui():
    app = QtGui.QApplication(sys.argv)
    gui = SubmitGui()
    gui.show()
    sys.exit(app.exec_())
