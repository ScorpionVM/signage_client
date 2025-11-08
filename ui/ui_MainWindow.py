# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
    QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(893, 777)
        MainWindow.setStyleSheet(u"QMainWindow { background-color: black; }")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_webview = QWidget()
        self.page_webview.setObjectName(u"page_webview")
        self.verticalLayout = QVBoxLayout(self.page_webview)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.webEngineView = QWebEngineView(self.page_webview)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setUrl(QUrl(u"about:blank"))

        self.verticalLayout.addWidget(self.webEngineView)

        self.stackedWidget.addWidget(self.page_webview)
        self.page_menu = QWidget()
        self.page_menu.setObjectName(u"page_menu")
        self.page_menu.setStyleSheet(u"QWidget { background-color: white; }")
        self.verticalLayout_2 = QVBoxLayout(self.page_menu)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 2, 1, 1, 1)

        self.frame = QFrame(self.page_menu)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(22)
        self.label.setFont(font)

        self.verticalLayout_3.addWidget(self.label)

        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.pushButton_menu_back = QPushButton(self.frame)
        self.pushButton_menu_back.setObjectName(u"pushButton_menu_back")
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(True)
        self.pushButton_menu_back.setFont(font1)
        self.pushButton_menu_back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_menu_back.setStyleSheet(u"QPushButton { padding: 15px; }")

        self.verticalLayout_3.addWidget(self.pushButton_menu_back)

        self.pushButton_menu_settings = QPushButton(self.frame)
        self.pushButton_menu_settings.setObjectName(u"pushButton_menu_settings")
        self.pushButton_menu_settings.setFont(font1)
        self.pushButton_menu_settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_menu_settings.setStyleSheet(u"QPushButton { padding: 15px; }")

        self.verticalLayout_3.addWidget(self.pushButton_menu_settings)

        self.pushButton_menu_close_app = QPushButton(self.frame)
        self.pushButton_menu_close_app.setObjectName(u"pushButton_menu_close_app")
        self.pushButton_menu_close_app.setFont(font1)
        self.pushButton_menu_close_app.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_menu_close_app.setStyleSheet(u"QPushButton { padding: 15px; }")

        self.verticalLayout_3.addWidget(self.pushButton_menu_close_app)


        self.gridLayout.addWidget(self.frame, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 3, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.stackedWidget.addWidget(self.page_menu)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.page_settings.setStyleSheet(u"QWidget { background-color: white; }")
        self.verticalLayout_4 = QVBoxLayout(self.page_settings)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_settings_close = QPushButton(self.page_settings)
        self.pushButton_settings_close.setObjectName(u"pushButton_settings_close")
        self.pushButton_settings_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.pushButton_settings_close)

        self.label_2 = QLabel(self.page_settings)
        self.label_2.setObjectName(u"label_2")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        font2.setItalic(True)
        font2.setUnderline(False)
        self.label_2.setFont(font2)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.scrollArea = QScrollArea(self.page_settings)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 859, 1337))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEdit_gbox_network_profile = QLineEdit(self.groupBox)
        self.lineEdit_gbox_network_profile.setObjectName(u"lineEdit_gbox_network_profile")

        self.horizontalLayout_3.addWidget(self.lineEdit_gbox_network_profile)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.lineEdit_gbox_network_host = QLineEdit(self.groupBox)
        self.lineEdit_gbox_network_host.setObjectName(u"lineEdit_gbox_network_host")

        self.horizontalLayout_3.addWidget(self.lineEdit_gbox_network_host)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.pushButton_gbox_network_add = QPushButton(self.groupBox)
        self.pushButton_gbox_network_add.setObjectName(u"pushButton_gbox_network_add")
        self.pushButton_gbox_network_add.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.pushButton_gbox_network_add)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.tableWidget_gbox_network = QTableWidget(self.groupBox)
        if (self.tableWidget_gbox_network.columnCount() < 4):
            self.tableWidget_gbox_network.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_gbox_network.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_gbox_network.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_gbox_network.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_gbox_network.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tableWidget_gbox_network.setObjectName(u"tableWidget_gbox_network")
        self.tableWidget_gbox_network.verticalHeader().setVisible(False)

        self.verticalLayout_6.addWidget(self.tableWidget_gbox_network)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        font3 = QFont()
        font3.setPointSize(10)
        self.label_6.setFont(font3)

        self.verticalLayout_6.addWidget(self.label_6)

        self.line_4 = QFrame(self.groupBox)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line_4)

        self.verticalSpacer_9 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_9)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_24 = QLabel(self.groupBox)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_4.addWidget(self.label_24, 1, 2, 1, 1)

        self.label_23 = QLabel(self.groupBox)
        self.label_23.setObjectName(u"label_23")
        font4 = QFont()
        font4.setBold(True)
        font4.setItalic(True)
        self.label_23.setFont(font4)

        self.gridLayout_4.addWidget(self.label_23, 0, 0, 1, 1)

        self.spinBox_gbox_network_config_reconnect_retries = QSpinBox(self.groupBox)
        self.spinBox_gbox_network_config_reconnect_retries.setObjectName(u"spinBox_gbox_network_config_reconnect_retries")
        self.spinBox_gbox_network_config_reconnect_retries.setMinimum(2)
        self.spinBox_gbox_network_config_reconnect_retries.setMaximum(5)
        self.spinBox_gbox_network_config_reconnect_retries.setValue(2)

        self.gridLayout_4.addWidget(self.spinBox_gbox_network_config_reconnect_retries, 1, 0, 1, 1)

        self.label_25 = QLabel(self.groupBox)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_4.addWidget(self.label_25, 2, 2, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_8, 1, 3, 1, 1)

        self.spinBox_gbox_network_config_timeout = QSpinBox(self.groupBox)
        self.spinBox_gbox_network_config_timeout.setObjectName(u"spinBox_gbox_network_config_timeout")
        self.spinBox_gbox_network_config_timeout.setMinimum(30)
        self.spinBox_gbox_network_config_timeout.setMaximum(120)

        self.gridLayout_4.addWidget(self.spinBox_gbox_network_config_timeout, 2, 0, 1, 1)

        self.label_gbox_network_color_reconnect_retries = QLabel(self.groupBox)
        self.label_gbox_network_color_reconnect_retries.setObjectName(u"label_gbox_network_color_reconnect_retries")
        self.label_gbox_network_color_reconnect_retries.setMinimumSize(QSize(25, 25))
        self.label_gbox_network_color_reconnect_retries.setMaximumSize(QSize(25, 25))
        self.label_gbox_network_color_reconnect_retries.setFrameShape(QFrame.Shape.Box)

        self.gridLayout_4.addWidget(self.label_gbox_network_color_reconnect_retries, 1, 1, 1, 1)

        self.label_gbox_network_color_timeout = QLabel(self.groupBox)
        self.label_gbox_network_color_timeout.setObjectName(u"label_gbox_network_color_timeout")
        self.label_gbox_network_color_timeout.setMinimumSize(QSize(25, 25))
        self.label_gbox_network_color_timeout.setMaximumSize(QSize(25, 25))
        self.label_gbox_network_color_timeout.setFrameShape(QFrame.Shape.Box)

        self.gridLayout_4.addWidget(self.label_gbox_network_color_timeout, 2, 1, 1, 1)


        self.verticalLayout_6.addLayout(self.gridLayout_4)

        self.line_5 = QFrame(self.groupBox)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line_5)

        self.verticalSpacer_10 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_10)

        self.label_26 = QLabel(self.groupBox)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setWordWrap(True)

        self.verticalLayout_6.addWidget(self.label_26)


        self.verticalLayout_5.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tableWidget_gbox_screen = QTableWidget(self.groupBox_2)
        if (self.tableWidget_gbox_screen.columnCount() < 6):
            self.tableWidget_gbox_screen.setColumnCount(6)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget_gbox_screen.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_gbox_screen.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_gbox_screen.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_gbox_screen.setHorizontalHeaderItem(3, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_gbox_screen.setHorizontalHeaderItem(4, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_gbox_screen.setHorizontalHeaderItem(5, __qtablewidgetitem9)
        self.tableWidget_gbox_screen.setObjectName(u"tableWidget_gbox_screen")
        self.tableWidget_gbox_screen.verticalHeader().setVisible(False)

        self.verticalLayout_7.addWidget(self.tableWidget_gbox_screen)

        self.label_22 = QLabel(self.groupBox_2)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font3)

        self.verticalLayout_7.addWidget(self.label_22)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)

        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_2.addWidget(self.label_11, 2, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 1, 4, 1, 1)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font4)

        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)

        self.spinBox_gbox_cache_image_files_count = QSpinBox(self.groupBox_3)
        self.spinBox_gbox_cache_image_files_count.setObjectName(u"spinBox_gbox_cache_image_files_count")
        self.spinBox_gbox_cache_image_files_count.setMinimum(50)
        self.spinBox_gbox_cache_image_files_count.setMaximum(250)

        self.gridLayout_2.addWidget(self.spinBox_gbox_cache_image_files_count, 1, 1, 1, 1)

        self.spinBox_gbox_cache_image_max_size = QSpinBox(self.groupBox_3)
        self.spinBox_gbox_cache_image_max_size.setObjectName(u"spinBox_gbox_cache_image_max_size")
        self.spinBox_gbox_cache_image_max_size.setMinimum(50)
        self.spinBox_gbox_cache_image_max_size.setMaximum(1024)

        self.gridLayout_2.addWidget(self.spinBox_gbox_cache_image_max_size, 2, 1, 1, 1)

        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 1, 3, 1, 1)

        self.label_27 = QLabel(self.groupBox_3)
        self.label_27.setObjectName(u"label_27")

        self.gridLayout_2.addWidget(self.label_27, 1, 2, 1, 1)

        self.label_28 = QLabel(self.groupBox_3)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_2.addWidget(self.label_28, 2, 2, 1, 1)


        self.verticalLayout_8.addLayout(self.gridLayout_2)

        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font3)

        self.verticalLayout_8.addWidget(self.label_12)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_8.addItem(self.verticalSpacer_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_19 = QLabel(self.groupBox_3)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font4)

        self.horizontalLayout_4.addWidget(self.label_19)

        self.label_gbox_cache_image_cache_info = QLabel(self.groupBox_3)
        self.label_gbox_cache_image_cache_info.setObjectName(u"label_gbox_cache_image_cache_info")

        self.horizontalLayout_4.addWidget(self.label_gbox_cache_image_cache_info)

        self.pushButton_gbox_cache_image_clear_cache = QPushButton(self.groupBox_3)
        self.pushButton_gbox_cache_image_clear_cache.setObjectName(u"pushButton_gbox_cache_image_clear_cache")
        self.pushButton_gbox_cache_image_clear_cache.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_4.addWidget(self.pushButton_gbox_cache_image_clear_cache)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)


        self.verticalLayout_8.addLayout(self.horizontalLayout_4)

        self.line_2 = QFrame(self.groupBox_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_8.addWidget(self.line_2)

        self.verticalSpacer_8 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_8.addItem(self.verticalSpacer_8)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_15 = QLabel(self.groupBox_3)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_3.addWidget(self.label_15, 1, 3, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 1, 4, 1, 1)

        self.label_17 = QLabel(self.groupBox_3)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_3.addWidget(self.label_17, 2, 3, 1, 1)

        self.label_14 = QLabel(self.groupBox_3)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_3.addWidget(self.label_14, 1, 0, 1, 1)

        self.label_16 = QLabel(self.groupBox_3)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_3.addWidget(self.label_16, 2, 0, 1, 1)

        self.label_13 = QLabel(self.groupBox_3)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font4)

        self.gridLayout_3.addWidget(self.label_13, 0, 0, 1, 1)

        self.spinBox_gbox_cache_video_max_size = QSpinBox(self.groupBox_3)
        self.spinBox_gbox_cache_video_max_size.setObjectName(u"spinBox_gbox_cache_video_max_size")
        self.spinBox_gbox_cache_video_max_size.setMinimum(100)
        self.spinBox_gbox_cache_video_max_size.setMaximum(2048)

        self.gridLayout_3.addWidget(self.spinBox_gbox_cache_video_max_size, 2, 1, 1, 1)

        self.spinBox_gbox_cache_video_files_count = QSpinBox(self.groupBox_3)
        self.spinBox_gbox_cache_video_files_count.setObjectName(u"spinBox_gbox_cache_video_files_count")
        self.spinBox_gbox_cache_video_files_count.setMinimum(25)
        self.spinBox_gbox_cache_video_files_count.setMaximum(100)

        self.gridLayout_3.addWidget(self.spinBox_gbox_cache_video_files_count, 1, 1, 1, 1)

        self.label_29 = QLabel(self.groupBox_3)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_3.addWidget(self.label_29, 1, 2, 1, 1)

        self.label_30 = QLabel(self.groupBox_3)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_3.addWidget(self.label_30, 2, 2, 1, 1)


        self.verticalLayout_8.addLayout(self.gridLayout_3)

        self.label_18 = QLabel(self.groupBox_3)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font3)

        self.verticalLayout_8.addWidget(self.label_18)

        self.verticalSpacer_6 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_8.addItem(self.verticalSpacer_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_20 = QLabel(self.groupBox_3)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font4)

        self.horizontalLayout_5.addWidget(self.label_20)

        self.label_gbox_cache_video_cache_info = QLabel(self.groupBox_3)
        self.label_gbox_cache_video_cache_info.setObjectName(u"label_gbox_cache_video_cache_info")

        self.horizontalLayout_5.addWidget(self.label_gbox_cache_video_cache_info)

        self.pushButton_gbox_cache_video_clear_cache = QPushButton(self.groupBox_3)
        self.pushButton_gbox_cache_video_clear_cache.setObjectName(u"pushButton_gbox_cache_video_clear_cache")
        self.pushButton_gbox_cache_video_clear_cache.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_5.addWidget(self.pushButton_gbox_cache_video_clear_cache)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)


        self.verticalLayout_8.addLayout(self.horizontalLayout_5)

        self.line_3 = QFrame(self.groupBox_3)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_8.addWidget(self.line_3)

        self.verticalSpacer_7 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_8.addItem(self.verticalSpacer_7)

        self.label_21 = QLabel(self.groupBox_3)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setWordWrap(True)

        self.verticalLayout_8.addWidget(self.label_21)


        self.verticalLayout_5.addWidget(self.groupBox_3)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.scrollArea)

        self.label_31 = QLabel(self.page_settings)
        self.label_31.setObjectName(u"label_31")

        self.verticalLayout_4.addWidget(self.label_31)

        self.stackedWidget.addWidget(self.page_settings)

        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 893, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Signage Menu", None))
        self.pushButton_menu_back.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.pushButton_menu_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.pushButton_menu_close_app.setText(QCoreApplication.translate("MainWindow", u"Close App", None))
        self.pushButton_settings_close.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"App Config", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Network", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Profile:", None))
        self.lineEdit_gbox_network_profile.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Local Host", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Host:", None))
        self.lineEdit_gbox_network_host.setPlaceholderText(QCoreApplication.translate("MainWindow", u"http://127.0.0.1:8080", None))
        self.label_5.setText("")
        self.pushButton_gbox_network_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        ___qtablewidgetitem = self.tableWidget_gbox_network.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"id", None));
        ___qtablewidgetitem1 = self.tableWidget_gbox_network.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Profile", None));
        ___qtablewidgetitem2 = self.tableWidget_gbox_network.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Host", None));
        ___qtablewidgetitem3 = self.tableWidget_gbox_network.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Priority", None));
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"(i) App will try to reconnect to another profile in priority order", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"(maximum number of reconnection attempts min: 2 & max: 5)", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Config", None))
        self.spinBox_gbox_network_config_reconnect_retries.setSuffix(QCoreApplication.translate("MainWindow", u" x", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"(timeout for connecting to the host min: 30 sec & max: 2 min)", None))
        self.spinBox_gbox_network_config_timeout.setSuffix(QCoreApplication.translate("MainWindow", u" sec", None))
        self.spinBox_gbox_network_config_timeout.setPrefix("")
        self.label_gbox_network_color_reconnect_retries.setText("")
        self.label_gbox_network_color_timeout.setText("")
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Network Control</span>: Do not set the timeout too big if you have already set a high number of connection retries, as this may cause a significant delay without reconnecting to another host.<br/><span style=\" font-weight:700;\">Recommended</span>: 2 retries with a 30-second timeout</p></body></html>", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Screen", None))
        ___qtablewidgetitem4 = self.tableWidget_gbox_screen.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"id", None));
        ___qtablewidgetitem5 = self.tableWidget_gbox_screen.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Pos", None));
        ___qtablewidgetitem6 = self.tableWidget_gbox_screen.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Active", None));
        ___qtablewidgetitem7 = self.tableWidget_gbox_screen.horizontalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Geometry", None));
        ___qtablewidgetitem8 = self.tableWidget_gbox_screen.horizontalHeaderItem(4)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Profile", None));
        ___qtablewidgetitem9 = self.tableWidget_gbox_screen.horizontalHeaderItem(5)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"In Use", None));
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"(i) All active screens and profiles that are in use are displayed here.", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Cache", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Files:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Max Size:", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"(total size min: 50MB & max: 1GB)", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Images", None))
        self.spinBox_gbox_cache_image_files_count.setSuffix(QCoreApplication.translate("MainWindow", u" x", None))
        self.spinBox_gbox_cache_image_max_size.setSuffix(QCoreApplication.translate("MainWindow", u" MB", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"(file counts min: 50 & max: 250)", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"(i) The image cache is a maximum of 250 files or a maximum of 1 GB of disk space used.", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Cache:", None))
        self.label_gbox_cache_image_cache_info.setText(QCoreApplication.translate("MainWindow", u"0 files with a total size of 0 MB  ", None))
        self.pushButton_gbox_cache_image_clear_cache.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"(file counts min: 25 & max: 100)", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"(total size min: 100MB & max: 2GB)", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Files:", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Max Size:", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Videos", None))
        self.spinBox_gbox_cache_video_max_size.setSuffix(QCoreApplication.translate("MainWindow", u" MB", None))
        self.spinBox_gbox_cache_video_files_count.setSuffix(QCoreApplication.translate("MainWindow", u" x", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"(i) The video cache is a maximum of 100 files or a maximum of 2 GB of disk space used.", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Cache:", None))
        self.label_gbox_cache_video_cache_info.setText(QCoreApplication.translate("MainWindow", u"0 files with a total size of 0 MB  ", None))
        self.pushButton_gbox_cache_video_clear_cache.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Cache Control</span>: If the cache is larger, then the application can store more files and run them locally without downloading them before display. <br/><span style=\" font-weight:700;\">Warning</span>: The larger the allocated cache, the more space the application occupies.</p></body></html>", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"(i) All changes are saved automatically.", None))
    # retranslateUi

