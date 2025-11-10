#!./.venv/bin/python

import json
import os
import sys
import time
import uuid

import requests
import socketio
from PySide6.QtCore import (QEasingCurve, QPoint, QPropertyAnimation, QSize, QThread, Signal, QObject,
                            QTimer, QUrl, Slot)
from PySide6.QtGui import QAction, QIcon, QKeyEvent, QPixmap, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QGraphicsOpacityEffect,
                               QHBoxLayout, QLabel, QMainWindow, QMenu,
                               QSpinBox, QTableWidgetItem, QVBoxLayout,
                               QWidget)

import resources_rc
from ui.ui_MainWindow import Ui_MainWindow

sio = socketio.Client()

is_frozen = getattr(sys, 'frozen', False)

WORK_PATH = "./_internal/local" if is_frozen else "./local"
WORK_PATH = os.path.abspath(WORK_PATH)

if not os.path.exists(WORK_PATH):
    os.makedirs(WORK_PATH, exist_ok=False)

CONFIG_FILE = os.path.join(WORK_PATH, "config/config.json")
CACHE_FOLDER = os.path.join(WORK_PATH, "cache")
HTML_FILE = os.path.join(WORK_PATH, "html")

# --- SocketIO ---
@sio.on("connect")
def socket_connect():
    print('[SIO] Connected!')
    sio.emit("client_message", {"text": "hello world!"})
    pass

@sio.on("disconnect")
def socket_disconnect():
    print("[SIO] Disconnected!")
    pass

@sio.on("server_message")
def socket_server_message(data):
    print("[SIO/Server] MSG: ", data['text'])
    pass


# --- QThread ---
class SocketWorker(QObject):
    connected = Signal()
    disconnected = Signal()
    commandReceived = Signal(dict)
    statusUpdate = Signal(str)

    def __init__(self):
        super().__init__()
        self.server_url = None
        self.client_id = None
        self.screens = []
        self.location = None
        self._running = False

        self.sio = socketio.Client(reconnection=False)

        @self.sio.on('connect')
        def on_connect():
            self.statusUpdate.emit(f"Connected to {self.server_url}")
            self.connected.emit()

            if self.client_id:
                self.sio.emit('register', {'id': self.client_id, "location": self.location, "screens": self.screens})
            pass

        @self.sio.on('disconnect')
        def on_disconnect():
            self.statusUpdate.emit("Disconnected from server.")
            self.disconnected.emit()

        @self.sio.on('server_command')
        def on_command(data):
            self.commandReceived.emit(data)

    def run(self):
        self._running = True
        while self._running:
            try:
                if not self.server_url:
                    time.sleep(3)
                    continue

                if not self.sio.connected:
                    self.sio.connect(self.server_url, wait_timeout=10)

                self.sio.wait()
            except Exception as e:
                self.statusUpdate.emit(f"Connection error: {e}")
                time.sleep(5)

    @Slot(dict)
    def connect_to_server(self, data:dict):
        self.server_url = data['url']
        self.client_id = data['id']
        self.location = data['location']
        self.screens = data.get('screens', [])
        pass

    @Slot(str)
    def send_status(self, msg):
        if self.sio.connected:
            self.sio.emit('client_status', {'id': self.client_id, 'msg': msg})
        else:
            self.statusUpdate.emit("Cannot send status: not connected!")
        pass

    def stop(self):
        self._running = False

        try:
            if self.sio.connected:
                self.sio.disconnect()
        except Exception:
            pass

        self.statusUpdate.emit("Socket worker stopped.")
        pass

