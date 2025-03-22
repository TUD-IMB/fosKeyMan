# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Edit(object):
    def setupUi(self, Edit):
        if not Edit.objectName():
            Edit.setObjectName(u"Edit")
        Edit.resize(400, 300)
        Edit.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(Edit)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableLayout = QVBoxLayout()
        self.tableLayout.setObjectName(u"tableLayout")
        self.tableWidget = QTableWidget(Edit)
        self.tableWidget.setObjectName(u"tableWidget")

        self.tableLayout.addWidget(self.tableWidget)


        self.verticalLayout_2.addLayout(self.tableLayout)

        self.addTableWidget = QTableWidget(Edit)
        self.addTableWidget.setObjectName(u"addTableWidget")

        self.verticalLayout_2.addWidget(self.addTableWidget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.cancelButton = QPushButton(Edit)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_4.addWidget(self.cancelButton)

        self.confirmButton = QPushButton(Edit)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_4.addWidget(self.confirmButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.retranslateUi(Edit)

        QMetaObject.connectSlotsByName(Edit)
    # setupUi

    def retranslateUi(self, Edit):
        Edit.setWindowTitle(QCoreApplication.translate("Edit", u"Edit", None))
#if QT_CONFIG(tooltip)
        self.cancelButton.setToolTip(QCoreApplication.translate("Edit", u"Cancel and Close", None))
#endif // QT_CONFIG(tooltip)
        self.cancelButton.setText(QCoreApplication.translate("Edit", u"Cancel", None))
#if QT_CONFIG(tooltip)
        self.confirmButton.setToolTip(QCoreApplication.translate("Edit", u"Confirm your selections", None))
#endif // QT_CONFIG(tooltip)
        self.confirmButton.setText(QCoreApplication.translate("Edit", u"Confirm", None))
    # retranslateUi

