# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cw_filter.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
from . import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(412, 517)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.w_filter = QWidget(Form)
        self.w_filter.setObjectName(u"w_filter")
        self.w_filter.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayout = QVBoxLayout(self.w_filter)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_filterN = QLabel(self.w_filter)
        self.lbl_filterN.setObjectName(u"lbl_filterN")
        self.lbl_filterN.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout.addWidget(self.lbl_filterN)

        self.fr_filter = QFrame(self.w_filter)
        self.fr_filter.setObjectName(u"fr_filter")
        self.fr_filter.setStyleSheet(u"#fr_filter {\n"
"    border-top: 1px solid #999999;\n"
"    border-left: none;\n"
"    border-right: none;\n"
"    border-bottom: none;\n"
"}")
        self.fr_filter.setFrameShape(QFrame.Shape.StyledPanel)
        self.fr_filter.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.fr_filter)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.cb_showFilter = QCheckBox(self.fr_filter)
        self.cb_showFilter.setObjectName(u"cb_showFilter")
        self.cb_showFilter.setMaximumSize(QSize(50, 16777215))
        self.cb_showFilter.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.cb_showFilter.setChecked(True)

        self.gridLayout_2.addWidget(self.cb_showFilter, 5, 4, 1, 1)

        self.w_otherFilterTypes = QWidget(self.fr_filter)
        self.w_otherFilterTypes.setObjectName(u"w_otherFilterTypes")
        self.w_otherFilterTypes.setMinimumSize(QSize(0, 105))
        self.gridLayout_4 = QGridLayout(self.w_otherFilterTypes)
        self.gridLayout_4.setSpacing(5)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.lbl_notchDepth = QLabel(self.w_otherFilterTypes)
        self.lbl_notchDepth.setObjectName(u"lbl_notchDepth")
        self.lbl_notchDepth.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_4.addWidget(self.lbl_notchDepth, 2, 0, 1, 1)

        self.dsb_blockFreq = QDoubleSpinBox(self.w_otherFilterTypes)
        self.dsb_blockFreq.setObjectName(u"dsb_blockFreq")
        self.dsb_blockFreq.setMinimumSize(QSize(100, 0))
        self.dsb_blockFreq.setMaximumSize(QSize(100, 16777215))
        self.dsb_blockFreq.setDecimals(4)
        self.dsb_blockFreq.setMinimum(-100000.000000000000000)
        self.dsb_blockFreq.setMaximum(100000.000000000000000)
        self.dsb_blockFreq.setValue(2000.000000000000000)

        self.gridLayout_4.addWidget(self.dsb_blockFreq, 0, 3, 1, 1)

        self.dsb_notchDepth = QDoubleSpinBox(self.w_otherFilterTypes)
        self.dsb_notchDepth.setObjectName(u"dsb_notchDepth")
        self.dsb_notchDepth.setMinimumSize(QSize(100, 0))
        self.dsb_notchDepth.setMaximumSize(QSize(100, 16777215))
        self.dsb_notchDepth.setDecimals(4)
        self.dsb_notchDepth.setMinimum(-100000.000000000000000)
        self.dsb_notchDepth.setMaximum(100000.000000000000000)

        self.gridLayout_4.addWidget(self.dsb_notchDepth, 2, 3, 1, 1)

        self.lbl_blockFreq = QLabel(self.w_otherFilterTypes)
        self.lbl_blockFreq.setObjectName(u"lbl_blockFreq")
        self.lbl_blockFreq.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_4.addWidget(self.lbl_blockFreq, 0, 0, 1, 1)

        self.dsb_attenuation = QDoubleSpinBox(self.w_otherFilterTypes)
        self.dsb_attenuation.setObjectName(u"dsb_attenuation")
        self.dsb_attenuation.setMinimumSize(QSize(100, 0))
        self.dsb_attenuation.setMaximumSize(QSize(100, 16777215))
        self.dsb_attenuation.setDecimals(4)
        self.dsb_attenuation.setMinimum(-180.000000000000000)
        self.dsb_attenuation.setMaximum(180.000000000000000)

        self.gridLayout_4.addWidget(self.dsb_attenuation, 3, 3, 1, 1)

        self.lbl_attenuation = QLabel(self.w_otherFilterTypes)
        self.lbl_attenuation.setObjectName(u"lbl_attenuation")
        self.lbl_attenuation.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_4.addWidget(self.lbl_attenuation, 3, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 0, 1, 1, 1)

        self.lbl_bandFreq = QLabel(self.w_otherFilterTypes)
        self.lbl_bandFreq.setObjectName(u"lbl_bandFreq")

        self.gridLayout_4.addWidget(self.lbl_bandFreq, 1, 0, 1, 1)

        self.dsb_bandFreq = QDoubleSpinBox(self.w_otherFilterTypes)
        self.dsb_bandFreq.setObjectName(u"dsb_bandFreq")
        self.dsb_bandFreq.setMinimumSize(QSize(100, 0))
        self.dsb_bandFreq.setMaximumSize(QSize(100, 16777215))
        self.dsb_bandFreq.setDecimals(4)
        self.dsb_bandFreq.setMinimum(-100000.000000000000000)
        self.dsb_bandFreq.setMaximum(100000.000000000000000)
        self.dsb_bandFreq.setValue(10.000000000000000)

        self.gridLayout_4.addWidget(self.dsb_bandFreq, 1, 3, 1, 1)

        self.pb_blockFreq = QPushButton(self.w_otherFilterTypes)
        self.pb_blockFreq.setObjectName(u"pb_blockFreq")
        self.pb_blockFreq.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/resources/reset_24dp.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_blockFreq.setIcon(icon)
        self.pb_blockFreq.setIconSize(QSize(18, 18))

        self.gridLayout_4.addWidget(self.pb_blockFreq, 0, 2, 1, 1)

        self.pb_bandFreq = QPushButton(self.w_otherFilterTypes)
        self.pb_bandFreq.setObjectName(u"pb_bandFreq")
        self.pb_bandFreq.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"}")
        self.pb_bandFreq.setIcon(icon)
        self.pb_bandFreq.setIconSize(QSize(18, 18))

        self.gridLayout_4.addWidget(self.pb_bandFreq, 1, 2, 1, 1)

        self.pb_notchDepth = QPushButton(self.w_otherFilterTypes)
        self.pb_notchDepth.setObjectName(u"pb_notchDepth")
        self.pb_notchDepth.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"}")
        self.pb_notchDepth.setIcon(icon)
        self.pb_notchDepth.setIconSize(QSize(18, 18))

        self.gridLayout_4.addWidget(self.pb_notchDepth, 2, 2, 1, 1)

        self.pb_attenuation = QPushButton(self.w_otherFilterTypes)
        self.pb_attenuation.setObjectName(u"pb_attenuation")
        self.pb_attenuation.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"}")
        self.pb_attenuation.setIcon(icon)
        self.pb_attenuation.setIconSize(QSize(18, 18))

        self.gridLayout_4.addWidget(self.pb_attenuation, 3, 2, 1, 1)


        self.gridLayout_2.addWidget(self.w_otherFilterTypes, 3, 0, 1, 5)

        self.lbl_showFilter = QLabel(self.fr_filter)
        self.lbl_showFilter.setObjectName(u"lbl_showFilter")

        self.gridLayout_2.addWidget(self.lbl_showFilter, 5, 0, 1, 1)

        self.w_PT1Filter = QWidget(self.fr_filter)
        self.w_PT1Filter.setObjectName(u"w_PT1Filter")
        self.horizontalLayout = QHBoxLayout(self.w_PT1Filter)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lbl_timeConstant = QLabel(self.w_PT1Filter)
        self.lbl_timeConstant.setObjectName(u"lbl_timeConstant")

        self.horizontalLayout.addWidget(self.lbl_timeConstant)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_8)

        self.pb_timeConstant = QPushButton(self.w_PT1Filter)
        self.pb_timeConstant.setObjectName(u"pb_timeConstant")
        self.pb_timeConstant.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"}")
        self.pb_timeConstant.setIcon(icon)
        self.pb_timeConstant.setIconSize(QSize(18, 18))

        self.horizontalLayout.addWidget(self.pb_timeConstant)

        self.dsb_timeConstant = QDoubleSpinBox(self.w_PT1Filter)
        self.dsb_timeConstant.setObjectName(u"dsb_timeConstant")
        self.dsb_timeConstant.setMinimumSize(QSize(100, 0))
        self.dsb_timeConstant.setMaximumSize(QSize(100, 16777215))
        self.dsb_timeConstant.setDecimals(4)
        self.dsb_timeConstant.setMinimum(-100000.000000000000000)
        self.dsb_timeConstant.setMaximum(100000.000000000000000)
        self.dsb_timeConstant.setValue(0.000000000000000)

        self.horizontalLayout.addWidget(self.dsb_timeConstant)


        self.gridLayout_2.addWidget(self.w_PT1Filter, 1, 0, 1, 5)

        self.w_color = QWidget(self.fr_filter)
        self.w_color.setObjectName(u"w_color")
        self.horizontalLayout_2 = QHBoxLayout(self.w_color)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lbl_color = QLabel(self.w_color)
        self.lbl_color.setObjectName(u"lbl_color")
        self.lbl_color.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_2.addWidget(self.lbl_color)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.w_colorPlaceholder = QWidget(self.w_color)
        self.w_colorPlaceholder.setObjectName(u"w_colorPlaceholder")

        self.horizontalLayout_2.addWidget(self.w_colorPlaceholder)


        self.gridLayout_2.addWidget(self.w_color, 6, 0, 1, 5)

        self.w_PT2Filter = QWidget(self.fr_filter)
        self.w_PT2Filter.setObjectName(u"w_PT2Filter")
        self.gridLayout_7 = QGridLayout(self.w_PT2Filter)
        self.gridLayout_7.setSpacing(5)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.dsb_resFreq = QDoubleSpinBox(self.w_PT2Filter)
        self.dsb_resFreq.setObjectName(u"dsb_resFreq")
        self.dsb_resFreq.setMinimumSize(QSize(100, 0))
        self.dsb_resFreq.setMaximumSize(QSize(100, 16777215))
        self.dsb_resFreq.setDecimals(4)
        self.dsb_resFreq.setMinimum(-1000000.000000000000000)
        self.dsb_resFreq.setMaximum(1000000.000000000000000)
        self.dsb_resFreq.setValue(0.000000000000000)

        self.gridLayout_7.addWidget(self.dsb_resFreq, 0, 3, 1, 1)

        self.lbl_damping = QLabel(self.w_PT2Filter)
        self.lbl_damping.setObjectName(u"lbl_damping")

        self.gridLayout_7.addWidget(self.lbl_damping, 1, 0, 1, 1)

        self.dsb_damping = QDoubleSpinBox(self.w_PT2Filter)
        self.dsb_damping.setObjectName(u"dsb_damping")
        self.dsb_damping.setMaximumSize(QSize(100, 16777215))
        self.dsb_damping.setDecimals(4)
        self.dsb_damping.setMinimum(-100000.000000000000000)
        self.dsb_damping.setMaximum(100000.000000000000000)
        self.dsb_damping.setSingleStep(0.100000000000000)
        self.dsb_damping.setValue(0.707100000000000)

        self.gridLayout_7.addWidget(self.dsb_damping, 1, 3, 1, 1)

        self.lbl_resFreq = QLabel(self.w_PT2Filter)
        self.lbl_resFreq.setObjectName(u"lbl_resFreq")
        self.lbl_resFreq.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_7.addWidget(self.lbl_resFreq, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)

        self.pb_resFreq = QPushButton(self.w_PT2Filter)
        self.pb_resFreq.setObjectName(u"pb_resFreq")
        self.pb_resFreq.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"}")
        self.pb_resFreq.setIcon(icon)
        self.pb_resFreq.setIconSize(QSize(18, 18))

        self.gridLayout_7.addWidget(self.pb_resFreq, 0, 2, 1, 1)

        self.pb_damping = QPushButton(self.w_PT2Filter)
        self.pb_damping.setObjectName(u"pb_damping")
        self.pb_damping.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"}")
        self.pb_damping.setIcon(icon)
        self.pb_damping.setIconSize(QSize(18, 18))

        self.gridLayout_7.addWidget(self.pb_damping, 1, 2, 1, 1)


        self.gridLayout_2.addWidget(self.w_PT2Filter, 2, 0, 1, 5)

        self.cb_filterType = QComboBox(self.fr_filter)
        self.cb_filterType.setObjectName(u"cb_filterType")
        self.cb_filterType.setStyleSheet(u"selection-color: rgb(1, 153, 153);")

        self.gridLayout_2.addWidget(self.cb_filterType, 0, 4, 1, 1)

        self.lbl_type = QLabel(self.fr_filter)
        self.lbl_type.setObjectName(u"lbl_type")
        self.lbl_type.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_2.addWidget(self.lbl_type, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 7, 1, 1, 4)

        self.pb_showParam = QPushButton(self.fr_filter)
        self.pb_showParam.setObjectName(u"pb_showParam")
        self.pb_showParam.setStyleSheet(u"text-align: left;\n"
"padding-left: 0px; /* shifts text from the edge */\n"
"border: none\n"
"\n"
"")
        icon1 = QIcon()
        icon1.addFile(u":/resources/arrow_right_24dp.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_showParam.setIcon(icon1)

        self.gridLayout_2.addWidget(self.pb_showParam, 7, 0, 1, 1)

        self.w_param = QWidget(self.fr_filter)
        self.w_param.setObjectName(u"w_param")
        self.w_param.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.gridLayout_3 = QGridLayout(self.w_param)
        self.gridLayout_3.setSpacing(5)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(20, 0, 0, 0)
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_7, 0, 1, 1, 1)

        self.lbl_param4 = QLabel(self.w_param)
        self.lbl_param4.setObjectName(u"lbl_param4")

        self.gridLayout_3.addWidget(self.lbl_param4, 3, 0, 1, 1)

        self.lbl_param5 = QLabel(self.w_param)
        self.lbl_param5.setObjectName(u"lbl_param5")

        self.gridLayout_3.addWidget(self.lbl_param5, 4, 0, 1, 1)

        self.lbl_param1 = QLabel(self.w_param)
        self.lbl_param1.setObjectName(u"lbl_param1")

        self.gridLayout_3.addWidget(self.lbl_param1, 0, 0, 1, 1)

        self.lbl_param2 = QLabel(self.w_param)
        self.lbl_param2.setObjectName(u"lbl_param2")

        self.gridLayout_3.addWidget(self.lbl_param2, 1, 0, 1, 1)

        self.lbl_param3 = QLabel(self.w_param)
        self.lbl_param3.setObjectName(u"lbl_param3")

        self.gridLayout_3.addWidget(self.lbl_param3, 2, 0, 1, 1)

        self.lbl_param1Value = QLabel(self.w_param)
        self.lbl_param1Value.setObjectName(u"lbl_param1Value")
        self.lbl_param1Value.setStyleSheet(u"background-color: rgb(213, 215, 215);")

        self.gridLayout_3.addWidget(self.lbl_param1Value, 0, 2, 1, 1)

        self.lbl_param2Value = QLabel(self.w_param)
        self.lbl_param2Value.setObjectName(u"lbl_param2Value")
        self.lbl_param2Value.setStyleSheet(u"background-color: rgb(213, 215, 215);")

        self.gridLayout_3.addWidget(self.lbl_param2Value, 1, 2, 1, 1)

        self.lbl_param3Value = QLabel(self.w_param)
        self.lbl_param3Value.setObjectName(u"lbl_param3Value")
        self.lbl_param3Value.setStyleSheet(u"background-color: rgb(213, 215, 215);")

        self.gridLayout_3.addWidget(self.lbl_param3Value, 2, 2, 1, 1)

        self.lbl_param4Value = QLabel(self.w_param)
        self.lbl_param4Value.setObjectName(u"lbl_param4Value")
        self.lbl_param4Value.setStyleSheet(u"background-color: rgb(213, 215, 215);")

        self.gridLayout_3.addWidget(self.lbl_param4Value, 3, 2, 1, 1)

        self.lbl_param5Value = QLabel(self.w_param)
        self.lbl_param5Value.setObjectName(u"lbl_param5Value")
        self.lbl_param5Value.setStyleSheet(u"background-color: rgb(213, 215, 215);")

        self.gridLayout_3.addWidget(self.lbl_param5Value, 4, 2, 1, 1)


        self.gridLayout_2.addWidget(self.w_param, 8, 0, 2, 5)

        self.pb_type = QPushButton(self.fr_filter)
        self.pb_type.setObjectName(u"pb_type")
        self.pb_type.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"}")
        self.pb_type.setIcon(icon)
        self.pb_type.setIconSize(QSize(18, 18))

        self.gridLayout_2.addWidget(self.pb_type, 0, 3, 1, 1)


        self.verticalLayout.addWidget(self.fr_filter)


        self.gridLayout.addWidget(self.w_filter, 0, 1, 1, 1)

        QWidget.setTabOrder(self.cb_filterType, self.dsb_damping)
        QWidget.setTabOrder(self.dsb_damping, self.dsb_bandFreq)
        QWidget.setTabOrder(self.dsb_bandFreq, self.dsb_notchDepth)
        QWidget.setTabOrder(self.dsb_notchDepth, self.dsb_attenuation)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lbl_filterN.setText(QCoreApplication.translate("Form", u"Filter n", None))
        self.cb_showFilter.setText("")
        self.lbl_notchDepth.setText(QCoreApplication.translate("Form", u"Kerbtiefe [dB]", None))
        self.lbl_blockFreq.setText(QCoreApplication.translate("Form", u"Sperrfrequenz [Hz]", None))
        self.lbl_attenuation.setText(QCoreApplication.translate("Form", u"Absenkung", None))
        self.lbl_bandFreq.setText(QCoreApplication.translate("Form", u"Bandbreite [Hz]", None))
        self.pb_blockFreq.setText("")
        self.pb_bandFreq.setText("")
        self.pb_notchDepth.setText("")
        self.pb_attenuation.setText("")
        self.lbl_showFilter.setText(QCoreApplication.translate("Form", u"Anzeigen", None))
        self.lbl_timeConstant.setText(QCoreApplication.translate("Form", u"Zeitkonstante [ms]", None))
        self.pb_timeConstant.setText("")
        self.lbl_color.setText(QCoreApplication.translate("Form", u"Farbe", None))
        self.lbl_damping.setText(QCoreApplication.translate("Form", u"D\u00e4mpfung [dB]", None))
        self.lbl_resFreq.setText(QCoreApplication.translate("Form", u"Eigenfrequenz [Hz]", None))
        self.pb_resFreq.setText("")
        self.pb_damping.setText("")
        self.lbl_type.setText(QCoreApplication.translate("Form", u"Typ", None))
        self.pb_showParam.setText(QCoreApplication.translate("Form", u"Parameter", None))
        self.lbl_param4.setText(QCoreApplication.translate("Form", u"param4", None))
        self.lbl_param5.setText(QCoreApplication.translate("Form", u"param5", None))
        self.lbl_param1.setText(QCoreApplication.translate("Form", u"param1", None))
        self.lbl_param2.setText(QCoreApplication.translate("Form", u"param2", None))
        self.lbl_param3.setText(QCoreApplication.translate("Form", u"param3", None))
        self.lbl_param1Value.setText(QCoreApplication.translate("Form", u"placeholder", None))
        self.lbl_param2Value.setText(QCoreApplication.translate("Form", u"placeholder", None))
        self.lbl_param3Value.setText(QCoreApplication.translate("Form", u"placeholder", None))
        self.lbl_param4Value.setText(QCoreApplication.translate("Form", u"placeholder", None))
        self.lbl_param5Value.setText(QCoreApplication.translate("Form", u"placeholder", None))
        self.pb_type.setText("")
    # retranslateUi