# --- UI ---
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
        
        # --- Settings - App ---
        self.ui.pushButton_gbox_app_toggle.clicked.connect(self.toggle_gbox_app)

        # --- Settings - Network ---
        self.ui.pushButton_gbox_network_add.clicked.connect(self.clicked_pushButton_gbox_network_add)
        self.ui.pushButton_gbox_network_config_toggle.clicked.connect(self.toggle_gbox_network_config)
        self.ui.spinBox_gbox_network_config_reconnect_retries.valueChanged.connect(self.changed_spinBox_gbox_network_config_reconnect_retries)
        self.ui.spinBox_gbox_network_config_timeout.valueChanged.connect(self.changed_spinBox_gbox_network_config_timeout)
        self.ui.tableWidget_gbox_network.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableWidget_gbox_network.customContextMenuRequested.connect(self.customContextMenu_tableWidget_gbox_network)

        # --- Settings - Screen ---
        self.ui.tableWidget_gbox_screen.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableWidget_gbox_screen.customContextMenuRequested.connect(self.customContextMenu_gbox_screen)

        # --- Settings - Cache ---
        self.ui.pushButton_gbox_cache_image_toggle.clicked.connect(self.toggle_gbox_cache_image_toggle)
        self.ui.spinBox_gbox_cache_image_files_count.valueChanged.connect(self.changed_spinBox_gbox_cache_image_files_count)
        self.ui.spinBox_gbox_cache_image_max_size.valueChanged.connect(self.changed_spinBox_gbox_cache_image_max_size)
        self.ui.pushButton_gbox_cache_image_clear_cache.clicked.connect(self.clicked_pushButton_gbox_cache_image_clear_cache)

        self.ui.pushButton_gbox_cache_video_toggle.clicked.connect(self.toggle_gbox_cache_video_toggle)
        self.ui.spinBox_gbox_cache_video_files_count.valueChanged.connect(self.changed_spinBox_gbox_cache_video_files_count)
        self.ui.spinBox_gbox_cache_video_max_size.valueChanged.connect(self.changed_spinBox_gbox_cache_video_max_size)
        self.ui.pushButton_gbox_cache_video_clear_cache.clicked.connect(self.clicked_pushButton_gbox_cache_video_clear_cache)

        # Socket Control + Thread
        self.socket_thread = QThread()
        self.socket_worker = SocketWorker()
        self.socket_worker.moveToThread(self.socket_thread)

        self.socket_worker.connected.connect(lambda: print("Socket Connected!"))
        self.socket_worker.commandReceived.connect(self.processCommand)
        self.socket_worker.statusUpdate.connect(self.processStatus)
        self.socket_thread.started.connect(self.socket_worker.run)
        self.socket_thread.start()

        # Vars
        self.config:dict = None

        # Load
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_webview)

        QTimer.singleShot(1000, self.load_ui_icons_async)

        self.load_config()
        self.init_webView()

        QTimer.singleShot(5000, self.connect_socket)

        # Debug
        # self.clicked_pushButton_menu_settings()
        pass

    """ CONTROL APP """
    @Slot()
    def init_webView(self):
        file_path = os.path.join(HTML_FILE, "default.html")

        if not os.path.exists(file_path):
            self.ui.webEngineView.setHtml("<h1 style='text-align:center'>Please reinstall the app!</h1>")
            return
        
        self.ui.webEngineView.setUrl(QUrl.fromLocalFile(file_path))
        pass

    @Slot()
    def connect_socket(self, url:str=None):
        if url is None:
            network = self.config.get('network', None)
            if network is None:
                self.show_toast(Toast.Error, "Please config network profiles!")
                return

            profiles = network.get("profiles", [])
            if not profiles:
                self.show_toast(Toast.Error, "No profile was found!")
                return
            
            network_config = network.get("config", None)
            retries = network_config['retries'] if network_config else self.ui.spinBox_gbox_network_config_reconnect_retries.minimum()
            timeout = network_config['timeout'] if network_config else self.ui.spinBox_gbox_network_config_timeout.minimum()

            for net in profiles:
                tries = 0
                while tries < retries:
                    self.show_toast(Toast.Info, f"Connect to {net['name']}")

                    res = requests.get(net['host'], timeout=timeout)
                    if res.status_code == 200:
                        url = net['host']
                        break
                    else:
                        self.show_toast(Toast.Error, "Timeout... Try to reconnect!")

                    tries += 1

            if url is None:
                return

        data = {
            "id": self.config["app"]["device_uuid"],
            "url": url,
            "location": self.config['app']['location'],
            "screens": self.config['screen']
        }

        self.socket_worker.connect_to_server(data)
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

    def load_ui_icons_async(self):
        # --- PAGE - MENU ---
        self.ui.pushButton_menu_back.setIcon(QIcon(":/icons/icon-back.png"))
        self.ui.pushButton_menu_back.setIconSize(QSize(20, 20))
        
        self.ui.pushButton_menu_settings.setIcon(QIcon(":/icons/icon-gear.png"))
        self.ui.pushButton_menu_settings.setIconSize(QSize(20, 20))

        self.ui.pushButton_menu_close_app.setIcon(QIcon(":/icons/icon-close.png"))
        self.ui.pushButton_menu_close_app.setIconSize(QSize(20, 20))

        # --- PAGE - SETTINGS ---
        self.ui.pushButton_settings_close.setIcon(QIcon(":/icons/icon-close.png"))
        self.ui.pushButton_gbox_network_add.setIcon(QIcon(":/icons/icon-add.png"))
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

        self.populate_page_settings_gbox_app()
        self.populate_page_settings_gbox_network()
        self.populate_page_settings_gbox_screen()
        self.populate_page_settings_gbox_cache()
        pass

    @Slot()
    def clicked_pushButton_settings_close(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_webview)
        pass

    """ PAGE - Settings - GBOX [App] """
    def populate_page_settings_gbox_app(self):
        # LOAD
        config_app = self.config['app']

        self.ui.lineEdit_gbox_app_location.setText(config_app['location'])

        self.toggle_gbox_app(reset=True)
        pass

    @Slot()
    def toggle_gbox_app(self, reset=False):
        if not hasattr(self, "toggle_state_gbox_app"):
            self.toggle_state_gbox_app = True

        if reset:
            self.toggle_state_gbox_app = True
        
        icon = QIcon(":/icons/icon-pen.png") if self.toggle_state_gbox_app else QIcon(":/icons/icon-check.png")
        
        if self.toggle_state_gbox_app and not reset:
            value = self.ui.lineEdit_gbox_app_location.text().strip()
            
            if not value:
                self.show_toast(Toast.Error, "Please enter location!")
                return
            
            elif value != self.config['app']['location']:
                self.config['app']['location'] = value
                self.show_toast(Toast.Success, "Location updated!")
                self.save_config()
        
        self.toggle_state_gbox_app = not self.toggle_state_gbox_app

        self.ui.pushButton_gbox_app_toggle.setIcon(icon)
        self.ui.lineEdit_gbox_app_location.setEnabled(self.toggle_state_gbox_app)
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

        self.toggle_gbox_network_config(reset=True)
        pass
    
    @Slot()
    def toggle_gbox_network_config(self, reset=False):
        if not hasattr(self, "toggle_state_network_config"):
            self.toggle_state_network_config = True

        if reset:
            self.toggle_state_network_config = True
        
        icon = QIcon(":/icons/icon-pen.png") if self.toggle_state_network_config else QIcon(":/icons/icon-check.png")
        
        self.toggle_state_network_config = not self.toggle_state_network_config

        self.ui.pushButton_gbox_network_config_toggle.setIcon(icon)

        self.ui.spinBox_gbox_network_config_reconnect_retries.setEnabled(self.toggle_state_network_config)
        self.ui.spinBox_gbox_network_config_timeout.setEnabled(self.toggle_state_network_config)
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
        value = self.get_value_spinbox_and_color(
            self.ui.spinBox_gbox_network_config_reconnect_retries,
            self.ui.label_gbox_network_color_reconnect_retries
        )
        
        self.config['network']['config']['retries'] = value
        self.save_config()
        pass

    @Slot()
    def changed_spinBox_gbox_network_config_timeout(self, value:int=None):
        value = self.get_value_spinbox_and_color(
            self.ui.spinBox_gbox_network_config_timeout,
            self.ui.label_gbox_network_color_timeout
        )

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

            self.show_toast(Toast.Success, "Priority increased!")
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

            self.show_toast(Toast.Success, "Priority decreased!")
            pass

        def control_connect(item:QTableWidgetItem):
            profile_id = self.ui.tableWidget_gbox_network.item(item.row(), 0).data(Qt.DisplayRole)

            profiles = self.config['network']["profiles"]

            self.show_toast(Toast.Warning, "Connect to new Host!")

            for i, profile in enumerate(profiles):
                if profile['id'] == profile_id:
                    self.connect_socket(url=profile['host'])
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

            self.show_toast(Toast.Success, "Profile deleted!")
            pass

        global_pos = self.ui.tableWidget_gbox_network.viewport().mapToGlobal(pos)

        item = self.ui.tableWidget_gbox_network.itemAt(pos)
        if not item:
            return
        
        menu = QMenu(self)

        action_increase_priority = QAction("Priority (+)", self, icon=QIcon(":/icons/icon-arrow-up.png"))
        action_decrease_priority = QAction("Priority (-)", self, icon=QIcon(":/icons/icon-arrow-down.png"))
        action_connect = QAction("Connect", self, icon=QIcon(":/icons/icon-link.png"))
        action_delete = QAction("Delete", self, icon=QIcon(":/icons/icon-delete.png"))

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
                "profile": None
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
                "XY: ({}, {})".format(*scr['point']), scr['dpi'], scr['profile']
            ]

            for j, val in enumerate(xrow):
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, val)

                self.ui.tableWidget_gbox_screen.setItem(i,j, item)

        self.ui.tableWidget_gbox_screen.resizeColumnsToContents()
        pass

    @Slot()
    def customContextMenu_gbox_screen(self, pos: QPoint):
        def control_toggle_active_status(item:QTableWidgetItem):
            screen_id = self.ui.tableWidget_gbox_screen.item(item.row(), 0).data(Qt.DisplayRole)

            current_status = False
            for scr in screens:
                if scr['id'] == screen_id:
                    current_status = scr['active']

            active_screens = [x for x in screens if x['active'] and x['id'] != screen_id]
        
            if not active_screens and current_status:
                self.show_toast(Toast.Error, "The screen cannot be disabled. At least one screen must be active.")
                return
            
            for i, scr in enumerate(self.config['screen']):
                if scr['id'] == screen_id:
                    self.config['screen'][i]['active'] = not current_status

            self.save_config()
            self.populate_page_settings_gbox_screen()

            self.show_toast(Toast.Success, "Display status changed successful!")
            pass

        global_pos = self.ui.tableWidget_gbox_screen.viewport().mapToGlobal(pos)

        item = self.ui.tableWidget_gbox_screen.itemAt(pos)
        if not item:
            return
        
        screens = self.config['screen'].copy()
        screen_id = self.ui.tableWidget_gbox_screen.item(item.row(), 0).data(Qt.DisplayRole)

        current_status = False
        for scr in screens:
            if scr['id'] == screen_id:
                current_status = scr['active']

        menu = QMenu(self)

        action_toggle_active_status = QAction("Change Status", self, icon=QIcon(":/icons/icon-toggle-on.png") if current_status else QIcon(":/icons/icon-toggle-off.png"))

        menu.addAction(action_toggle_active_status)

        action_toggle_active_status.triggered.connect(lambda: control_toggle_active_status(item))

        menu.exec(global_pos)
        pass

    """ PAGE - Settings - GBOX [Cache] """
    def populate_page_settings_gbox_cache(self):
        # LOAD
        config_cache = self.config['cache']

        # -- image
        self.ui.spinBox_gbox_cache_image_files_count.setValue(config_cache['image']['max-files'])
        self.ui.spinBox_gbox_cache_image_max_size.setValue(config_cache['image']['max-size'])

        usage = self.calculate_disk_used(os.path.join(CACHE_FOLDER, "image"))
        self.ui.label_gbox_cache_image_cache_info.setText(usage)

        # -- video
        self.ui.spinBox_gbox_cache_video_files_count.setValue(config_cache['video']['max-files'])
        self.ui.spinBox_gbox_cache_video_max_size.setValue(config_cache['video']['max-size'])

        usage = self.calculate_disk_used(os.path.join(CACHE_FOLDER, "video"))
        self.ui.label_gbox_cache_video_cache_info.setText(usage)
        
        self.changed_spinBox_gbox_cache_image_files_count()
        self.changed_spinBox_gbox_cache_image_max_size()

        self.changed_spinBox_gbox_cache_video_files_count()
        self.changed_spinBox_gbox_cache_video_max_size()

        self.toggle_gbox_cache_image_toggle(reset=True)
        self.toggle_gbox_cache_video_toggle(reset=True)
        pass

    @Slot()
    def toggle_gbox_cache_image_toggle(self, reset=False):
        if not hasattr(self, "toggle_state_cache_image"):
            self.toggle_state_cache_image = True

        if reset:
            self.toggle_state_cache_image = True
        
        icon = QIcon(":/icons/icon-pen.png") if self.toggle_state_cache_image else QIcon(":/icons/icon-check.png")
        
        self.toggle_state_cache_image = not self.toggle_state_cache_image

        self.ui.pushButton_gbox_cache_image_toggle.setIcon(icon)

        self.ui.spinBox_gbox_cache_image_files_count.setEnabled(self.toggle_state_cache_image)
        self.ui.spinBox_gbox_cache_image_max_size.setEnabled(self.toggle_state_cache_image)
        pass

    @Slot()
    def changed_spinBox_gbox_cache_image_files_count(self, value:int=None):
        value = self.get_value_spinbox_and_color(
            self.ui.spinBox_gbox_cache_image_files_count, 
            self.ui.label_gbox_cache_image_color_files_count
        )

        self.config['cache']['image']['max-files'] = value
        self.save_config()
        pass

    @Slot()
    def changed_spinBox_gbox_cache_image_max_size(self, value:int=None):
        value = self.get_value_spinbox_and_color(
            self.ui.spinBox_gbox_cache_image_max_size, 
            self.ui.label_gbox_cache_image_color_max_size
        )

        self.config['cache']['image']['max-size'] = value
        self.save_config()
        pass

    @Slot()
    def clicked_pushButton_gbox_cache_image_clear_cache(self):
        self.clear_cache("image")
        self.populate_page_settings_gbox_cache()
        pass

    @Slot()
    def toggle_gbox_cache_video_toggle(self, reset=False):
        if not hasattr(self, "toggle_state_cache_video"):
            self.toggle_state_cache_video = True
        
        if reset:
            self.toggle_state_cache_video = True
        
        icon = QIcon(":/icons/icon-pen.png") if self.toggle_state_cache_video else QIcon(":/icons/icon-check.png")
        
        self.toggle_state_cache_video = not self.toggle_state_cache_video

        self.ui.pushButton_gbox_cache_video_toggle.setIcon(icon)

        self.ui.spinBox_gbox_cache_video_files_count.setEnabled(self.toggle_state_cache_video)
        self.ui.spinBox_gbox_cache_video_max_size.setEnabled(self.toggle_state_cache_video)
        pass

    @Slot()
    def changed_spinBox_gbox_cache_video_files_count(self, value:int=None):
        value = self.get_value_spinbox_and_color(
            self.ui.spinBox_gbox_cache_video_files_count, 
            self.ui.label_gbox_cache_video_color_files_count
        )

        self.config['cache']['video']['max-files'] = value
        self.save_config()
        pass

    @Slot()
    def changed_spinBox_gbox_cache_video_max_size(self, value:int=None):
        value = self.get_value_spinbox_and_color(
            self.ui.spinBox_gbox_cache_video_max_size, 
            self.ui.label_gbox_cache_video_color_max_size
        )

        self.config['cache']['video']['max-size'] = value
        self.save_config()
        pass

    @Slot()
    def clicked_pushButton_gbox_cache_video_clear_cache(self):
        self.clear_cache("video")
        self.populate_page_settings_gbox_cache()
        pass

    """ FILE METHODS """
    def init_config(self):
        data = {
            "app": {
                "location": "Store Wall",
                "device_uuid": self.generate_unique_id()
            },
            "network": {
                "profiles": [],
                "config": {
                    "retries": self.ui.spinBox_gbox_network_config_reconnect_retries.minimum(),
                    "timeout": self.ui.spinBox_gbox_network_config_timeout.minimum()
                }
            },
            "screen": [],
            "cache": {
                "image": {
                    "max-files": self.ui.spinBox_gbox_cache_image_files_count.minimum(),
                    "max-size": self.ui.spinBox_gbox_cache_image_max_size.minimum(),
                    "files": []
                },
                "video": {
                    "max-files": self.ui.spinBox_gbox_cache_video_files_count.minimum(),
                    "max-size": self.ui.spinBox_gbox_cache_video_max_size.minimum(),
                    "files": []
                }
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

    def clear_cache(self, source:str):
        path = os.path.join(CACHE_FOLDER, source)
        files = [os.path.join(path, x) for x in os.listdir(path)]

        deleted = []
        for f in files:
            try:
                os.remove(f)
                deleted.append(f)
            except Exception as e:
                print(repr(e))

        self.show_toast(Toast.Info, "Clear cache {}.<br>{} files deleted!".format(source, len(deleted)))
        pass

    """ SETTINGS METHODS """
    def get_value_spinbox_and_color(self, spinBox:QSpinBox, label:QLabel) -> int:
        value = spinBox.value()
        xmin = spinBox.minimum()
        xmax = spinBox.maximum()

        hexcol = self.gradient_color(value, xmin, xmax)
        label.setStyleSheet("QLabel { background-color: %s; }" % hexcol)

        return value

    @staticmethod
    def calculate_disk_used(path:str):
        files = []
        size = 0

        if not os.path.exists(path):
            os.makedirs(path, exist_ok=False)
        
        files = [os.path.join(path, x) for x in os.listdir(path)]
        size = sum([os.path.getsize(x) for x in files])/1024/1024
        
        return "<b>{} files</b> with a total size of <b>{:.2f} MB</b>  ".format(len(files), size)

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


    """ SOCKET + THREAD """
    @Slot(dict)
    def processCommand(self, data:dict):
        print(data)
        pass

    @Slot(str)
    def processStatus(self, msg:str):
        print("[SIO] Log:", msg)
        pass


    """ OVERRIDE """
    def closeEvent(self, event):
        self.socket_worker.stop()
        self.socket_thread.quit()
        self.socket_thread.wait()

        event.accept()
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())
