import sys, zipfile
from PyQt4 import QtGui
from main import Ui_SubmitMainWindow

class SubmitGui(QtGui.QDialog, Ui_SubmitMainWindow):
    def __init__(self, parent=None):
        super(SubmitGui, self).__init__(parent)
        self.setupUi(self)
    
    def browse(self):
        filename = QtGui.QFileDialog.getOpenFileName(filter="*.zip")
        self.scene_field.clear()
        if filename:
            self.project_field.setText(filename)
            zf = zipfile.ZipFile(open(filename,'rb'))
            self.scene_field.addItems([f for f in zf.namelist() if f.lower().endswith('.max')])
    
    def submit_job(self): 
        self.quit()
    def quit(self): 
        self.done(0)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    gui = SubmitGui()
    gui.show()
    sys.exit(app.exec_())
