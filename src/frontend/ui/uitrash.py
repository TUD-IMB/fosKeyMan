# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'trash.ui'
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
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Trash(object):
    def setupUi(self, Trash):
        if not Trash.objectName():
            Trash.setObjectName(u"Trash")
        Trash.resize(513, 300)
        Trash.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(Trash)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(Trash)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.tableLayout = QVBoxLayout()
        self.tableLayout.setObjectName(u"tableLayout")
        self.tableWidget = QTableWidget(Trash)
        self.tableWidget.setObjectName(u"tableWidget")

        self.tableLayout.addWidget(self.tableWidget)


        self.verticalLayout_2.addLayout(self.tableLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.emptyButton = QPushButton(Trash)
        self.emptyButton.setObjectName(u"emptyButton")
        self.emptyButton.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_4.addWidget(self.emptyButton)

        self.closeButton = QPushButton(Trash)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout_4.addWidget(self.closeButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.retranslateUi(Trash)

        QMetaObject.connectSlotsByName(Trash)
    # setupUi

    def retranslateUi(self, Trash):
        Trash.setWindowTitle(QCoreApplication.translate("Trash", u"Deleted Keyfiles", None))
        self.label.setText(QCoreApplication.translate("Trash", u"Manage deleted keyfiles. You can restore or permanently remove them from the trash.", None))
#if QT_CONFIG(tooltip)
        self.emptyButton.setToolTip(QCoreApplication.translate("Trash", u"Confirm your selections", None))
#endif // QT_CONFIG(tooltip)
        self.emptyButton.setText(QCoreApplication.translate("Trash", u"Empty Trash", None))
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("Trash", u"Cancel and Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("Trash", u"Close", None))
    # retranslateUi

