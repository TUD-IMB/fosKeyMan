# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'merge.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Merge(object):
    def setupUi(self, Merge):
        if not Merge.objectName():
            Merge.setObjectName(u"Merge")
        Merge.resize(769, 420)
        self.verticalLayout_4 = QVBoxLayout(Merge)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.currentSpecimenLineEdit = QLineEdit(Merge)
        self.currentSpecimenLineEdit.setObjectName(u"currentSpecimenLineEdit")

        self.gridLayout.addWidget(self.currentSpecimenLineEdit, 5, 2, 1, 1)

        self.mergedOperatorLineEdit = QLineEdit(Merge)
        self.mergedOperatorLineEdit.setObjectName(u"mergedOperatorLineEdit")

        self.gridLayout.addWidget(self.mergedOperatorLineEdit, 4, 4, 1, 1)

        self.currentProjectLineEdit = QLineEdit(Merge)
        self.currentProjectLineEdit.setObjectName(u"currentProjectLineEdit")

        self.gridLayout.addWidget(self.currentProjectLineEdit, 3, 2, 1, 1)

        self.label_6 = QLabel(Merge)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 4, 1, 1)

        self.currentSerialLineEdit = QLineEdit(Merge)
        self.currentSerialLineEdit.setObjectName(u"currentSerialLineEdit")

        self.gridLayout.addWidget(self.currentSerialLineEdit, 1, 2, 1, 1)

        self.label_3 = QLabel(Merge)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.importedOperatorLineEdit = QLineEdit(Merge)
        self.importedOperatorLineEdit.setObjectName(u"importedOperatorLineEdit")

        self.gridLayout.addWidget(self.importedOperatorLineEdit, 4, 3, 1, 1)

        self.mergedSpecimenLineEdit = QLineEdit(Merge)
        self.mergedSpecimenLineEdit.setObjectName(u"mergedSpecimenLineEdit")

        self.gridLayout.addWidget(self.mergedSpecimenLineEdit, 5, 4, 1, 1)

        self.label_10 = QLabel(Merge)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 6, 0, 1, 1)

        self.label_8 = QLabel(Merge)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)

        self.importedInstallLineEdit = QLineEdit(Merge)
        self.importedInstallLineEdit.setObjectName(u"importedInstallLineEdit")

        self.gridLayout.addWidget(self.importedInstallLineEdit, 7, 3, 1, 1)

        self.currentOperatorLineEdit = QLineEdit(Merge)
        self.currentOperatorLineEdit.setObjectName(u"currentOperatorLineEdit")

        self.gridLayout.addWidget(self.currentOperatorLineEdit, 4, 2, 1, 1)

        self.mergedNameLineEdit = QLineEdit(Merge)
        self.mergedNameLineEdit.setObjectName(u"mergedNameLineEdit")

        self.gridLayout.addWidget(self.mergedNameLineEdit, 2, 4, 1, 1)

        self.mergedTypeLineEdit = QLineEdit(Merge)
        self.mergedTypeLineEdit.setObjectName(u"mergedTypeLineEdit")

        self.gridLayout.addWidget(self.mergedTypeLineEdit, 6, 4, 1, 1)

        self.importedKeyfileStatusLabel = QLabel(Merge)
        self.importedKeyfileStatusLabel.setObjectName(u"importedKeyfileStatusLabel")

        self.gridLayout.addWidget(self.importedKeyfileStatusLabel, 14, 3, 1, 1)

        self.currentInstallLineEdit = QLineEdit(Merge)
        self.currentInstallLineEdit.setObjectName(u"currentInstallLineEdit")

        self.gridLayout.addWidget(self.currentInstallLineEdit, 7, 2, 1, 1)

        self.currentNameLineEdit = QLineEdit(Merge)
        self.currentNameLineEdit.setObjectName(u"currentNameLineEdit")

        self.gridLayout.addWidget(self.currentNameLineEdit, 2, 2, 1, 1)

        self.importedSpecimenLineEdit = QLineEdit(Merge)
        self.importedSpecimenLineEdit.setObjectName(u"importedSpecimenLineEdit")

        self.gridLayout.addWidget(self.importedSpecimenLineEdit, 5, 3, 1, 1)

        self.label_5 = QLabel(Merge)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 3, 1, 1)

        self.importedSerialLineEdit = QLineEdit(Merge)
        self.importedSerialLineEdit.setObjectName(u"importedSerialLineEdit")

        self.gridLayout.addWidget(self.importedSerialLineEdit, 1, 3, 1, 1)

        self.mergedProjectLineEdit = QLineEdit(Merge)
        self.mergedProjectLineEdit.setObjectName(u"mergedProjectLineEdit")

        self.gridLayout.addWidget(self.mergedProjectLineEdit, 3, 4, 1, 1)

        self.currentNotelineEdit = QLineEdit(Merge)
        self.currentNotelineEdit.setObjectName(u"currentNotelineEdit")

        self.gridLayout.addWidget(self.currentNotelineEdit, 8, 2, 1, 1)

        self.currentTypeLineEdit = QLineEdit(Merge)
        self.currentTypeLineEdit.setObjectName(u"currentTypeLineEdit")

        self.gridLayout.addWidget(self.currentTypeLineEdit, 6, 2, 1, 1)

        self.mergedInstallLineEdit = QLineEdit(Merge)
        self.mergedInstallLineEdit.setObjectName(u"mergedInstallLineEdit")

        self.gridLayout.addWidget(self.mergedInstallLineEdit, 7, 4, 1, 1)

        self.mergedSerialLineEdit = QLineEdit(Merge)
        self.mergedSerialLineEdit.setObjectName(u"mergedSerialLineEdit")

        self.gridLayout.addWidget(self.mergedSerialLineEdit, 1, 4, 1, 1)

        self.importedNoteLineEdit = QLineEdit(Merge)
        self.importedNoteLineEdit.setObjectName(u"importedNoteLineEdit")

        self.gridLayout.addWidget(self.importedNoteLineEdit, 8, 3, 1, 1)

        self.importedProjectLineEdit = QLineEdit(Merge)
        self.importedProjectLineEdit.setObjectName(u"importedProjectLineEdit")

        self.gridLayout.addWidget(self.importedProjectLineEdit, 3, 3, 1, 1)

        self.label_11 = QLabel(Merge)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 7, 0, 1, 1)

        self.mergedNoteLineEdit = QLineEdit(Merge)
        self.mergedNoteLineEdit.setObjectName(u"mergedNoteLineEdit")

        self.gridLayout.addWidget(self.mergedNoteLineEdit, 8, 4, 1, 1)

        self.label = QLabel(Merge)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.label_7 = QLabel(Merge)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1)

        self.label_2 = QLabel(Merge)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.importedTypeLineEdit = QLineEdit(Merge)
        self.importedTypeLineEdit.setObjectName(u"importedTypeLineEdit")

        self.gridLayout.addWidget(self.importedTypeLineEdit, 6, 3, 1, 1)

        self.label_9 = QLabel(Merge)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 5, 0, 1, 1)

        self.label_4 = QLabel(Merge)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)

        self.importedNameLineEdit = QLineEdit(Merge)
        self.importedNameLineEdit.setObjectName(u"importedNameLineEdit")

        self.gridLayout.addWidget(self.importedNameLineEdit, 2, 3, 1, 1)

        self.currentRadioButton = QRadioButton(Merge)
        self.currentRadioButton.setObjectName(u"currentRadioButton")

        self.gridLayout.addWidget(self.currentRadioButton, 13, 2, 1, 1)

        self.label_12 = QLabel(Merge)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 13, 0, 1, 1)

        self.importedRadioButton = QRadioButton(Merge)
        self.importedRadioButton.setObjectName(u"importedRadioButton")

        self.gridLayout.addWidget(self.importedRadioButton, 13, 3, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.currentButton = QPushButton(Merge)
        self.currentButton.setObjectName(u"currentButton")

        self.horizontalLayout_2.addWidget(self.currentButton)

        self.importButton = QPushButton(Merge)
        self.importButton.setObjectName(u"importButton")

        self.horizontalLayout_2.addWidget(self.importButton)

        self.compareKeyfileButton = QPushButton(Merge)
        self.compareKeyfileButton.setObjectName(u"compareKeyfileButton")

        self.horizontalLayout_2.addWidget(self.compareKeyfileButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.proceedButton = QPushButton(Merge)
        self.proceedButton.setObjectName(u"proceedButton")

        self.horizontalLayout_2.addWidget(self.proceedButton)

        self.skipButton = QPushButton(Merge)
        self.skipButton.setObjectName(u"skipButton")

        self.horizontalLayout_2.addWidget(self.skipButton)

        self.finishButton = QPushButton(Merge)
        self.finishButton.setObjectName(u"finishButton")

        self.horizontalLayout_2.addWidget(self.finishButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Merge)

        QMetaObject.connectSlotsByName(Merge)
    # setupUi

    def retranslateUi(self, Merge):
        Merge.setWindowTitle(QCoreApplication.translate("Merge", u"Merge Conflict", None))
#if QT_CONFIG(tooltip)
        Merge.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.currentSpecimenLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Specimen details in current database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.mergedOperatorLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Enter operator name after merge", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.currentProjectLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Project name in current database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_6.setToolTip(QCoreApplication.translate("Merge", u"Metadata after merge", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("Merge", u"Merged entry", None))
#if QT_CONFIG(tooltip)
        self.currentSerialLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Serial number in current database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("Merge", u"Project", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Merge", u"Project", None))
#if QT_CONFIG(tooltip)
        self.importedOperatorLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Operator name in imported database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.mergedSpecimenLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Enter specimen details after merge", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_10.setToolTip(QCoreApplication.translate("Merge", u"DFOS Type", None))
#endif // QT_CONFIG(tooltip)
        self.label_10.setText(QCoreApplication.translate("Merge", u"DFOS_Type", None))
#if QT_CONFIG(tooltip)
        self.label_8.setToolTip(QCoreApplication.translate("Merge", u"Note", None))
#endif // QT_CONFIG(tooltip)
        self.label_8.setText(QCoreApplication.translate("Merge", u"Note", None))
#if QT_CONFIG(tooltip)
        self.importedInstallLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Installation details in imported database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.currentOperatorLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Operator name in current database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.mergedNameLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Enter sensor name after merge", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.mergedTypeLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Enter DFOS type after merge", None))
#endif // QT_CONFIG(tooltip)
        self.importedKeyfileStatusLabel.setText("")
#if QT_CONFIG(tooltip)
        self.currentInstallLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Installation details in current database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.currentNameLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Sensor name in current database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.importedSpecimenLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Specimen details in imported database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("Merge", u"Metadata in imported database", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("Merge", u"Imported entry", None))
#if QT_CONFIG(tooltip)
        self.importedSerialLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Serial number in imported database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.mergedProjectLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Enter project name after merge", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.currentNotelineEdit.setToolTip(QCoreApplication.translate("Merge", u"Note in current database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.currentTypeLineEdit.setToolTip(QCoreApplication.translate("Merge", u"DFOS type in current database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.mergedInstallLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Enter installation details after merge", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.mergedSerialLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Enter serial number after merge", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.importedNoteLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Note in imported database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.importedProjectLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Project name in imported database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_11.setToolTip(QCoreApplication.translate("Merge", u"Installation", None))
#endif // QT_CONFIG(tooltip)
        self.label_11.setText(QCoreApplication.translate("Merge", u"Installation", None))
#if QT_CONFIG(tooltip)
        self.mergedNoteLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Enter note after merge", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Merge", u"Sensor Name", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Merge", u"Sensor Name", None))
#if QT_CONFIG(tooltip)
        self.label_7.setToolTip(QCoreApplication.translate("Merge", u"Operator", None))
#endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("Merge", u"Operator", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Merge", u"Serial Number", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Merge", u"Serial Number", None))
#if QT_CONFIG(tooltip)
        self.importedTypeLineEdit.setToolTip(QCoreApplication.translate("Merge", u"DFOS type in imported database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_9.setToolTip(QCoreApplication.translate("Merge", u"Specimen", None))
#endif // QT_CONFIG(tooltip)
        self.label_9.setText(QCoreApplication.translate("Merge", u"Specimen", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("Merge", u"Metadata in current database", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("Merge", u"Current entry", None))
#if QT_CONFIG(tooltip)
        self.importedNameLineEdit.setToolTip(QCoreApplication.translate("Merge", u"Sensor name in imported database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.currentRadioButton.setToolTip(QCoreApplication.translate("Merge", u"Keyfile in current database", None))
#endif // QT_CONFIG(tooltip)
        self.currentRadioButton.setText(QCoreApplication.translate("Merge", u"Current Keyfile Version", None))
#if QT_CONFIG(tooltip)
        self.label_12.setToolTip(QCoreApplication.translate("Merge", u"Keyfile", None))
#endif // QT_CONFIG(tooltip)
        self.label_12.setText(QCoreApplication.translate("Merge", u"Keyfile", None))
#if QT_CONFIG(tooltip)
        self.importedRadioButton.setToolTip(QCoreApplication.translate("Merge", u"Keyfile in  imported database", None))
#endif // QT_CONFIG(tooltip)
        self.importedRadioButton.setText(QCoreApplication.translate("Merge", u"Imported Keyfile Version", None))
#if QT_CONFIG(tooltip)
        self.currentButton.setToolTip(QCoreApplication.translate("Merge", u"Keep current entry for merged version", None))
#endif // QT_CONFIG(tooltip)
        self.currentButton.setText(QCoreApplication.translate("Merge", u"Keep current version", None))
#if QT_CONFIG(tooltip)
        self.importButton.setToolTip(QCoreApplication.translate("Merge", u"Keep imported entry for merged version", None))
#endif // QT_CONFIG(tooltip)
        self.importButton.setText(QCoreApplication.translate("Merge", u"Keep import version", None))
#if QT_CONFIG(tooltip)
        self.compareKeyfileButton.setToolTip(QCoreApplication.translate("Merge", u"Compare keyfiles between current and imported database", None))
#endif // QT_CONFIG(tooltip)
        self.compareKeyfileButton.setText(QCoreApplication.translate("Merge", u"Compare Keyfile", None))
#if QT_CONFIG(tooltip)
        self.proceedButton.setToolTip(QCoreApplication.translate("Merge", u"Save and Next", None))
#endif // QT_CONFIG(tooltip)
        self.proceedButton.setText(QCoreApplication.translate("Merge", u"Proceed", None))
#if QT_CONFIG(tooltip)
        self.skipButton.setToolTip(QCoreApplication.translate("Merge", u"Skip entry", None))
#endif // QT_CONFIG(tooltip)
        self.skipButton.setText(QCoreApplication.translate("Merge", u"Skip", None))
#if QT_CONFIG(tooltip)
        self.finishButton.setToolTip(QCoreApplication.translate("Merge", u"Finish merge", None))
#endif // QT_CONFIG(tooltip)
        self.finishButton.setText(QCoreApplication.translate("Merge", u"Finish", None))
    # retranslateUi

