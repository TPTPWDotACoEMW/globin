from .ui.options_tab import Ui_OptionsTab

from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox
from globin import read_directory_from_file, is_valid_steam_directory, is_valid_game_directory

class OptionsTab(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.ui = Ui_OptionsTab()
        self.ui.setupUi(self)

        self.ui.buttonBrowseWorldOfGooInstallation.clicked.connect(self.browse_world_of_goo_directory)
        self.ui.buttonBrowseSteamDirectory.clicked.connect(self.browse_steam_directory)

        self.ui.lineEditWorldOfGooInstallation.setText(read_directory_from_file("wog_directory.txt"))
        self.ui.lineEditSteamDirectory.setText(read_directory_from_file("steam_directory.txt"))

    def browse_steam_directory(self):
        new_steam_directory = QFileDialog.getExistingDirectory(self, "Choose Steam directory", self.ui.lineEditSteamDirectory.text())
         
        if len(new_steam_directory) == 0:
            return

        if not is_valid_steam_directory(new_steam_directory):
            QMessageBox.warning(None, "Invalid directory", "Not a valid steam directory")
            return

        self.ui.lineEditSteamDirectory.setText(new_steam_directory)

        with open("steam_directory.txt", "w") as steam_dir_file:
            steam_dir_file.write(new_steam_directory)
            steam_dir_file.close()

    def browse_world_of_goo_directory(self):
        new_wog_directory = QFileDialog.getExistingDirectory(self, "Choose World of Goo directory", self.ui.lineEditWorldOfGooInstallation.text())
         
        if len(new_wog_directory) == 0:
            return

        if not is_valid_game_directory(new_wog_directory):
            QMessageBox.warning(None, "Invalid directory", "Not a valid World of Goo directory. Perhaps you are trying to select an old version of World of Goo, or a demo version.")
            return

        self.ui.lineEditWorldOfGooInstallation.setText(new_wog_directory)

        with open("wog_directory.txt", "w") as wog_dir_file:
            wog_dir_file.write(new_wog_directory)
            wog_dir_file.close()