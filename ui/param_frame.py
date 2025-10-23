# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'param_frame.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)
from . import resources_rc

class Ui_fr_param(object):
    def setupUi(self, fr_param):
        if not fr_param.objectName():
            fr_param.setObjectName(u"fr_param")
        fr_param.resize(400, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(fr_param.sizePolicy().hasHeightForWidth())
        fr_param.setSizePolicy(sizePolicy)
        fr_param.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(255, 255, 255);\n"
"	border: none;\n"
"}")
        self.horizontalLayout = QHBoxLayout(fr_param)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_param_str = QLabel(fr_param)
        self.lbl_param_str.setObjectName(u"lbl_param_str")

        self.horizontalLayout.addWidget(self.lbl_param_str)

        self.lbl_meaning = QLabel(fr_param)
        self.lbl_meaning.setObjectName(u"lbl_meaning")

        self.horizontalLayout.addWidget(self.lbl_meaning)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pb_reset = QPushButton(fr_param)
        self.pb_reset.setObjectName(u"pb_reset")
        self.pb_reset.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/resources/reset_24dp.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_reset.setIcon(icon)
        self.pb_reset.setIconSize(QSize(18, 18))

        self.horizontalLayout.addWidget(self.pb_reset)

        self.dsb_value = QDoubleSpinBox(fr_param)
        self.dsb_value.setObjectName(u"dsb_value")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dsb_value.sizePolicy().hasHeightForWidth())
        self.dsb_value.setSizePolicy(sizePolicy1)
        self.dsb_value.setMinimumSize(QSize(100, 0))
        self.dsb_value.setMaximumSize(QSize(150, 16777215))
        self.dsb_value.setMinimum(-100000.000000000000000)
        self.dsb_value.setMaximum(100000.000000000000000)

        self.horizontalLayout.addWidget(self.dsb_value)


        self.retranslateUi(fr_param)

        QMetaObject.connectSlotsByName(fr_param)
    # setupUi

    def retranslateUi(self, fr_param):
        fr_param.setWindowTitle(QCoreApplication.translate("fr_param", u"Frame", None))
        self.lbl_param_str.setText(QCoreApplication.translate("fr_param", u"p_empty", None))
        self.lbl_meaning.setText(QCoreApplication.translate("fr_param", u"Description", None))
        self.pb_reset.setText("")
    # retranslateUi

