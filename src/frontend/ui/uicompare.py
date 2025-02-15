# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'compare.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QTextBrowser,
    QTreeView, QVBoxLayout, QWidget)

class Ui_Compare(object):
    def setupUi(self, Compare):
        if not Compare.objectName():
            Compare.setObjectName(u"Compare")
        Compare.resize(575, 526)
        self.verticalLayout = QVBoxLayout(Compare)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.currentLabel = QLabel(Compare)
        self.currentLabel.setObjectName(u"currentLabel")

        self.horizontalLayout.addWidget(self.currentLabel)

        self.importedLabel = QLabel(Compare)
        self.importedLabel.setObjectName(u"importedLabel")

        self.horizontalLayout.addWidget(self.importedLabel)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.currentTreeView = QTreeView(Compare)
        self.currentTreeView.setObjectName(u"currentTreeView")

        self.horizontalLayout_2.addWidget(self.currentTreeView)

        self.importedTreeView = QTreeView(Compare)
        self.importedTreeView.setObjectName(u"importedTreeView")

        self.horizontalLayout_2.addWidget(self.importedTreeView)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.textBrowser = QTextBrowser(Compare)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, 0, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.closeButton = QPushButton(Compare)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout_3.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Compare)

        QMetaObject.connectSlotsByName(Compare)
    # setupUi

    def retranslateUi(self, Compare):
        Compare.setWindowTitle(QCoreApplication.translate("Compare", u"Conflict detected in keyfiles.", None))
#if QT_CONFIG(tooltip)
        Compare.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.currentLabel.setToolTip(QCoreApplication.translate("Compare", u"Current Keyfile Version", None))
#endif // QT_CONFIG(tooltip)
        self.currentLabel.setText(QCoreApplication.translate("Compare", u"Current Keyfile Version", None))
#if QT_CONFIG(tooltip)
        self.importedLabel.setToolTip(QCoreApplication.translate("Compare", u"Imported Keyfile Version", None))
#endif // QT_CONFIG(tooltip)
        self.importedLabel.setText(QCoreApplication.translate("Compare", u"Imported Keyfile Version", None))
#if QT_CONFIG(tooltip)
        self.currentTreeView.setToolTip(QCoreApplication.translate("Compare", u"Keyfile content from the database", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.importedTreeView.setToolTip(QCoreApplication.translate("Compare", u"Keyfile content from the disk", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.textBrowser.setToolTip(QCoreApplication.translate("Compare", u"Details of the selected file", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("Compare", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("Compare", u"Close", None))
    # retranslateUi

