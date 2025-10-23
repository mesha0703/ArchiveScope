# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'controller_frame.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_fr_controller(object):
    def setupUi(self, fr_controller):
        if not fr_controller.objectName():
            fr_controller.setObjectName(u"fr_controller")
        fr_controller.resize(400, 300)
        fr_controller.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayout = QVBoxLayout(fr_controller)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_controller_name = QLabel(fr_controller)
        self.lbl_controller_name.setObjectName(u"lbl_controller_name")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_controller_name.sizePolicy().hasHeightForWidth())
        self.lbl_controller_name.setSizePolicy(sizePolicy)
        self.lbl_controller_name.setMaximumSize(QSize(16777215, 18))

        self.verticalLayout.addWidget(self.lbl_controller_name)

        self.fr_controllerParams = QFrame(fr_controller)
        self.fr_controllerParams.setObjectName(u"fr_controllerParams")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.fr_controllerParams.sizePolicy().hasHeightForWidth())
        self.fr_controllerParams.setSizePolicy(sizePolicy1)
        self.fr_controllerParams.setStyleSheet(u"QFrame {\n"
"    border-top: 1px solid #999999;\n"
"    border-left: none;\n"
"    border-right: none;\n"
"    border-bottom: none;\n"
"}")
        self.fr_controllerParams.setFrameShape(QFrame.Shape.StyledPanel)
        self.fr_controllerParams.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.fr_controllerParams)


        self.retranslateUi(fr_controller)

        QMetaObject.connectSlotsByName(fr_controller)
    # setupUi

    def retranslateUi(self, fr_controller):
        fr_controller.setWindowTitle(QCoreApplication.translate("fr_controller", u"Frame", None))
        self.lbl_controller_name.setText(QCoreApplication.translate("fr_controller", u"Regler", None))
    # retranslateUi

