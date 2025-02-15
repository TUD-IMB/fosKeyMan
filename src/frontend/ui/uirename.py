# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rename.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Rename(object):
    def setupUi(self, Rename):
        if not Rename.objectName():
            Rename.setObjectName(u"Rename")
        Rename.resize(344, 109)
        self.verticalLayout_4 = QVBoxLayout(Rename)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.serialNumberLabel = QLabel(Rename)
        self.serialNumberLabel.setObjectName(u"serialNumberLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.serialNumberLabel)

        self.sensorNameLabel = QLabel(Rename)
        self.sensorNameLabel.setObjectName(u"sensorNameLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.sensorNameLabel)

        self.sensorNameLineEdit = QLineEdit(Rename)
        self.sensorNameLineEdit.setObjectName(u"sensorNameLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.sensorNameLineEdit)

        self.serialNumberLabel2 = QLabel(Rename)
        self.serialNumberLabel2.setObjectName(u"serialNumberLabel2")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.serialNumberLabel2)


        self.verticalLayout_4.addLayout(self.formLayout)

        self.horizontalButtonlLayout = QHBoxLayout()
        self.horizontalButtonlLayout.setObjectName(u"horizontalButtonlLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalButtonlLayout.addItem(self.horizontalSpacer)

        self.renameButton = QPushButton(Rename)
        self.renameButton.setObjectName(u"renameButton")

        self.horizontalButtonlLayout.addWidget(self.renameButton)

        self.cancelButton = QPushButton(Rename)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalButtonlLayout.addWidget(self.cancelButton)


        self.verticalLayout_4.addLayout(self.horizontalButtonlLayout)


        self.retranslateUi(Rename)

        QMetaObject.connectSlotsByName(Rename)
    # setupUi

    def retranslateUi(self, Rename):
        Rename.setWindowTitle(QCoreApplication.translate("Rename", u"Rename Sensor", None))
#if QT_CONFIG(tooltip)
        Rename.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.serialNumberLabel.setToolTip(QCoreApplication.translate("Rename", u"Serial Number", None))
#endif // QT_CONFIG(tooltip)
        self.serialNumberLabel.setText(QCoreApplication.translate("Rename", u"Serial Number:", None))
#if QT_CONFIG(tooltip)
        self.sensorNameLabel.setToolTip(QCoreApplication.translate("Rename", u"Sensor Name", None))
#endif // QT_CONFIG(tooltip)
        self.sensorNameLabel.setText(QCoreApplication.translate("Rename", u"Sensor Name:", None))
#if QT_CONFIG(tooltip)
        self.sensorNameLineEdit.setToolTip(QCoreApplication.translate("Rename", u"Enter sensor name metadata", None))
#endif // QT_CONFIG(tooltip)
        self.serialNumberLabel2.setText("")
#if QT_CONFIG(tooltip)
        self.renameButton.setToolTip(QCoreApplication.translate("Rename", u"Import and Next", None))
#endif // QT_CONFIG(tooltip)
        self.renameButton.setText(QCoreApplication.translate("Rename", u"Rename", None))
#if QT_CONFIG(tooltip)
        self.cancelButton.setToolTip(QCoreApplication.translate("Rename", u"Cancel and Close", None))
#endif // QT_CONFIG(tooltip)
        self.cancelButton.setText(QCoreApplication.translate("Rename", u"Cancel", None))
    # retranslateUi

