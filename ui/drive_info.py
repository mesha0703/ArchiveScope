# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cw_archiveDriveInfo.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
from . import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(424, 300)
        Form.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.fr_main = QFrame(Form)
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
        self.sa_mainContents.setGeometry(QRect(0, 0, 376, 252))
        self.sa_mainContents.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.sa_mainContents)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.w_driveInfo = QWidget(self.sa_mainContents)
        self.w_driveInfo.setObjectName(u"w_driveInfo")
        self.w_driveInfo.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.w_driveInfo)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setContentsMargins(10, 10, 10, 0)
        self.lbl_archiveName = QLabel(self.w_driveInfo)
        self.lbl_archiveName.setObjectName(u"lbl_archiveName")

        self.gridLayout.addWidget(self.lbl_archiveName, 0, 0, 1, 1)

        self.w_activeFiltersNum = QWidget(self.w_driveInfo)
        self.w_activeFiltersNum.setObjectName(u"w_activeFiltersNum")
        self.horizontalLayout = QHBoxLayout(self.w_activeFiltersNum)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 0, 10, 0)
        self.lbl_numActiveFilters = QLabel(self.w_activeFiltersNum)
        self.lbl_numActiveFilters.setObjectName(u"lbl_numActiveFilters")

        self.horizontalLayout.addWidget(self.lbl_numActiveFilters)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pb_numActiveFilters = QPushButton(self.w_activeFiltersNum)
        self.pb_numActiveFilters.setObjectName(u"pb_numActiveFilters")
        self.pb_numActiveFilters.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/resources/reset_24dp.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_numActiveFilters.setIcon(icon)
        self.pb_numActiveFilters.setIconSize(QSize(18, 18))

        self.horizontalLayout.addWidget(self.pb_numActiveFilters)

        self.cb_numActiveFilters = QComboBox(self.w_activeFiltersNum)
        self.cb_numActiveFilters.setObjectName(u"cb_numActiveFilters")
        self.cb_numActiveFilters.setStyleSheet(u"selection-color: rgb(1, 153, 153);")

        self.horizontalLayout.addWidget(self.cb_numActiveFilters)


        self.gridLayout.addWidget(self.w_activeFiltersNum, 5, 0, 1, 2)

        self.lbl_drives = QLabel(self.w_driveInfo)
        self.lbl_drives.setObjectName(u"lbl_drives")

        self.gridLayout.addWidget(self.lbl_drives, 1, 0, 1, 1)

        self.w_filters = QWidget(self.w_driveInfo)
        self.w_filters.setObjectName(u"w_filters")

        self.gridLayout.addWidget(self.w_filters, 6, 0, 1, 2)

        self.w_plot = QWidget(self.w_driveInfo)
        self.w_plot.setObjectName(u"w_plot")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.w_plot.sizePolicy().hasHeightForWidth())
        self.w_plot.setSizePolicy(sizePolicy2)
        self.w_plot.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.w_plot, 4, 0, 1, 2)

        self.pb_moreInfo = QPushButton(self.w_driveInfo)
        self.pb_moreInfo.setObjectName(u"pb_moreInfo")
        self.pb_moreInfo.setStyleSheet(u"text-align: left;\n"
"padding-left: 0px; /* shifts text from the edge */\n"
"border: none\n"
"\n"
"")
        icon1 = QIcon()
        icon1.addFile(u":/resources/arrow_right_24dp.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_moreInfo.setIcon(icon1)

        self.gridLayout.addWidget(self.pb_moreInfo, 2, 0, 1, 1)

        self.cb_driveNames = QComboBox(self.w_driveInfo)
        self.cb_driveNames.setObjectName(u"cb_driveNames")
        self.cb_driveNames.setStyleSheet(u"selection-color: rgb(1, 153, 153);\n"
"border-color: rgb(145, 144, 146)")

        self.gridLayout.addWidget(self.cb_driveNames, 1, 1, 1, 1)

        self.w_moreInfo = QWidget(self.w_driveInfo)
        self.w_moreInfo.setObjectName(u"w_moreInfo")
        self.w_moreInfo.setStyleSheet(u"color: rgb(150, 150, 150);")
        self.horizontalLayout_2 = QHBoxLayout(self.w_moreInfo)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(6, 0, 0, 0)
        self.lbl_driveMoreInfoLeft = QLabel(self.w_moreInfo)
        self.lbl_driveMoreInfoLeft.setObjectName(u"lbl_driveMoreInfoLeft")

        self.horizontalLayout_2.addWidget(self.lbl_driveMoreInfoLeft)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.lbl_driveMoreInfoRight = QLabel(self.w_moreInfo)
        self.lbl_driveMoreInfoRight.setObjectName(u"lbl_driveMoreInfoRight")
        self.lbl_driveMoreInfoRight.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.lbl_driveMoreInfoRight.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.lbl_driveMoreInfoRight)


        self.gridLayout.addWidget(self.w_moreInfo, 3, 0, 1, 2)

        self.lbl_archiveNameValue = QLabel(self.w_driveInfo)
        self.lbl_archiveNameValue.setObjectName(u"lbl_archiveNameValue")
        self.lbl_archiveNameValue.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.lbl_archiveNameValue, 0, 1, 1, 1)


        self.verticalLayout_3.addWidget(self.w_driveInfo)

        self.sa_main.setWidget(self.sa_mainContents)

        self.verticalLayout_2.addWidget(self.sa_main)


        self.verticalLayout.addWidget(self.fr_main)

        QWidget.setTabOrder(self.cb_driveNames, self.pb_moreInfo)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lbl_archiveName.setText(QCoreApplication.translate("Form", u"Archive: ", None))
        self.lbl_numActiveFilters.setText(QCoreApplication.translate("Form", u"Anzahl aktiver Filter", None))
        self.pb_numActiveFilters.setText("")
        self.lbl_drives.setText(QCoreApplication.translate("Form", u"Antrieb:", None))
        self.pb_moreInfo.setText(QCoreApplication.translate("Form", u"mehr Info", None))
        self.lbl_driveMoreInfoLeft.setText("")
        self.lbl_driveMoreInfoRight.setText("")
        self.lbl_archiveNameValue.setText(QCoreApplication.translate("Form", u"TextLabel", None))
    # retranslateUi

