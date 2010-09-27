import sys
from PyQt4 import QtGui
from main import Ui_SubmitMainWindow

class SubmitGui(QtGui.QDialog, Ui_SubmitMainWindow):
    def __init__(self, parent=None):
        super(SubmitGui, self).__init__(parent)
        self.setupUi(self)
    
    def browse(self):
        filename = QtGui.QFileDialog.getOpenFileName()
        if filename:
            self.project_field.setText(filename)
    
    def submit_job(self): pass
    def quit(self): pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    gui = SubmitGui()
    gui.show()
    sys.exit(app.exec_())
