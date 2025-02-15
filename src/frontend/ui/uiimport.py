# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import.ui'
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
from PySide6.QtWidgets import (QApplication, QDockWidget, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTextBrowser, QVBoxLayout, QWidget)

class Ui_Import(object):
    def setupUi(self, Import):
        if not Import.objectName():
            Import.setObjectName(u"Import")
        Import.resize(529, 442)
        self.verticalLayout_4 = QVBoxLayout(Import)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.serialNumberLabel = QLabel(Import)
        self.serialNumberLabel.setObjectName(u"serialNumberLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.serialNumberLabel)

        self.serialNumberLineEdit = QLineEdit(Import)
        self.serialNumberLineEdit.setObjectName(u"serialNumberLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.serialNumberLineEdit)

        self.sensorNameLabel = QLabel(Import)
        self.sensorNameLabel.setObjectName(u"sensorNameLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.sensorNameLabel)

        self.sensorNameLineEdit = QLineEdit(Import)
        self.sensorNameLineEdit.setObjectName(u"sensorNameLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.sensorNameLineEdit)

        self.projectLabel = QLabel(Import)
        self.projectLabel.setObjectName(u"projectLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.projectLabel)

        self.projectLineEdit = QLineEdit(Import)
        self.projectLineEdit.setObjectName(u"projectLineEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.projectLineEdit)

        self.operatorLabel = QLabel(Import)
        self.operatorLabel.setObjectName(u"operatorLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.operatorLabel)

        self.operatorLineEdit = QLineEdit(Import)
        self.operatorLineEdit.setObjectName(u"operatorLineEdit")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.operatorLineEdit)

        self.specimenLabel = QLabel(Import)
        self.specimenLabel.setObjectName(u"specimenLabel")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.specimenLabel)

        self.specimenLineEdit = QLineEdit(Import)
        self.specimenLineEdit.setObjectName(u"specimenLineEdit")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.specimenLineEdit)

        self.dFOSTypeLabel = QLabel(Import)
        self.dFOSTypeLabel.setObjectName(u"dFOSTypeLabel")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.dFOSTypeLabel)

        self.dFOSTypeLineEdit = QLineEdit(Import)
        self.dFOSTypeLineEdit.setObjectName(u"dFOSTypeLineEdit")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.dFOSTypeLineEdit)

        self.installationLabel = QLabel(Import)
        self.installationLabel.setObjectName(u"installationLabel")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.installationLabel)

        self.installationLineEdit = QLineEdit(Import)
        self.installationLineEdit.setObjectName(u"installationLineEdit")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.installationLineEdit)

        self.noteLabel = QLabel(Import)
        self.noteLabel.setObjectName(u"noteLabel")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.noteLabel)

        self.noteLineEdit = QLineEdit(Import)
        self.noteLineEdit.setObjectName(u"noteLineEdit")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.noteLineEdit)

        self.keyfileLabel = QLabel(Import)
        self.keyfileLabel.setObjectName(u"keyfileLabel")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.keyfileLabel)

        self.keyfileStatus = QLabel(Import)
        self.keyfileStatus.setObjectName(u"keyfileStatus")

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.keyfileStatus)


        self.verticalLayout_4.addLayout(self.formLayout)

        self.dockWidget = QDockWidget(Import)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.infoTextBrowser = QTextBrowser(self.dockWidgetContents)
        self.infoTextBrowser.setObjectName(u"infoTextBrowser")

        self.verticalLayout.addWidget(self.infoTextBrowser)

        self.dockWidget.setWidget(self.dockWidgetContents)

        self.verticalLayout_4.addWidget(self.dockWidget)

        self.horizontalButtonlLayout = QHBoxLayout()
        self.horizontalButtonlLayout.setObjectName(u"horizontalButtonlLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalButtonlLayout.addItem(self.horizontalSpacer)

        self.importButton = QPushButton(Import)
        self.importButton.setObjectName(u"importButton")

        self.horizontalButtonlLayout.addWidget(self.importButton)


        self.verticalLayout_4.addLayout(self.horizontalButtonlLayout)


        self.retranslateUi(Import)

        QMetaObject.connectSlotsByName(Import)
    # setupUi

    def retranslateUi(self, Import):
        Import.setWindowTitle(QCoreApplication.translate("Import", u"Import Keyfile to Database", None))
#if QT_CONFIG(tooltip)
        Import.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.serialNumberLabel.setToolTip(QCoreApplication.translate("Import", u"Serial Number", None))
#endif // QT_CONFIG(tooltip)
        self.serialNumberLabel.setText(QCoreApplication.translate("Import", u"Serial Number", None))
#if QT_CONFIG(tooltip)
        self.serialNumberLineEdit.setToolTip(QCoreApplication.translate("Import", u"Enter serial number metadata", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.sensorNameLabel.setToolTip(QCoreApplication.translate("Import", u"Sensor Name", None))
#endif // QT_CONFIG(tooltip)
        self.sensorNameLabel.setText(QCoreApplication.translate("Import", u"Sensor Name", None))
#if QT_CONFIG(tooltip)
        self.sensorNameLineEdit.setToolTip(QCoreApplication.translate("Import", u"Enter sensor name metadata", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.projectLabel.setToolTip(QCoreApplication.translate("Import", u"Project", None))
#endif // QT_CONFIG(tooltip)
        self.projectLabel.setText(QCoreApplication.translate("Import", u"Project", None))
#if QT_CONFIG(tooltip)
        self.projectLineEdit.setToolTip(QCoreApplication.translate("Import", u"Enter project metadata", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.operatorLabel.setToolTip(QCoreApplication.translate("Import", u"Operator", None))
#endif // QT_CONFIG(tooltip)
        self.operatorLabel.setText(QCoreApplication.translate("Import", u"Operator", None))
#if QT_CONFIG(tooltip)
        self.operatorLineEdit.setToolTip(QCoreApplication.translate("Import", u"Enter operator metadata", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.specimenLabel.setToolTip(QCoreApplication.translate("Import", u"Specimen", None))
#endif // QT_CONFIG(tooltip)
        self.specimenLabel.setText(QCoreApplication.translate("Import", u"Specimen", None))
#if QT_CONFIG(tooltip)
        self.specimenLineEdit.setToolTip(QCoreApplication.translate("Import", u"Enter specimen metadata", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.dFOSTypeLabel.setToolTip(QCoreApplication.translate("Import", u"DFOS Type", None))
#endif // QT_CONFIG(tooltip)
        self.dFOSTypeLabel.setText(QCoreApplication.translate("Import", u"DFOS Type", None))
#if QT_CONFIG(tooltip)
        self.dFOSTypeLineEdit.setToolTip(QCoreApplication.translate("Import", u"Enter DFOS type metadata", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.installationLabel.setToolTip(QCoreApplication.translate("Import", u"Installation", None))
#endif // QT_CONFIG(tooltip)
        self.installationLabel.setText(QCoreApplication.translate("Import", u"Installation", None))
#if QT_CONFIG(tooltip)
        self.installationLineEdit.setToolTip(QCoreApplication.translate("Import", u"Enter installation metadata", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.noteLabel.setToolTip(QCoreApplication.translate("Import", u"Note", None))
#endif // QT_CONFIG(tooltip)
        self.noteLabel.setText(QCoreApplication.translate("Import", u"Note", None))
#if QT_CONFIG(tooltip)
        self.noteLineEdit.setToolTip(QCoreApplication.translate("Import", u"Enter note metadata", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.keyfileLabel.setToolTip(QCoreApplication.translate("Import", u"Keyfile", None))
#endif // QT_CONFIG(tooltip)
        self.keyfileLabel.setText(QCoreApplication.translate("Import", u"Keyfile", None))
#if QT_CONFIG(tooltip)
        self.keyfileStatus.setToolTip(QCoreApplication.translate("Import", u"Attached Keyfile", None))
#endif // QT_CONFIG(tooltip)
        self.keyfileStatus.setText("")
#if QT_CONFIG(tooltip)
        self.dockWidget.setToolTip(QCoreApplication.translate("Import", u"Keyfile Information", None))
#endif // QT_CONFIG(tooltip)
        self.dockWidget.setWindowTitle(QCoreApplication.translate("Import", u"Keyfile Information", None))
#if QT_CONFIG(tooltip)
        self.infoTextBrowser.setToolTip(QCoreApplication.translate("Import", u"More information about the keyfile", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.importButton.setToolTip(QCoreApplication.translate("Import", u"Import and Next", None))
#endif // QT_CONFIG(tooltip)
        self.importButton.setText(QCoreApplication.translate("Import", u"Proceed", None))
    # retranslateUi

