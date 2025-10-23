# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cw_kinematic_tree.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QHBoxLayout,
    QLabel, QScrollArea, QSizePolicy, QVBoxLayout,
    QWidget)
from . import resources_rc

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.fr_main = QFrame(Frame)
        self.fr_main.setObjectName(u"fr_main")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr_main.sizePolicy().hasHeightForWidth())
        self.fr_main.setSizePolicy(sizePolicy)
        self.fr_main.setMinimumSize(QSize(0, 0))
        self.fr_main.setMaximumSize(QSize(16777215, 16777215))
        self.fr_main.setStyleSheet(u"#fr_main {\n"
"	background-color: rgb(255, 255, 255);\n"
"	border: 2px grey;\n"
"	border-color: rgb(50,50,50);\n"
"	border-radius: 10px;\n"
"}")
        self.fr_main.setFrameShape(QFrame.Shape.StyledPanel)
        self.fr_main.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.fr_main)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.sa_main = QScrollArea(self.fr_main)
        self.sa_main.setObjectName(u"sa_main")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.sa_main.sizePolicy().hasHeightForWidth())
        self.sa_main.setSizePolicy(sizePolicy1)
        self.sa_main.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.sa_main.setFrameShape(QFrame.Shape.NoFrame)
        self.sa_main.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sa_main.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.sa_main.setWidgetResizable(True)
        self.sa_mainContents = QWidget()
        self.sa_mainContents.setObjectName(u"sa_mainContents")
        self.sa_mainContents.setGeometry(QRect(0, 0, 352, 252))
        self.sa_mainContents.setStyleSheet(u"")
        self.sa_mainContents_layout = QVBoxLayout(self.sa_mainContents)
        self.sa_mainContents_layout.setSpacing(0)
        self.sa_mainContents_layout.setObjectName(u"sa_mainContents_layout")
        self.sa_mainContents_layout.setContentsMargins(0, 0, 0, 0)
        self.w_archiveInfo = QWidget(self.sa_mainContents)
        self.w_archiveInfo.setObjectName(u"w_archiveInfo")
        self.horizontalLayout = QHBoxLayout(self.w_archiveInfo)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lbl_archiveName = QLabel(self.w_archiveInfo)
        self.lbl_archiveName.setObjectName(u"lbl_archiveName")

        self.horizontalLayout.addWidget(self.lbl_archiveName)

        self.lbl_archiveNameValue = QLabel(self.w_archiveInfo)
        self.lbl_archiveNameValue.setObjectName(u"lbl_archiveNameValue")
        self.lbl_archiveNameValue.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.lbl_archiveNameValue)


        self.sa_mainContents_layout.addWidget(self.w_archiveInfo)

        self.sa_main.setWidget(self.sa_mainContents)

        self.verticalLayout_2.addWidget(self.sa_main)


        self.verticalLayout.addWidget(self.fr_main)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.lbl_archiveName.setText(QCoreApplication.translate("Frame", u"Archive: ", None))
        self.lbl_archiveNameValue.setText(QCoreApplication.translate("Frame", u"TextLabel", None))
    # retranslateUi

