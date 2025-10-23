# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bitconfig_single_bit.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)
from . import resources_rc

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(400, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Frame.sizePolicy().hasHeightForWidth())
        Frame.setSizePolicy(sizePolicy)
        Frame.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.horizontalLayout = QHBoxLayout(Frame)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_meaning = QLabel(Frame)
        self.lbl_meaning.setObjectName(u"lbl_meaning")
        self.lbl_meaning.setMaximumSize(QSize(16777215, 16777215))
        self.lbl_meaning.setWordWrap(False)

        self.horizontalLayout.addWidget(self.lbl_meaning)

        self.horizontalSpacer = QSpacerItem(192, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pb_reset = QPushButton(Frame)
        self.pb_reset.setObjectName(u"pb_reset")
        self.pb_reset.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/resources/reset_24dp.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_reset.setIcon(icon)
        self.pb_reset.setIconSize(QSize(18, 18))

        self.horizontalLayout.addWidget(self.pb_reset)

        self.checkBox = QCheckBox(Frame)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout.addWidget(self.checkBox)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.lbl_meaning.setText(QCoreApplication.translate("Frame", u"bitconfig_str", None))
        self.pb_reset.setText("")
        self.checkBox.setText("")
    # retranslateUi

