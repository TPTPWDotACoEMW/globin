from .ui.mainwindow import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import pyqtSignal
from globin import build_addins, launch_world_of_goo, read_directory_from_file
import platform

class GlobinMainWindow(QMainWindow):
    configure_world_of_goo_directory_requested = pyqtSignal()
    configure_steam_directory_requested = pyqtSignal()

    def __init__(self):
        super(GlobinMainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.buttonSave.clicked.connect(self.on_save_clicked)
        self.ui.buttonSaveAndLaunch.clicked.connect(self.on_save_and_launch_clicked)

        self.configure_world_of_goo_directory_requested.connect(self.ui.tabOptions.browse_world_of_goo_directory)
        self.configure_steam_directory_requested.connect(self.ui.tabOptions.browse_steam_directory)

    def on_save_clicked(self):
        self.build_and_launch(launch_after_build = False)

    def on_save_and_launch_clicked(self):
        self.build_and_launch(launch_after_build = True)

    def build_and_launch(self, launch_after_build):
        wog_dir = read_directory_from_file("wog_directory.txt")

        try:
            build_addins(wog_dir)

            if launch_after_build:
                launch_world_of_goo(wog_dir)

        except FileNotFoundError as e:
            if e.filename == "wog_dir":
                configure_wog_dir = QMessageBox.warning(None, "Directory not configured", "World of Goo directory is not configured. Configure it now?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if configure_wog_dir == QMessageBox.StandardButton.Yes:
                    self.configure_world_of_goo_directory_requested.emit()

            elif e.filename == "steam_dir":
                if platform.system() == "Windows":
                    configure_steam_dir = QMessageBox.warning(None,  "Directory not configured", "Steam directory is not configured. Configure it now?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if configure_steam_dir == QMessageBox.StandardButton.Yes:
                        self.configure_steam_directory_requested.emit()

                else:
                    QMessageBox.warning(None, "There was a problem launching Steam.", "Steam launch error")