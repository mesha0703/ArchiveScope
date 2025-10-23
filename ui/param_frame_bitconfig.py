# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'param_frame_bitconfig.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QWidget)
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
        self.gridLayout = QGridLayout(fr_param)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_meaning = QLabel(fr_param)
        self.lbl_meaning.setObjectName(u"lbl_meaning")

        self.gridLayout.addWidget(self.lbl_meaning, 0, 1, 1, 1)

        self.pb_param = QPushButton(fr_param)
        self.pb_param.setObjectName(u"pb_param")
        self.pb_param.setStyleSheet(u"border: none;")
        icon = QIcon()
        icon.addFile(u":/resources/arrow_right_24dp.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_param.setIcon(icon)

        self.gridLayout.addWidget(self.pb_param, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.lbl_value = QLabel(fr_param)
        self.lbl_value.setObjectName(u"lbl_value")

        self.gridLayout.addWidget(self.lbl_value, 0, 3, 1, 1)

        self.w_bit_config = QWidget(fr_param)
        self.w_bit_config.setObjectName(u"w_bit_config")

        self.gridLayout.addWidget(self.w_bit_config, 1, 0, 1, 4)


        self.retranslateUi(fr_param)

        QMetaObject.connectSlotsByName(fr_param)
    # setupUi

    def retranslateUi(self, fr_param):
        fr_param.setWindowTitle(QCoreApplication.translate("fr_param", u"Frame", None))
        self.lbl_meaning.setText(QCoreApplication.translate("fr_param", u"Description", None))
        self.pb_param.setText(QCoreApplication.translate("fr_param", u"p0000[0]", None))
        self.lbl_value.setText(QCoreApplication.translate("fr_param", u"Value", None))
    # retranslateUi

