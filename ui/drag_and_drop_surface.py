# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'archive_dragAndDrop.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from ui.drop_label import DropLabel
from . import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        self.frame.setStyleSheet(u"#frame {\n"
"    background-color: rgb(202, 204, 204);\n"
"    border-color: rgb(50,50,50);\n"
"    border-radius: 10px;\n"
"}")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.w_addArchive = QWidget(self.frame)
        self.w_addArchive.setObjectName(u"w_addArchive")
        self.w_addArchive.setStyleSheet(u"#w_addArchive {\n"
"    background-color: rgb(202, 204, 204);\n"
"    border: 2px rgb(50,50,50);\n"
"    border-color: rgb(50,50,50);\n"
"    border-radius: 10px;\n"
"}")
        self.gridLayout_2 = QGridLayout(self.w_addArchive)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(0)
        self.fr_dragAndDropZone = DropLabel(self.w_addArchive)
        self.fr_dragAndDropZone.setObjectName(u"fr_dragAndDropZone")
        self.fr_dragAndDropZone.setMinimumSize(QSize(320, 100))
        self.fr_dragAndDropZone.setAcceptDrops(True)
        self.fr_dragAndDropZone.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.fr_dragAndDropZone.setStyleSheet(u"#fr_dragAndDropZone {\n"
"    border: 2px dashed rgb(193, 197, 197);\n"
"    border-radius: 10px;\n"
"    background-color: rgb(255, 255, 255)\n"
"}")
        self.fr_dragAndDropZone.setFrameShape(QFrame.Shape.StyledPanel)
        self.fr_dragAndDropZone.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.fr_dragAndDropZone)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(0)
        self.gridLayout_3.setVerticalSpacing(5)
        self.horizontalSpacer = QSpacerItem(115, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 4, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(115, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 4, 3, 1, 1)

        self.pb_browseFiles = QPushButton(self.fr_dragAndDropZone)
        self.pb_browseFiles.setObjectName(u"pb_browseFiles")
        self.pb_browseFiles.setMinimumSize(QSize(0, 20))
        self.pb_browseFiles.setMaximumSize(QSize(100, 16777215))
        self.pb_browseFiles.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(202, 201, 203);\n"
"	border-radius: 4px;\n"
"	padding: 4px 4px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	border-color: rgb(1, 153, 153);\n"
"	color: rgb(1, 153, 153);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	border-color: rgb(1, 100, 100);\n"
"	color: rgb(1, 100, 100);\n"
"}")

        self.gridLayout_3.addWidget(self.pb_browseFiles, 4, 2, 1, 1)

        self.label = QLabel(self.fr_dragAndDropZone)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 2, 1, 1, 3)

        self.label_2 = QLabel(self.fr_dragAndDropZone)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_2, 3, 1, 1, 3)


        self.gridLayout_2.addWidget(self.fr_dragAndDropZone, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.w_addArchive)

        self.w_empty = QWidget(self.frame)
        self.w_empty.setObjectName(u"w_empty")
        self.w_empty.setStyleSheet(u"#w_empty {\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-bottom-left-radius: 10px;\n"
"    border-bottom-right-radius: 10px;\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.w_empty)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer = QSpacerItem(20, 123, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.w_empty)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pb_browseFiles.setText(QCoreApplication.translate("Form", u"Datei w\u00e4hlen", None))
        self.label.setText(QCoreApplication.translate("Form", u"Siemens-Archiv hierher ziehen", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"oder", None))
    # retranslateUi

