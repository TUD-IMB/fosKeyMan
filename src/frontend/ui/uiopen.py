# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'open.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Open(object):
    def setupUi(self, Open):
        if not Open.objectName():
            Open.setObjectName(u"Open")
        Open.resize(400, 300)
        Open.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(Open)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(Open)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.acLineEdit = QLineEdit(Open)
        self.acLineEdit.setObjectName(u"acLineEdit")

        self.horizontalLayout_2.addWidget(self.acLineEdit)

        self.acBrowseButton = QPushButton(Open)
        self.acBrowseButton.setObjectName(u"acBrowseButton")

        self.horizontalLayout_2.addWidget(self.acBrowseButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.label_2 = QLabel(Open)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.deacLineEdit = QLineEdit(Open)
        self.deacLineEdit.setObjectName(u"deacLineEdit")

        self.horizontalLayout_3.addWidget(self.deacLineEdit)

        self.deacBrowseButton = QPushButton(Open)
        self.deacBrowseButton.setObjectName(u"deacBrowseButton")

        self.horizontalLayout_3.addWidget(self.deacBrowseButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.label = QLabel(Open)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.dbLineEdit = QLineEdit(Open)
        self.dbLineEdit.setObjectName(u"dbLineEdit")

        self.horizontalLayout.addWidget(self.dbLineEdit)

        self.dbBrowseButton = QPushButton(Open)
        self.dbBrowseButton.setObjectName(u"dbBrowseButton")

        self.horizontalLayout.addWidget(self.dbBrowseButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 50)
        self.label_4 = QLabel(Open)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.createOneButton = QPushButton(Open)
        self.createOneButton.setObjectName(u"createOneButton")
        self.createOneButton.setStyleSheet(u"QPushButton {\n"
"    color: blue;\n"
"    border: none;\n"
"    background: none;\n"
"    text-decoration: underline;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    color: darkblue;\n"
"}\n"
"")

        self.horizontalLayout_5.addWidget(self.createOneButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.cancelButton = QPushButton(Open)
        self.cancelButton.setObjectName(u"cancelButton")

        self.horizontalLayout_4.addWidget(self.cancelButton)

        self.confirmButton = QPushButton(Open)
        self.confirmButton.setObjectName(u"confirmButton")
        self.confirmButton.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_4.addWidget(self.confirmButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.retranslateUi(Open)

        QMetaObject.connectSlotsByName(Open)
    # setupUi

    def retranslateUi(self, Open):
        Open.setWindowTitle(QCoreApplication.translate("Open", u"Open", None))
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("Open", u"Select the activated keyfile directory", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Open", u"Activated Directory", None))
#if QT_CONFIG(tooltip)
        self.acLineEdit.setToolTip(QCoreApplication.translate("Open", u"Path to activated keyfile directory", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.acBrowseButton.setToolTip(QCoreApplication.translate("Open", u"Browse for activated directory", None))
#endif // QT_CONFIG(tooltip)
        self.acBrowseButton.setText(QCoreApplication.translate("Open", u"Browse", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Open", u"Select the deactivated keyfile directory", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Open", u"Deactivated Directory", None))
#if QT_CONFIG(tooltip)
        self.deacLineEdit.setToolTip(QCoreApplication.translate("Open", u"Path to deactivated keyfile directory", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.deacBrowseButton.setToolTip(QCoreApplication.translate("Open", u"Browse for deactivated directory", None))
#endif // QT_CONFIG(tooltip)
        self.deacBrowseButton.setText(QCoreApplication.translate("Open", u"Browse", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Open", u"Select the database file", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Open", u"Database", None))
#if QT_CONFIG(tooltip)
        self.dbLineEdit.setToolTip(QCoreApplication.translate("Open", u"Path to database file", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.dbBrowseButton.setToolTip(QCoreApplication.translate("Open", u"Browse for database file", None))
#endif // QT_CONFIG(tooltip)
        self.dbBrowseButton.setText(QCoreApplication.translate("Open", u"Browse", None))
        self.label_4.setText(QCoreApplication.translate("Open", u"No database?", None))
        self.createOneButton.setText(QCoreApplication.translate("Open", u"Create One!", None))
#if QT_CONFIG(tooltip)
        self.cancelButton.setToolTip(QCoreApplication.translate("Open", u"Cancel and Close", None))
#endif // QT_CONFIG(tooltip)
        self.cancelButton.setText(QCoreApplication.translate("Open", u"Cancel", None))
#if QT_CONFIG(tooltip)
        self.confirmButton.setToolTip(QCoreApplication.translate("Open", u"Confirm your selections", None))
#endif // QT_CONFIG(tooltip)
        self.confirmButton.setText(QCoreApplication.translate("Open", u"Confirm", None))
    # retranslateUi

