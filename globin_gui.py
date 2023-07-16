from src.ui_mainwindow import GlobinMainWindow
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = GlobinMainWindow()
    main_window.show()

    app.exec()