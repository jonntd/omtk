# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/nodegraph/ui/nodegraph_widget.ui'
#
# Created: Wed Apr  4 19:57:25 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2880, 1278)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.widget_toolbar = WidgetToolbar(MainWindow)
        self.widget_toolbar.setObjectName("widget_toolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.widget_toolbar)
        MainWindow.insertToolBarBreak(self.widget_toolbar)
        self.toolBar_arrange = QtWidgets.QToolBar(MainWindow)
        self.toolBar_arrange.setObjectName("toolBar_arrange")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_arrange)
        self.actionAdd = QtWidgets.QAction(MainWindow)
        self.actionAdd.setObjectName("actionAdd")
        self.actionRemove = QtWidgets.QAction(MainWindow)
        self.actionRemove.setObjectName("actionRemove")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionExpand = QtWidgets.QAction(MainWindow)
        self.actionExpand.setObjectName("actionExpand")
        self.actionCollapse = QtWidgets.QAction(MainWindow)
        self.actionCollapse.setObjectName("actionCollapse")
        self.actionGoDown = QtWidgets.QAction(MainWindow)
        self.actionGoDown.setObjectName("actionGoDown")
        self.actionGoUp = QtWidgets.QAction(MainWindow)
        self.actionGoUp.setObjectName("actionGoUp")
        self.actionGroup = QtWidgets.QAction(MainWindow)
        self.actionGroup.setObjectName("actionGroup")
        self.actionUngroup = QtWidgets.QAction(MainWindow)
        self.actionUngroup.setObjectName("actionUngroup")
        self.actionMatchMayaEditorPositions = QtWidgets.QAction(MainWindow)
        self.actionMatchMayaEditorPositions.setObjectName("actionMatchMayaEditorPositions")
        self.actionLayoutUpstream = QtWidgets.QAction(MainWindow)
        self.actionLayoutUpstream.setObjectName("actionLayoutUpstream")
        self.actionLayoutDownstream = QtWidgets.QAction(MainWindow)
        self.actionLayoutDownstream.setObjectName("actionLayoutDownstream")
        self.actionLayoutSpring = QtWidgets.QAction(MainWindow)
        self.actionLayoutSpring.setObjectName("actionLayoutSpring")
        self.actionLayoutRecenter = QtWidgets.QAction(MainWindow)
        self.actionLayoutRecenter.setObjectName("actionLayoutRecenter")
        self.actionExpandMore = QtWidgets.QAction(MainWindow)
        self.actionExpandMore.setObjectName("actionExpandMore")
        self.actionExpandMoreMore = QtWidgets.QAction(MainWindow)
        self.actionExpandMoreMore.setObjectName("actionExpandMoreMore")
        self.actionFrameAll = QtWidgets.QAction(MainWindow)
        self.actionFrameAll.setObjectName("actionFrameAll")
        self.actionFrameSelected = QtWidgets.QAction(MainWindow)
        self.actionFrameSelected.setObjectName("actionFrameSelected")
        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addAction(self.actionRemove)
        self.toolBar.addAction(self.actionClear)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionGoUp)
        self.toolBar.addAction(self.actionGoDown)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionGroup)
        self.toolBar.addAction(self.actionUngroup)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExpand)
        self.toolBar.addAction(self.actionExpandMore)
        self.toolBar.addAction(self.actionExpandMoreMore)
        self.toolBar.addAction(self.actionCollapse)
        self.toolBar.addAction(self.actionFrameAll)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionLayoutSpring)
        self.toolBar.addAction(self.actionLayoutDownstream)
        self.toolBar.addAction(self.actionFrameSelected)
        self.toolBar.addAction(self.actionLayoutRecenter)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.toolBar.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "toolBar", None, -1))
        self.widget_toolbar.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "toolBar_2", None, -1))
        self.toolBar_arrange.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "toolBar_2", None, -1))
        self.actionAdd.setText(QtWidgets.QApplication.translate("MainWindow", "Add", None, -1))
        self.actionRemove.setText(QtWidgets.QApplication.translate("MainWindow", "Remove", None, -1))
        self.actionClear.setText(QtWidgets.QApplication.translate("MainWindow", "Clear", None, -1))
        self.actionExpand.setText(QtWidgets.QApplication.translate("MainWindow", "Expand", None, -1))
        self.actionCollapse.setText(QtWidgets.QApplication.translate("MainWindow", "Collapse", None, -1))
        self.actionGoDown.setText(QtWidgets.QApplication.translate("MainWindow", "Go Down", None, -1))
        self.actionGoUp.setText(QtWidgets.QApplication.translate("MainWindow", "Go Up", None, -1))
        self.actionGroup.setText(QtWidgets.QApplication.translate("MainWindow", "Group", None, -1))
        self.actionUngroup.setText(QtWidgets.QApplication.translate("MainWindow", "Ungroup", None, -1))
        self.actionMatchMayaEditorPositions.setText(QtWidgets.QApplication.translate("MainWindow", "&Sync to Maya Node Editor", None, -1))
        self.actionLayoutUpstream.setText(QtWidgets.QApplication.translate("MainWindow", "&Layout Upstream", None, -1))
        self.actionLayoutDownstream.setText(QtWidgets.QApplication.translate("MainWindow", "Layout &Downstream", None, -1))
        self.actionLayoutSpring.setText(QtWidgets.QApplication.translate("MainWindow", "La&yout Spring", None, -1))
        self.actionLayoutRecenter.setText(QtWidgets.QApplication.translate("MainWindow", "Recenter", None, -1))
        self.actionExpandMore.setText(QtWidgets.QApplication.translate("MainWindow", "Expand 2x", None, -1))
        self.actionExpandMoreMore.setText(QtWidgets.QApplication.translate("MainWindow", "Expand 3x", None, -1))
        self.actionFrameAll.setText(QtWidgets.QApplication.translate("MainWindow", "Frame All", None, -1))
        self.actionFrameSelected.setText(QtWidgets.QApplication.translate("MainWindow", "Frame Selected", None, -1))

from ...widget_toolbar import WidgetToolbar
