# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'column.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
from frontend.ui import toolicons_rc

class Ui_Column(object):
    def setupUi(self, Column):
        if not Column.objectName():
            Column.setObjectName(u"Column")
        Column.resize(400, 300)
        Column.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(Column)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.label = QLabel(Column)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.autoLoadButton = QPushButton(Column)
        self.autoLoadButton.setObjectName(u"autoLoadButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autoLoadButton.sizePolicy().hasHeightForWidth())
        self.autoLoadButton.setSizePolicy(sizePolicy)
        self.autoLoadButton.setStyleSheet(u"QPushButton {\n"
"    border: none; \n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: lightgray;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: lightblue;\n"
"}\n"
"")
        icon = QIcon()
        icon.addFile(u":/icons/icons/scan.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.autoLoadButton.setIcon(icon)
        self.autoLoadButton.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.autoLoadButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.tableLayout = QVBoxLayout()
        self.tableLayout.setObjectName(u"tableLayout")
        self.tableWidget = QTableWidget(Column)
        self.tableWidget.setObjectName(u"tableWidget")

        self.tableLayout.addWidget(self.tableWidget)


        self.verticalLayout_2.addLayout(self.tableLayout)

        self.addTableWidget = QTableWidget(Column)
        self.addTableWidget.setObjectName(u"addTableWidget")

        self.verticalLayout_2.addWidget(self.addTableWidget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.cancelButton = QPushButton(Column)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_4.addWidget(self.cancelButton)

        self.confirmButton = QPushButton(Column)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_4.addWidget(self.confirmButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.retranslateUi(Column)

        QMetaObject.connectSlotsByName(Column)
    # setupUi

    def retranslateUi(self, Column):
        Column.setWindowTitle(QCoreApplication.translate("Column", u"Table Column", None))
        self.label.setText(QCoreApplication.translate("Column", u"Configure metadata keys to display as table columns.", None))
#if QT_CONFIG(tooltip)
        self.autoLoadButton.setToolTip(QCoreApplication.translate("Column", u"Load from json file.", None))
#endif // QT_CONFIG(tooltip)
        self.autoLoadButton.setText("")
#if QT_CONFIG(tooltip)
        self.cancelButton.setToolTip(QCoreApplication.translate("Column", u"Cancel and Close", None))
#endif // QT_CONFIG(tooltip)
        self.cancelButton.setText(QCoreApplication.translate("Column", u"Cancel", None))
#if QT_CONFIG(tooltip)
        self.confirmButton.setToolTip(QCoreApplication.translate("Column", u"Confirm your selections", None))
#endif // QT_CONFIG(tooltip)
        self.confirmButton.setText(QCoreApplication.translate("Column", u"Confirm", None))
    # retranslateUi

