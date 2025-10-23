# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QWidget)
from . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMaximumSize(QSize(1920, 1080))
        icon = QIcon()
        icon.addFile(u"../../resources/ArchiveScope_icon.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        MainWindow.setDocumentMode(False)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionCloseProject = QAction(MainWindow)
        self.actionCloseProject.setObjectName(u"actionCloseProject")
        self.actionRemoveArchive = QAction(MainWindow)
        self.actionRemoveArchive.setObjectName(u"actionRemoveArchive")
        self.actionPrint = QAction(MainWindow)
        self.actionPrint.setObjectName(u"actionPrint")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionAbout_ArchiveScope = QAction(MainWindow)
        self.actionAbout_ArchiveScope.setObjectName(u"actionAbout_ArchiveScope")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionClose_ArchiveScope = QAction(MainWindow)
        self.actionClose_ArchiveScope.setObjectName(u"actionClose_ArchiveScope")
        self.actionExportArchive = QAction(MainWindow)
        self.actionExportArchive.setObjectName(u"actionExportArchive")
        self.actionAddArchive_BrowseFiles = QAction(MainWindow)
        self.actionAddArchive_BrowseFiles.setObjectName(u"actionAddArchive_BrowseFiles")
        self.actionAddArchive_Window = QAction(MainWindow)
        self.actionAddArchive_Window.setObjectName(u"actionAddArchive_Window")
        self.actionRemove = QAction(MainWindow)
        self.actionRemove.setObjectName(u"actionRemove")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.actionAddArchive_Browse = QAction(MainWindow)
        self.actionAddArchive_Browse.setObjectName(u"actionAddArchive_Browse")
        self.actionAddWindow = QAction(MainWindow)
        self.actionAddWindow.setObjectName(u"actionAddWindow")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.fr_archivesSurface = QFrame(self.widget)
        self.fr_archivesSurface.setObjectName(u"fr_archivesSurface")
        self.fr_archivesSurface.setStyleSheet(u"QFrame {\n"
"    border: none;\n"
"    background-color: rgb(234, 238, 238)\n"
"}\n"
"")
        self.fr_archivesSurface.setFrameShape(QFrame.Shape.StyledPanel)
        self.fr_archivesSurface.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.fr_archivesSurface, 2, 0, 1, 1)

        self.wg_maintools = QWidget(self.widget)
        self.wg_maintools.setObjectName(u"wg_maintools")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wg_maintools.sizePolicy().hasHeightForWidth())
        self.wg_maintools.setSizePolicy(sizePolicy)
        self.wg_maintools.setMaximumSize(QSize(16777215, 80))
        self.gridLayout_2 = QGridLayout(self.wg_maintools)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(5)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setContentsMargins(10, 10, 10, 0)
        self.tabWidget = QTabWidget(self.wg_maintools)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tabWidget.setMinimumSize(QSize(520, 0))
        self.tabWidget.setMaximumSize(QSize(520, 26))
        self.tabWidget.setStyleSheet(u"QTabWidget::pane {\n"
"    background: rgb(234, 238, 238);\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background: white;\n"
"    color: black;\n"
"    padding: 4px 0px;\n"
"    border: 1px solid #ccc;\n"
"    border-bottom: 2px solid rgb(234, 238, 238);\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 100px;\n"
"    max-width: 120px;\n"
"    font-size: 10px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background: rgb(234, 238, 238);\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background: #eaeaea;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: none;\n"
"    height: 0px;\n"
"}\n"
"")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.tabWidget.addTab(self.tab_5, "")

        self.gridLayout_2.addWidget(self.tabWidget, 2, 0, 1, 1)

        self.pb_compare = QPushButton(self.wg_maintools)
        self.pb_compare.setObjectName(u"pb_compare")
        self.pb_compare.setStyleSheet(u"border: none;")
        icon1 = QIcon()
        icon1.addFile(u":/resources/equal_blck_24dp.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_compare.setIcon(icon1)
        self.pb_compare.setIconSize(QSize(16, 16))

        self.gridLayout_2.addWidget(self.pb_compare, 0, 3, 1, 1)

        self.pb_addArchive = QPushButton(self.wg_maintools)
        self.pb_addArchive.setObjectName(u"pb_addArchive")
        self.pb_addArchive.setStyleSheet(u"border: none;")
        icon2 = QIcon()
        icon2.addFile(u":/resources/add_blck_24dp.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_addArchive.setIcon(icon2)
        self.pb_addArchive.setIconSize(QSize(16, 16))

        self.gridLayout_2.addWidget(self.pb_addArchive, 0, 4, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 1, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 2, 2, 1, 1)


        self.gridLayout.addWidget(self.wg_maintools, 1, 0, 1, 1)


        self.horizontalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setStyleSheet(u"QMenu { background: #2b2b2b; color: #f0f0f0; }\n"
"QMenu::item:selected { background: #3a3a3a; color: #ffffff; }\n"
"QToolTip { color: #111; background: #ffffe1; border: 1px solid #b7b7b7; }")
        self.menuArchiv_hinzuf_gen = QMenu(self.menuFile)
        self.menuArchiv_hinzuf_gen.setObjectName(u"menuArchiv_hinzuf_gen")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.menuArchiv_hinzuf_gen.menuAction())
        self.menuFile.addAction(self.actionRemove)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport)
        self.menuArchiv_hinzuf_gen.addAction(self.actionAddArchive_Browse)
        self.menuArchiv_hinzuf_gen.addAction(self.actionAddWindow)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ArchiveScope", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New Project", None))
        self.actionCloseProject.setText(QCoreApplication.translate("MainWindow", u"Close Project", None))
        self.actionRemoveArchive.setText(QCoreApplication.translate("MainWindow", u"Remove Archive", None))
        self.actionPrint.setText(QCoreApplication.translate("MainWindow", u"Export PDF", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.actionAbout_ArchiveScope.setText(QCoreApplication.translate("MainWindow", u"About ArchiveScope", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionClose_ArchiveScope.setText(QCoreApplication.translate("MainWindow", u"Close ArchiveScope", None))
        self.actionExportArchive.setText(QCoreApplication.translate("MainWindow", u"Export Archive", None))
        self.actionAddArchive_BrowseFiles.setText(QCoreApplication.translate("MainWindow", u"Browse Files", None))
        self.actionAddArchive_Window.setText(QCoreApplication.translate("MainWindow", u"Add Archive Window", None))
        self.actionRemove.setText(QCoreApplication.translate("MainWindow", u"Archiv entfernen", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Archiv exportieren", None))
        self.actionAddArchive_Browse.setText(QCoreApplication.translate("MainWindow", u"Datei w\u00e4hlen", None))
        self.actionAddWindow.setText(QCoreApplication.translate("MainWindow", u"Fenster hinzuf\u00fcgen", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"Stromsollwert", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Drehzahlsollwert", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Drehzahlistwert", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Reglerparameter", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Kin. Kette", None))
        self.pb_compare.setText("")
        self.pb_addArchive.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"Datei", None))
        self.menuArchiv_hinzuf_gen.setTitle(QCoreApplication.translate("MainWindow", u"Archiv hinzuf\u00fcgen", None))
    # retranslateUi

