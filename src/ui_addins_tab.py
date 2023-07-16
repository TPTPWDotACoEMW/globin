from .ui.addins_tab import Ui_AddinsTab

from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QSortFilterProxyModel
from globin import gather_addin_infos, add_addin, move_addin
import os

class AddinsTableModel(QAbstractTableModel):
    def __init__(self):
        super(AddinsTableModel, self).__init__()

        self.column_names = \
        [
            "Addin Name",
            "Type",
            "Version",
            "Author",
            "Enabled"
        ]

        self.addins_dir     = os.path.join(os.getcwd(), "addins")
        self.not_in_use_dir = os.path.join(os.getcwd(), "not-in-use")

        enabled_addins_list  = gather_addin_infos(self.addins_dir)
        disabled_addins_list = gather_addin_infos(self.not_in_use_dir)

        self.addin_infos = enabled_addins_list + disabled_addins_list
        self.enabled_addins = set([addin.folder_name for addin in enabled_addins_list])
        self.disabled_addins = set([addin.folder_name for addin in disabled_addins_list])

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if self.column_names[index.column()] == "Addin Name":
                return str(self.addin_infos[index.row()].name)
            
            elif self.column_names[index.column()] == "Type":
                addin_type = str(self.addin_infos[index.row()].type)
                if len(addin_type) > 0:
                    addin_type = addin_type[0].upper() + addin_type[1:] #"level" -> "Level", "mod" -> "Mod"
                return addin_type
            
            elif self.column_names[index.column()] == "Version":
                return str(self.addin_infos[index.row()].version)
            
            elif self.column_names[index.column()] == "Author":
                return str(self.addin_infos[index.row()].author)
        
        elif role == Qt.ItemDataRole.CheckStateRole and self.column_names[index.column()] == "Enabled":
            addin_folder_name = str(self.addin_infos[index.row()].folder_name)

            if addin_folder_name in self.enabled_addins:
                return Qt.CheckState.Checked
            else:
                return Qt.CheckState.Unchecked
        
    def setData(self, index, value, role):
        if self.column_names[index.column()] == "Enabled" and role == Qt.ItemDataRole.CheckStateRole:
            addin_folder_name = str(self.addin_infos[index.row()].folder_name)

            if Qt.CheckState(value) == Qt.CheckState.Unchecked:
                move_addin(addin_folder_name, "addins", "not-in-use")
                self.enabled_addins.remove(addin_folder_name)
                self.disabled_addins.add(addin_folder_name)

            elif Qt.CheckState(value) == Qt.CheckState.Checked:
                move_addin(addin_folder_name, "not-in-use", "addins")
                self.disabled_addins.remove(addin_folder_name)
                self.enabled_addins.add(addin_folder_name)

            self.dataChanged.emit(QModelIndex(), QModelIndex(), [])
            return True
        
        else:
            return super().setData(index, value, role)

    def flags(self, index):
        item_flags = super().flags(index)
        if self.column_names[index.column()] == "Enabled":
            item_flags |= Qt.ItemFlag.ItemIsUserCheckable
            item_flags &= ~Qt.ItemFlag.ItemIsAutoTristate

        return item_flags
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.column_names[section]

        return super().headerData(section, orientation, role)

    def columnCount(self, parent_index):
        return len(self.column_names)

    def rowCount(self, parent_index):
        return len(self.addin_infos)
    
    def add_enabled_item(self, addin_info):
        self.beginInsertRows(QModelIndex(), len(self.addin_infos), len(self.addin_infos))
        self.addin_infos.append(addin_info)
        self.enabled_addins.add(addin_info.folder_name)
        self.endInsertRows()

class AddinsTab(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.ui = Ui_AddinsTab()
        self.ui.setupUi(self)

        self.table_model = AddinsTableModel()
        self.table_proxy_model = QSortFilterProxyModel()

        self.table_proxy_model.setSourceModel(self.table_model)
        self.ui.tableViewAddins.setModel(self.table_proxy_model)

        self.ui.buttonInstallNewAddin.clicked.connect(self.add_addin_with_file_dialog)

    def add_addin_with_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Addin files (*.goomod)")

        try:
            if file_dialog.exec():
                addin_filenames = file_dialog.selectedFiles()
                for addin_filename in addin_filenames:
                    addin_info = add_addin(addin_filename)
                    
                    if addin_info is None:
                        QMessageBox.warning(None, "Incorrect addin file", "Please provide a valid addin file!")

                    elif(len(addin_info.name) != 0):
                        self.table_model.add_enabled_item(addin_info)

        except FileExistsError as e:
            QMessageBox.warning(None, "Addin already exists", e.strerror)