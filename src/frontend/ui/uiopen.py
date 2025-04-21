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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Open(object):
    def setupUi(self, Open):
        if not Open.objectName():
            Open.setObjectName(u"Open")
        Open.resize(400, 212)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Open.sizePolicy().hasHeightForWidth())
        Open.setSizePolicy(sizePolicy)
        Open.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(Open)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.label_3 = QLabel(Open)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.acLineEdit = QLineEdit(Open)
        self.acLineEdit.setObjectName(u"acLineEdit")

        self.horizontalLayout_2.addWidget(self.acLineEdit)

        self.acBrowseButton = QPushButton(Open)
        self.acBrowseButton.setObjectName(u"acBrowseButton")

        self.horizontalLayout_2.addWidget(self.acBrowseButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.label_2 = QLabel(Open)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.label_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.deacLineEdit = QLineEdit(Open)
        self.deacLineEdit.setObjectName(u"deacLineEdit")

        self.horizontalLayout_3.addWidget(self.deacLineEdit)

        self.deacBrowseButton = QPushButton(Open)
        self.deacBrowseButton.setObjectName(u"deacBrowseButton")

        self.horizontalLayout_3.addWidget(self.deacBrowseButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.label = QLabel(Open)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.trashLineEdit = QLineEdit(Open)
        self.trashLineEdit.setObjectName(u"trashLineEdit")

        self.horizontalLayout.addWidget(self.trashLineEdit)

        self.trashBrowseButton = QPushButton(Open)
        self.trashBrowseButton.setObjectName(u"trashBrowseButton")

        self.horizontalLayout.addWidget(self.trashBrowseButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
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
        self.label.setText(QCoreApplication.translate("Open", u"Trash Directory", None))
        self.trashBrowseButton.setText(QCoreApplication.translate("Open", u"Browse", None))
#if QT_CONFIG(tooltip)
        self.cancelButton.setToolTip(QCoreApplication.translate("Open", u"Cancel and Close", None))
#endif // QT_CONFIG(tooltip)
        self.cancelButton.setText(QCoreApplication.translate("Open", u"Cancel", None))
#if QT_CONFIG(tooltip)
        self.confirmButton.setToolTip(QCoreApplication.translate("Open", u"Confirm your selections", None))
#endif // QT_CONFIG(tooltip)
        self.confirmButton.setText(QCoreApplication.translate("Open", u"Confirm", None))
    # retranslateUi

