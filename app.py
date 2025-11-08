#!./.venv/bin/python

import json
import os
import sys
import uuid
import time

import requests
from PySide6.QtCore import (QEasingCurve, QPoint, QPropertyAnimation, QTimer,
                            QUrl, Slot)
from PySide6.QtGui import QAction, QKeyEvent, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QGraphicsOpacityEffect,
                               QHBoxLayout, QLabel, QMainWindow, QMenu,
                               QTableWidgetItem, QVBoxLayout, QWidget)

from ui.ui_MainWindow import Ui_MainWindow

is_frozen = getattr(sys, 'frozen', False)

WORK_PATH = "./_internal/local" if is_frozen else "./local"
WORK_PATH = os.path.abspath(WORK_PATH)

if not os.path.exists(WORK_PATH):
    os.makedirs(WORK_PATH, exist_ok=False)

CONFIG_FILE = os.path.join(WORK_PATH, "config/config.json")
CACHE_FOLDER = os.path.join(WORK_PATH, "cache")
HTML_FILE = os.path.join(WORK_PATH, "html")

class Toast(QWidget):
    Error = "#ff0000"
    Success = "#00ff95"
    Warning = "#fbff00"
    Info = "#00eeff"

    def __init__(self, parent, message, flag_color=Info, duration=3000):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setStyleSheet("QWidget { background-color: white; }")

        self.last_toast:Toast = None
        self.active:bool = True

        # Layout principal
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        # Linie verticală stânga
        self.flag = QWidget()
        self.flag.setFixedWidth(5)
        self.flag.setStyleSheet(f"background-color: {flag_color};")
        layout.addWidget(self.flag)
        
        # Content
        self.label = QLabel(message)
        self.label.setStyleSheet("padding: 10px;")
        self.label.setWordWrap(True)
        self.label.setMinimumWidth(200)
        self.label.setMaximumWidth(300)
        layout.addWidget(self.label)
        
        self.setLayout(layout)
        self.adjustSize()

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b'opacity')
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # self.parent = parent
        if not hasattr(parent, "toasts"):
            parent.toasts = []

        self.last_toast = parent.toasts[-1] if parent.toasts and parent.toasts[-1].active else None
        parent.toasts.append(self)

        # Poziționare în colțul dreapta-sus al parent
        self.move_to_top_right()
        self.fade_in()
        
        # Timer pentru auto-close
        QTimer.singleShot(duration, self.fade_out)
        pass
    
    def move_to_top_right(self):
        parent_geom = self.parent().geometry()
        x = parent_geom.x() + parent_geom.width() - self.width() - 20  # 20px padding

        if self.last_toast is None:
            y = parent_geom.y() + 20  # 20px de sus
        else:
            y = self.last_toast.y() + self.last_toast.height() + 10

        self.move(x, y)
        pass

    def fade_in(self):
        self.fade_animation.stop()
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setDuration(400)
        self.fade_animation.start()
        self.show()
        pass

    def fade_out(self):
        self.fade_animation.stop()
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.setDuration(500)
        self.fade_animation.finished.connect(self.close_toast)
        self.fade_animation.start()
        pass

    def close_toast(self):
        self.active = False
        self.close()

        # curăță lista din parent
        if hasattr(self.parent, "toasts"):
            self.parent.toasts = [t for t in self.parent.toasts if t.active]
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Browser PySide6")

        # Connect
        # --- Menu ---
        self.ui.pushButton_menu_back.clicked.connect(self.clicked_pushButton_menu_back)
        self.ui.pushButton_menu_settings.clicked.connect(self.clicked_pushButton_menu_settings)
        self.ui.pushButton_menu_close_app.clicked.connect(self.clicked_pushButton_menu_close_app)

        # --- Settings ---
        self.ui.pushButton_settings_close.clicked.connect(self.clicked_pushButton_settings_close)
        
        # --- Settings - Network ---
        self.ui.pushButton_gbox_network_add.clicked.connect(self.clicked_pushButton_gbox_network_add)
        self.ui.spinBox_gbox_network_config_reconnect_retries.valueChanged.connect(self.changed_spinBox_gbox_network_config_reconnect_retries)
        self.ui.spinBox_gbox_network_config_timeout.valueChanged.connect(self.changed_spinBox_gbox_network_config_timeout)
        self.ui.tableWidget_gbox_network.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableWidget_gbox_network.customContextMenuRequested.connect(self.customContextMenu_tableWidget_gbox_network)

        # --- Settings - Screen ---
        self.ui.tableWidget_gbox_screen.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.ui.tableWidget_gbox_screen.customContextMenuRequested.connect(self.customContextMenu_gbox_screen)

        # --- Settings - Cache ---

        # Vars
        self.config:dict = None

        # Load
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_webview)

        self.load_config()
        self.connect_page(firstrun=True)
        # self.open_child_widget()

        QTimer.singleShot(5000, self.connect_page)

        # Debug
        # self.clicked_pushButton_menu_settings()
        pass

    """ CONTROL APP """
    @Slot()
    def connect_page(self, url:str=None, firstrun=False):
        network = self.config.get("network", None)

        missconfigured = False
        if network is None:
            missconfigured = True

        elif not len(network.get("profiles", [])):
            missconfigured = True

        if firstrun:
            missconfigured = True
            url = None

        if missconfigured and url is None:
            file_path = os.path.join(HTML_FILE, "default.html")

            if not os.path.exists(file_path):
                self.ui.webEngineView.setHtml("<h1>Please reinstall the app!</h1>")
                return

            self.ui.webEngineView.setUrl(QUrl.fromLocalFile(file_path))
        
        elif url is not None:
            try:
                res = requests.get(url, timeout=network['config']['timeout'])

                if res.status_code == 200:
                    self.ui.webEngineView.setUrl(QUrl(url))

                    self.show_toast(Toast.Success, "Connected Successful!")
                else:
                    self.show_toast(Toast.Error, "Timeout! Try again...")
            except Exception as e:
                self.show_toast(Toast.Error, "Incorrect Host URL!")
                print(repr(e))
        else:
            profiles = network['profiles']
            connected = False

            for profile in profiles:
                retries = 0
                
                self.show_toast(Toast.Info, "Connect Profile: "+profile['name'])
                while retries < network['config']['retries']:
                    try:
                        res = requests.get(profile["host"], timeout=network['config']['timeout'])

                        if res.status_code == 200:
                            self.ui.webEngineView.setUrl(QUrl(profile['host']))
                            self.show_toast(Toast.Success, "Connected!")
                            connected = True
                            break
                    except Exception as e:
                        print(repr(e))

                    retries += 1
                    self.show_toast(Toast.Error, "Timeout. Try again...")
                
            if not connected:
                self.show_toast(Toast.Warning, "Fall to default! During failed connection!")
        pass

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_F1:
            self.on_escape_pressed()
        else:
            super().keyPressEvent(event)

    def on_escape_pressed(self):
        current_widget = self.ui.stackedWidget.currentWidget()

        if current_widget == self.ui.page_menu:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_webview)

        elif current_widget == self.ui.page_settings:
            return
        
        elif current_widget == self.ui.page_webview:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_menu)
        pass

    """ PAGE - WebView """


    """ PAGE - Menu """
    @Slot()
    def clicked_pushButton_menu_close_app(self):
        self.close()
        pass

    @Slot()
    def clicked_pushButton_menu_settings(self):
        self.populate_page_settings()
        pass

    @Slot()
    def clicked_pushButton_menu_back(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_webview)
        pass

    """ PAGE - Settings """
    def populate_page_settings(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_settings)

        self.populate_page_settings_gbox_network()
        self.populate_page_settings_gbox_screen()
        pass

    @Slot()
    def clicked_pushButton_settings_close(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_webview)
        pass

    """ PAGE - Settings - GBOX [Network] """
    def populate_page_settings_gbox_network(self):
        # CLEAR
        self.ui.lineEdit_gbox_network_profile.clear()
        self.ui.lineEdit_gbox_network_host.clear()

        # LOAD
        profiles = self.config['network']['profiles']

        self.ui.tableWidget_gbox_network.clearContents()
        self.ui.tableWidget_gbox_network.setRowCount(0)
        self.ui.tableWidget_gbox_network.hideColumn(0)

        if profiles:
            profiles.sort(key=lambda x: x['priority'])

            self.ui.tableWidget_gbox_network.setRowCount(len(profiles))

            for i, profile in enumerate(profiles):
                xrow = [
                    profile['id'], profile['name'], profile['host'], profile['priority']
                ]

                for j, val in enumerate(xrow):
                    item = QTableWidgetItem()
                    item.setData(Qt.DisplayRole, val)

                    self.ui.tableWidget_gbox_network.setItem(i,j, item)

            self.ui.tableWidget_gbox_network.resizeColumnsToContents()

        self.ui.spinBox_gbox_network_config_reconnect_retries.setValue(self.config['network']['config']['retries'])
        self.ui.spinBox_gbox_network_config_timeout.setValue(self.config['network']['config']['timeout'])

        self.changed_spinBox_gbox_network_config_reconnect_retries()
        self.changed_spinBox_gbox_network_config_timeout()
        pass

    @Slot()
    def clicked_pushButton_gbox_network_add(self):
        profile = self.ui.lineEdit_gbox_network_profile.text().strip()
        host = self.ui.lineEdit_gbox_network_host.text().strip()

        if not profile:
            self.show_toast(Toast.Error, "Missing Profile")

        if not host:
            self.show_toast(Toast.Error, "Missing Host")

        if not profile or not host:
            return

        rows = self.ui.tableWidget_gbox_network.rowCount()
        
        profile = {
            "id": self.generate_unique_id(),
            "name": profile,
            "host": host,
            "priority": rows
        }

        self.config['network']['profiles'].append(profile)
        self.save_config()

        self.show_toast(Toast.Success, "New Profile Added!")
        self.populate_page_settings_gbox_network()
        pass

    @Slot()
    def changed_spinBox_gbox_network_config_reconnect_retries(self, value:int=None):
        value = self.ui.spinBox_gbox_network_config_reconnect_retries.value()
        xmin = self.ui.spinBox_gbox_network_config_reconnect_retries.minimum()
        xmax = self.ui.spinBox_gbox_network_config_reconnect_retries.maximum()

        hexcol = self.gradient_color(value, xmin, xmax)
        self.ui.label_gbox_network_color_reconnect_retries.setStyleSheet("QLabel { background-color: %s; }" % hexcol)

        self.config['network']['config']['retries'] = value
        self.save_config()
        pass

    @Slot()
    def changed_spinBox_gbox_network_config_timeout(self, value:int=None):
        value = self.ui.spinBox_gbox_network_config_timeout.value()
        xmin = self.ui.spinBox_gbox_network_config_timeout.minimum()
        xmax = self.ui.spinBox_gbox_network_config_timeout.maximum()

        hexcol = self.gradient_color(value, xmin, xmax)
        self.ui.label_gbox_network_color_timeout.setStyleSheet("QLabel { background-color: %s; }" % hexcol)

        self.config['network']['config']['timeout'] = value
        self.save_config()
        pass

    @Slot()
    def customContextMenu_tableWidget_gbox_network(self, pos: QPoint):
        def control_inc_priority(item:QTableWidgetItem):
            profile_id = self.ui.tableWidget_gbox_network.item(item.row(), 0).data(Qt.DisplayRole)

            profiles = self.config['network']["profiles"]

            for profile in profiles:
                if profile['id'] == profile_id:
                    profile["priority"] -= 1.1

            profiles.sort(key=lambda x: x['priority'])

            for i in range(len(profiles)):
                profiles[i]['priority'] = i

            self.config['network']['profiles'] = profiles
            self.save_config()
            self.populate_page_settings_gbox_network()
            pass

        def control_dec_priority(item:QTableWidgetItem):
            profile_id = self.ui.tableWidget_gbox_network.item(item.row(), 0).data(Qt.DisplayRole)

            profiles = self.config['network']["profiles"]

            for profile in profiles:
                if profile['id'] == profile_id:
                    profile["priority"] += 1.1

            profiles.sort(key=lambda x: x['priority'])

            for i in range(len(profiles)):
                profiles[i]['priority'] = i

            self.config['network']['profiles'] = profiles
            self.save_config()
            self.populate_page_settings_gbox_network()
            pass

        def control_connect(item:QTableWidgetItem):
            profile_id = self.ui.tableWidget_gbox_network.item(item.row(), 0).data(Qt.DisplayRole)

            profiles = self.config['network']["profiles"]

            self.show_toast(Toast.Warning, "Connect to new Host!")

            for i, profile in enumerate(profiles):
                if profile['id'] == profile_id:
                    self.connect_page(url=profile['host'])
                    break
            
            pass

        def control_delete(item:QTableWidgetItem):
            profile_id = self.ui.tableWidget_gbox_network.item(item.row(), 0).data(Qt.DisplayRole)

            profiles = self.config['network']["profiles"]

            profiles = [profile for profile in profiles if not profile['id'] == profile_id]
            profiles.sort(key=lambda x: x['priority'])

            for i in range(len(profiles)):
                profiles[i]['priority'] = i

            self.config['network']['profiles'] = profiles
            self.save_config()
            self.populate_page_settings_gbox_network()

            self.show_toast(Toast.Success, "Host deleted!")
            pass

        global_pos = self.ui.tableWidget_gbox_network.viewport().mapToGlobal(pos)

        item = self.ui.tableWidget_gbox_network.itemAt(pos)
        if not item:
            return
        
        menu = QMenu(self)

        action_increase_priority = QAction("Priority (+)", self)
        action_decrease_priority = QAction("Priority (-)", self)
        action_connect = QAction("Connect", self)
        action_delete = QAction("Delete", self)

        menu.addAction(action_increase_priority)
        menu.addAction(action_decrease_priority)
        menu.addAction(action_connect)
        menu.addAction(action_delete)

        action_increase_priority.triggered.connect(lambda: control_inc_priority(item))
        action_decrease_priority.triggered.connect(lambda: control_dec_priority(item))
        action_connect.triggered.connect(lambda: control_connect(item))
        action_delete.triggered.connect(lambda: control_delete(item))

        menu.exec(global_pos)
        pass

    """ PAGE - Settings - GBOX [Screen] """
    def populate_page_settings_gbox_screen(self):
        # LOAD
        self.ui.tableWidget_gbox_screen.clearContents()
        self.ui.tableWidget_gbox_screen.setRowCount(0)
        self.ui.tableWidget_gbox_screen.hideColumn(0)

        screens = app.screens()

        extracted = []
        for i, scr in enumerate(screens):
            geometry = scr.geometry()

            screen_object = {
                "id": self.generate_unique_id(),
                "pos": i,
                "name": scr.name(),
                "active": True,
                "geometry": (geometry.width(), geometry.height()),
                "point": (geometry.x(), geometry.y()),
                "dpi": f"{scr.logicalDotsPerInch():.3f}",
                "exists": True,
                "profile": None,
                "in_use": True
            }

            extracted.append(screen_object)

        config_screens = self.config['screen']
        for scr in config_screens:
            scr['exists'] = False

        for ex_scr in extracted:
            matched = False

            for scr in config_screens:
                if scr['name'] == ex_scr['name'] and tuple(scr['geometry']) == tuple(ex_scr['geometry']):
                    scr['exists'] = True
                    matched = True
                    break
            
            if not matched:
                config_screens.append(ex_scr)

        config_screens = [x for x in config_screens if x['exists']]

        self.config['screen'] = config_screens
        self.save_config()

        self.ui.tableWidget_gbox_screen.setRowCount(len(config_screens))

        for i, scr in enumerate(config_screens):
            xrow = [
                scr['id'], scr['pos'], scr['name'], scr['active'], "{}x{}".format(*scr['geometry']), 
                "x: {} & y: {}".format(*scr['point']), scr['dpi'], scr['profile'], scr['in_use']
            ]

            for j, val in enumerate(xrow):
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, val)

                self.ui.tableWidget_gbox_screen.setItem(i,j, item)

        self.ui.tableWidget_gbox_screen.resizeColumnsToContents()
        pass

    """ FILE METHODS """
    @staticmethod
    def init_config():
        data = {
            "network": {
                "profiles": [],
                "config": {
                    "retries": 2,
                    "timeout": 30
                }
            },
            "screen": [],
            "cache": {
                "image": [],
                "video": []
            }
        }
        
        return data

    def load_config(self):
        self.config:dict = None

        dirname = os.path.dirname(CONFIG_FILE)
        if not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=False)

        if not os.path.exists(CONFIG_FILE):
            data = self.init_config()
        else:
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(repr(e))
        
        self.config = data
        pass
    
    def save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(repr(e))
        pass

    """ SETTINGS METHODS """
    @staticmethod
    def generate_unique_id():
        return str(uuid.uuid4())
    
    @staticmethod
    def fetch_screens_list():
        return []
    
    @staticmethod
    def gradient_color(value, min_value, max_value):
        """
        Returnează o culoare între verde -> galben -> roșu
        """
        # Normalizare între 0 și 1
        ratio = (value - min_value) / (max_value - min_value)
        ratio = max(0, min(ratio, 1))

        if ratio < 0.5:
            # verde -> galben
            # verde = (0,255,0), galben = (255,255,0)
            local_ratio = ratio / 0.5
            red = int(255 * local_ratio)
            green = 255
            blue = 0
        else:
            # galben -> roșu
            # galben = (255,255,0), roșu = (255,0,0)
            local_ratio = (ratio - 0.5) / 0.5
            red = 255
            green = int(255 * (1 - local_ratio))
            blue = 0

        return f"#{red:02x}{green:02x}{blue:02x}"
    
    """ Custom UI """
    def show_toast(self, flag:str, message:str, duration:int=3):
        toast = Toast(self, message, flag, duration*1000)
        toast.show()
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())
