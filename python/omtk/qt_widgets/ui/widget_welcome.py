# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/ui/widget_welcome.ui'
#
# Created: Wed Dec 20 20:39:33 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(952, 626)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_create_rig_default = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_create_rig_default.sizePolicy().hasHeightForWidth())
        self.btn_create_rig_default.setSizePolicy(sizePolicy)
        self.btn_create_rig_default.setMinimumSize(QtCore.QSize(0, 84))
        self.btn_create_rig_default.setObjectName("btn_create_rig_default")
        self.verticalLayout_2.addWidget(self.btn_create_rig_default)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.tableView_types_rig = QtWidgets.QTableView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_types_rig.sizePolicy().hasHeightForWidth())
        self.tableView_types_rig.setSizePolicy(sizePolicy)
        self.tableView_types_rig.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView_types_rig.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView_types_rig.setObjectName("tableView_types_rig")
        self.tableView_types_rig.horizontalHeader().setVisible(False)
        self.tableView_types_rig.horizontalHeader().setStretchLastSection(True)
        self.tableView_types_rig.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.tableView_types_rig)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_create_rig_template = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_create_rig_template.sizePolicy().hasHeightForWidth())
        self.btn_create_rig_template.setSizePolicy(sizePolicy)
        self.btn_create_rig_template.setMinimumSize(QtCore.QSize(0, 84))
        self.btn_create_rig_template.setObjectName("btn_create_rig_template")
        self.verticalLayout.addWidget(self.btn_create_rig_template)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.tableView_types_template = QtWidgets.QTableView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_types_template.sizePolicy().hasHeightForWidth())
        self.tableView_types_template.setSizePolicy(sizePolicy)
        self.tableView_types_template.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView_types_template.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView_types_template.setObjectName("tableView_types_template")
        self.tableView_types_template.horizontalHeader().setVisible(False)
        self.tableView_types_template.horizontalHeader().setStretchLastSection(True)
        self.tableView_types_template.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableView_types_template)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn_start = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_start.sizePolicy().hasHeightForWidth())
        self.btn_start.setSizePolicy(sizePolicy)
        self.btn_start.setMinimumSize(QtCore.QSize(0, 84))
        self.btn_start.setObjectName("btn_start")
        self.verticalLayout_3.addWidget(self.btn_start)
        spacerItem2 = QtWidgets.QSpacerItem(17, 78, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_4.addWidget(self.checkBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form"))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Welcome!"))
        self.btn_create_rig_default.setText(QtWidgets.QApplication.translate("Form", "Start from a rig"))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "Available rigs:"))
        self.btn_create_rig_template.setText(QtWidgets.QApplication.translate("Form", "Start from a template"))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "Available templates"))
        self.btn_start.setText(QtWidgets.QApplication.translate("Form", "Start from scratch"))
        self.checkBox.setText(QtWidgets.QApplication.translate("Form", "show at startup"))

