# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\rrt\maya\ui\submit.ui'
#
# Created: Wed Oct 24 16:19:16 2012
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SubmitMainWindow(object):
    def setupUi(self, SubmitMainWindow):
        SubmitMainWindow.setObjectName(_fromUtf8("SubmitMainWindow"))
        SubmitMainWindow.setEnabled(True)
        SubmitMainWindow.resize(445, 283)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SubmitMainWindow.sizePolicy().hasHeightForWidth())
        SubmitMainWindow.setSizePolicy(sizePolicy)
        SubmitMainWindow.setMinimumSize(QtCore.QSize(445, 283))
        SubmitMainWindow.setWindowTitle(_fromUtf8("hpc-submit-maya"))
        self.verticalLayout = QtGui.QVBoxLayout(SubmitMainWindow)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(8)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.head_node_label = QtGui.QLabel(SubmitMainWindow)
        self.head_node_label.setObjectName(_fromUtf8("head_node_label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.head_node_label)
        self.head_node_field = QtGui.QComboBox(SubmitMainWindow)
        self.head_node_field.setObjectName(_fromUtf8("head_node_field"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.head_node_field)
        self.title_label = QtGui.QLabel(SubmitMainWindow)
        self.title_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.title_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.title_label.setObjectName(_fromUtf8("title_label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.title_label)
        self.project_label = QtGui.QLabel(SubmitMainWindow)
        self.project_label.setMinimumSize(QtCore.QSize(0, 0))
        self.project_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.project_label.setObjectName(_fromUtf8("project_label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.project_label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.project_field = QtGui.QLineEdit(SubmitMainWindow)
        self.project_field.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.project_field.sizePolicy().hasHeightForWidth())
        self.project_field.setSizePolicy(sizePolicy)
        self.project_field.setMinimumSize(QtCore.QSize(161, 26))
        self.project_field.setReadOnly(True)
        self.project_field.setObjectName(_fromUtf8("project_field"))
        self.horizontalLayout.addWidget(self.project_field)
        self.browse_button = QtGui.QPushButton(SubmitMainWindow)
        self.browse_button.setMinimumSize(QtCore.QSize(85, 27))
        self.browse_button.setObjectName(_fromUtf8("browse_button"))
        self.horizontalLayout.addWidget(self.browse_button)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.scene_label = QtGui.QLabel(SubmitMainWindow)
        self.scene_label.setObjectName(_fromUtf8("scene_label"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.scene_label)
        self.horizontalLayout1 = QtGui.QHBoxLayout()
        self.horizontalLayout1.setSpacing(6)
        self.horizontalLayout1.setObjectName(_fromUtf8("horizontalLayout1"))
        self.scene_field = QtGui.QLineEdit(SubmitMainWindow)
        self.scene_field.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scene_field.sizePolicy().hasHeightForWidth())
        self.scene_field.setSizePolicy(sizePolicy)
        self.scene_field.setMinimumSize(QtCore.QSize(161, 26))
        self.scene_field.setReadOnly(True)
        self.scene_field.setObjectName(_fromUtf8("scene_field"))
        self.horizontalLayout1.addWidget(self.scene_field)
        self.scene_button = QtGui.QPushButton(SubmitMainWindow)
        self.scene_button.setMinimumSize(QtCore.QSize(85, 27))
        self.scene_button.setObjectName(_fromUtf8("scene_button"))
        self.horizontalLayout1.addWidget(self.scene_button)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout1)
        self.start_label = QtGui.QLabel(SubmitMainWindow)
        self.start_label.setObjectName(_fromUtf8("start_label"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.start_label)
        self.start_field = QtGui.QSpinBox(SubmitMainWindow)
        self.start_field.setMinimum(1)
        self.start_field.setMaximum(999999999)
        self.start_field.setObjectName(_fromUtf8("start_field"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.start_field)
        self.end_label = QtGui.QLabel(SubmitMainWindow)
        self.end_label.setObjectName(_fromUtf8("end_label"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.end_label)
        self.end_field = QtGui.QSpinBox(SubmitMainWindow)
        self.end_field.setMinimum(1)
        self.end_field.setMaximum(999999999)
        self.end_field.setObjectName(_fromUtf8("end_field"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.end_field)
        self.step_label = QtGui.QLabel(SubmitMainWindow)
        self.step_label.setObjectName(_fromUtf8("step_label"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.step_label)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.step_field = QtGui.QSpinBox(SubmitMainWindow)
        self.step_field.setMinimum(1)
        self.step_field.setMaximum(999999999)
        self.step_field.setObjectName(_fromUtf8("step_field"))
        self.horizontalLayout_11.addWidget(self.step_field)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout_11.addItem(spacerItem)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout_11.addItem(spacerItem1)
        spacerItem2 = QtGui.QSpacerItem(50, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout_11.addItem(spacerItem2)
        self.render_label = QtGui.QLabel(SubmitMainWindow)
        self.render_label.setObjectName(_fromUtf8("render_label"))
        self.horizontalLayout_11.addWidget(self.render_label)
        self.render_field = QtGui.QComboBox(SubmitMainWindow)
        self.render_field.setObjectName(_fromUtf8("render_field"))
        self.horizontalLayout_11.addWidget(self.render_field)
        spacerItem3 = QtGui.QSpacerItem(10, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout_11.addItem(spacerItem3)
        self.formLayout.setLayout(6, QtGui.QFormLayout.FieldRole, self.horizontalLayout_11)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.rrt_debug = QtGui.QCheckBox(SubmitMainWindow)
        self.rrt_debug.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rrt_debug.setObjectName(_fromUtf8("rrt_debug"))
        self.horizontalLayout_5.addWidget(self.rrt_debug)
        self.pause = QtGui.QCheckBox(SubmitMainWindow)
        self.pause.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pause.setObjectName(_fromUtf8("pause"))
        self.horizontalLayout_5.addWidget(self.pause)
        self.formLayout.setLayout(7, QtGui.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.title_field = QtGui.QLineEdit(SubmitMainWindow)
        self.title_field.setObjectName(_fromUtf8("title_field"))
        self.horizontalLayout_4.addWidget(self.title_field)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.verticalLayout.addLayout(self.formLayout)
        self.line = QtGui.QFrame(SubmitMainWindow)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.submit_button = QtGui.QPushButton(SubmitMainWindow)
        self.submit_button.setObjectName(_fromUtf8("submit_button"))
        self.horizontalLayout_2.addWidget(self.submit_button)
        self.cancel_button = QtGui.QPushButton(SubmitMainWindow)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.horizontalLayout_2.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(SubmitMainWindow)
        QtCore.QObject.connect(self.browse_button, QtCore.SIGNAL(_fromUtf8("clicked()")), SubmitMainWindow.browse)
        QtCore.QObject.connect(self.cancel_button, QtCore.SIGNAL(_fromUtf8("clicked()")), SubmitMainWindow.quit)
        QtCore.QObject.connect(self.submit_button, QtCore.SIGNAL(_fromUtf8("clicked()")), SubmitMainWindow.submit_job)
        QtCore.QObject.connect(self.scene_button, QtCore.SIGNAL(_fromUtf8("clicked()")), SubmitMainWindow.scene)
        QtCore.QMetaObject.connectSlotsByName(SubmitMainWindow)

    def retranslateUi(self, SubmitMainWindow):
        self.head_node_label.setToolTip(QtGui.QApplication.translate("SubmitMainWindow", "which cluster to use", None, QtGui.QApplication.UnicodeUTF8))
        self.head_node_label.setText(QtGui.QApplication.translate("SubmitMainWindow", "Head Node", None, QtGui.QApplication.UnicodeUTF8))
        self.head_node_field.setToolTip(QtGui.QApplication.translate("SubmitMainWindow", "Which cluster to submit to", None, QtGui.QApplication.UnicodeUTF8))
        self.title_label.setText(QtGui.QApplication.translate("SubmitMainWindow", "Job Title", None, QtGui.QApplication.UnicodeUTF8))
        self.project_label.setText(QtGui.QApplication.translate("SubmitMainWindow", "Project Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.browse_button.setText(QtGui.QApplication.translate("SubmitMainWindow", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.scene_label.setText(QtGui.QApplication.translate("SubmitMainWindow", "Maya Scene File", None, QtGui.QApplication.UnicodeUTF8))
        self.scene_button.setText(QtGui.QApplication.translate("SubmitMainWindow", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.start_label.setText(QtGui.QApplication.translate("SubmitMainWindow", "Start Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.end_label.setText(QtGui.QApplication.translate("SubmitMainWindow", "End Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.step_label.setText(QtGui.QApplication.translate("SubmitMainWindow", "Frame Step", None, QtGui.QApplication.UnicodeUTF8))
        self.render_label.setText(QtGui.QApplication.translate("SubmitMainWindow", "Renderer", None, QtGui.QApplication.UnicodeUTF8))
        self.rrt_debug.setText(QtGui.QApplication.translate("SubmitMainWindow", "Show Debug Messages", None, QtGui.QApplication.UnicodeUTF8))
        self.pause.setText(QtGui.QApplication.translate("SubmitMainWindow", "Pause before exit", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_button.setText(QtGui.QApplication.translate("SubmitMainWindow", "Submit Job", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_button.setText(QtGui.QApplication.translate("SubmitMainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
