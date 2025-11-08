#!./.venv/bin/python

import json
import os
import sys
import uuid

from PySide6.QtCore import QUrl, Slot, QTimer
from PySide6.QtGui import QKeyEvent, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidgetItem, QHBoxLayout, QLabel

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

    def __init__(self, parent, message, flag_color="#ff0000", duration=3000):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setStyleSheet("QWidget { background-color: white; border-radius: 5px; }")

        self.last_toast:Toast = None
        self.active = True

        if len(parent.toasts):
            self.last_toast = parent.toasts[-1]
            if not self.last_toast.active:
                self.last_toast = None

        # Layout principal
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        
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
        
        # Poziționare în colțul dreapta-sus al parent
        self.move_to_top_right()
        
        # Timer pentru auto-close
        QTimer.singleShot(duration, self.close_toast)
    
    def move_to_top_right(self):
        if self.last_toast is None:
            parent_geom = self.parent().geometry()
            x = parent_geom.x() + parent_geom.width() - self.width() - 20  # 20px padding
            y = parent_geom.y() + 20  # 20px de sus
        else:
            parent_geom = self.parent().geometry()
            x = parent_geom.x() + parent_geom.width() - self.width() - 20  # 20px padding
            y = parent_geom.y() + 10 + self.last_toast.height() + 20

        self.move(x, y)
        pass

    def close_toast(self):
        self.close()
        self.active = False
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
        # self.ui.tableWidget_gbox_network.customContextMenuRequested.connect(self.customContextMenu_tableWidget_gbox_network)

        # --- Settings - Screen ---
        # self.ui.tableWidget_gbox_screen.customContextMenuRequested.connect(self.customContextMenu_gbox_screen)

        # --- Settings - Cache ---

        # Vars
        self.config:dict = None
        self.toasts:list[Toast] = []

        # Load
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_webview)

        self.load_config()
        self.connect_page()
        # self.open_child_widget()
        pass

    """ CONTROL APP """
    def connect_page(self):
        network = self.config.get("network", None)

        missconfigured = False
        if network is None:
            missconfigured = True

        elif not len(network.get("profiles", [])):
            missconfigured = True

        # Setăm URL-ul pe care vrem să-l accesăm
        # self.ui.webEngineView.setUrl(QUrl("http://127.0.0.1:8080/"))

        if missconfigured:
            file_path = os.path.join(HTML_FILE, "default.html")

            if not os.path.exists(file_path):
                self.ui.webEngineView.setHtml("<h1>Please reinstall the app!</h1>")
                return

            self.ui.webEngineView.setUrl(QUrl.fromLocalFile(file_path))
        pass

    # def open_child_widget(self):
    #     # Cream widget-ul copil, dar nu-l afișăm încă
    #     self.child_widget = QWidget(self)
    #     self.child_widget.setAttribute(Qt.WA_StyledBackground, True)
    #     self.child_widget.setStyleSheet("background-color: white;")  # fundal curat
    #     self.child_widget.setGeometry(100, 100, 600, 400)  # poziție și dimensiune
    #     self.child_widget.hide()

    #     # Layout cu WebView în widget-ul copil
    #     layout = QVBoxLayout()
    #     self.web = QWebEngineView()
    #     self.web.setUrl(QUrl("https://www.wikipedia.org"))
    #     layout.addWidget(self.web)
    #     self.child_widget.setLayout(layout)

    #     self.child_widget.show()
    #     self.child_widget.raise_() 
    #     pass

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

        # --- Network ---
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
    def clicked_pushButton_settings_close(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_webview)
        pass

    """ PAGE - Settings - GBOX [Network] """
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
        pass

    @Slot()
    def changed_spinBox_gbox_network_config_reconnect_retries(self, value:int=None):
        value = self.ui.spinBox_gbox_network_config_reconnect_retries.value()
        xmin = self.ui.spinBox_gbox_network_config_reconnect_retries.minimum()
        xmax = self.ui.spinBox_gbox_network_config_reconnect_retries.maximum()

        hexcol = self.gradient_color(value, xmin, xmax)
        
        self.ui.label_gbox_network_color_reconnect_retries.setStyleSheet("QLabel { background-color: %s; }" % hexcol)
        pass

    @Slot()
    def changed_spinBox_gbox_network_config_timeout(self, value:int=None):
        value = self.ui.spinBox_gbox_network_config_timeout.value()
        xmin = self.ui.spinBox_gbox_network_config_timeout.minimum()
        xmax = self.ui.spinBox_gbox_network_config_timeout.maximum()

        hexcol = self.gradient_color(value, xmin, xmax)

        self.ui.label_gbox_network_color_timeout.setStyleSheet("QLabel { background-color: %s; }" % hexcol)
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
        self.toasts.append(Toast(self, message, flag, duration*1000))
        self.toasts[-1].show()
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec())
