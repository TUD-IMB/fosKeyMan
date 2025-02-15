# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'replace.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QTextBrowser, QTreeView, QVBoxLayout, QWidget)

class Ui_Replace(object):
    def setupUi(self, Replace):
        if not Replace.objectName():
            Replace.setObjectName(u"Replace")
        Replace.resize(575, 526)
        self.verticalLayout = QVBoxLayout(Replace)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Replace)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.dbRadioButton = QRadioButton(Replace)
        self.dbRadioButton.setObjectName(u"dbRadioButton")

        self.horizontalLayout.addWidget(self.dbRadioButton)

        self.diskRadioButton = QRadioButton(Replace)
        self.diskRadioButton.setObjectName(u"diskRadioButton")

        self.horizontalLayout.addWidget(self.diskRadioButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.dbTreeView = QTreeView(Replace)
        self.dbTreeView.setObjectName(u"dbTreeView")

        self.horizontalLayout_2.addWidget(self.dbTreeView)

        self.diskTreeView = QTreeView(Replace)
        self.diskTreeView.setObjectName(u"diskTreeView")

        self.horizontalLayout_2.addWidget(self.diskTreeView)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.textBrowser = QTextBrowser(Replace)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.horizontalButtonlLayout = QHBoxLayout()
        self.horizontalButtonlLayout.setObjectName(u"horizontalButtonlLayout")
        self.horizontalButtonlLayout.setContentsMargins(-1, 0, 0, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalButtonlLayout.addItem(self.horizontalSpacer)

        self.saveButton = QPushButton(Replace)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalButtonlLayout.addWidget(self.saveButton)


        self.verticalLayout.addLayout(self.horizontalButtonlLayout)


        self.retranslateUi(Replace)

        QMetaObject.connectSlotsByName(Replace)
    # setupUi

    def retranslateUi(self, Replace):
        Replace.setWindowTitle(QCoreApplication.translate("Replace", u"Mismatch detected in keyfiles.", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Replace", u"Choose the version of the keyfile to retain", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Replace", u"Please select the keyfile version you want to keep:", None))
#if QT_CONFIG(tooltip)
        self.dbRadioButton.setToolTip(QCoreApplication.translate("Replace", u"Keep the keyfile stored in the database", None))
#endif // QT_CONFIG(tooltip)
        self.dbRadioButton.setText(QCoreApplication.translate("Replace", u"Version in Database", None))
#if QT_CONFIG(tooltip)
        self.diskRadioButton.setToolTip(QCoreApplication.translate("Replace", u"Keep the keyfile stored on disk", None))
#endif // QT_CONFIG(tooltip)
        self.diskRadioButton.setText(QCoreApplication.translate("Replace", u"Version in Disk", None))
#if QT_CONFIG(tooltip)
        self.dbTreeView.setToolTip(QCoreApplication.translate("Replace", u"Keyfile content from the database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.diskTreeView.setToolTip(QCoreApplication.translate("Replace", u"Keyfile content from the disk", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.textBrowser.setToolTip(QCoreApplication.translate("Replace", u"Details of the selected file", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.saveButton.setToolTip(QCoreApplication.translate("Replace", u"Save the selected keyfile version", None))
#endif // QT_CONFIG(tooltip)
        self.saveButton.setText(QCoreApplication.translate("Replace", u"Proceed", None))
    # retranslateUi

