from PyQt6.QtCore import QEvent
from .ui.profile_tab import Ui_ProfileTab

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel, pyqtSignal
from .profile import ProfileCollection
from globin import read_directory_from_file, is_valid_game_directory

class LevelsTableModel(QAbstractTableModel):
    def __init__(self, profile_info):
        super(LevelsTableModel, self).__init__()

        self.column_names = \
        [
            "Level",
            "Most Balls",
            "Least Moves",
            "Least Time"
        ]

        self.profile_level_resutls = profile_info.level_results

        self.sort_role = Qt.ItemDataRole.UserRole

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if self.column_names[index.column()] == "Level":
                return str(self.profile_level_resutls[index.row()].level_id)
            
            elif self.column_names[index.column()] == "Most Balls":
                return str(self.profile_level_resutls[index.row()].most_balls)
            
            elif self.column_names[index.column()] == "Least Moves":
                return str(self.profile_level_resutls[index.row()].least_moves)
            
            elif self.column_names[index.column()] == "Least Time":
                return str(self.profile_level_resutls[index.row()].least_time)
            
        #Sort numbers instead of strings
        elif role == self.sort_role:
            if self.column_names[index.column()] == "Level":
                return str(self.profile_level_resutls[index.row()].level_id)
            
            elif self.column_names[index.column()] == "Most Balls":
                return self.profile_level_resutls[index.row()].most_balls
            
            elif self.column_names[index.column()] == "Least Moves":
                return self.profile_level_resutls[index.row()].least_moves
            
            elif self.column_names[index.column()] == "Least Time":
                return self.profile_level_resutls[index.row()].least_time
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.column_names[section]

        return super().headerData(section, orientation, role)

    def columnCount(self, parent_index):
        return len(self.column_names)

    def rowCount(self, parent_index):
        return len(self.profile_level_resutls)

class ProfileTab(QWidget):
    configure_world_of_goo_directory_requested = pyqtSignal()

    def __init__(self):
        super(QWidget, self).__init__()

        self.ui = Ui_ProfileTab()
        self.ui.setupUi(self)

        self.level_results_model = None
        self.ui.comboBoxProfiles.activated.connect(self.on_profile_changed)

        self.selected_profile = None
        self.load_profiles()

    def load_profiles(self):
        self.profile_collection = ProfileCollection()

        profile_index = 0
        while True:
            profile = self.profile_collection.get_profile_by_index(profile_index)
            
            if profile is None:
                break

            self.ui.comboBoxProfiles.addItem(profile.name)
            profile_index += 1

        if self.ui.comboBoxProfiles.count() > 0:
            self.ui.comboBoxProfiles.show()
            self.ui.comboBoxProfiles.setCurrentText(self.profile_collection.get_current_profile().name)
            self.on_profile_changed()

        else:
            self.ui.comboBoxProfiles.hide()
            self.ui.stackedWidgetProfiles.setCurrentWidget(self.ui.pageNoProfileFound)

    def on_profile_changed(self):
        self.selected_profile = self.profile_collection.get_profile_by_index(self.ui.comboBoxProfiles.currentIndex())
        self.show_selected_profile()

    def show_selected_profile(self):
        if self.selected_profile is None:
            self.ui.stackedWidgetProfiles.setCurrentWidget(self.ui.pageNoProfileFound)

        else:
            self.ui.comboBoxProfiles.setCurrentText(self.selected_profile.name)
            self.ui.stackedWidgetProfiles.setCurrentWidget(self.ui.pageProfileInfo)

            self.ui.labelProfileNameValue.setText(str(self.selected_profile.name))
            self.ui.labelPlayTimeValue.setText(ProfileTab.format_time(self.selected_profile.play_time))
            self.ui.labelLevelsPlayedValue.setText(str(len(self.selected_profile.level_results)))
            self.ui.labelFlagsValue.setText(ProfileTab.format_flags(self.selected_profile.flags))

            self.ui.labelHeightValue.setText("{:.3f} meters".format(self.selected_profile.tower.tower_height))
            self.ui.labelBallsValue.setText(str(self.selected_profile.tower.used_node_balls + self.selected_profile.tower.used_strand_balls) + " of " + str(self.selected_profile.tower.total_balls))
            self.ui.labelNodeBallsValue.setText(str(self.selected_profile.tower.used_node_balls))
            self.ui.labelStrandBallsValue.setText(str(self.selected_profile.tower.used_strand_balls))
            self.level_results_model = LevelsTableModel(self.selected_profile)
            self.table_proxy_model = QSortFilterProxyModel()

            self.table_proxy_model.setSourceModel(self.level_results_model)
            self.table_proxy_model.setSortRole(self.level_results_model.sort_role)

            self.ui.tableLevelsInfo.setModel(self.table_proxy_model)

    def format_time(secs):
        result = ""

        days = secs // 86400
        if days > 0:
            result += str(days)
            
            result += " day"
            if days != 1: 
                result += "s"

            result += ", "
            secs %= 86400

        hours = secs // 3600
        if days > 0 or hours > 0:
            result += str(hours)
            
            result += " hour"
            if hours != 1: 
                result += "s"

            result += ", "
            secs %= 3600

        minutes = secs // 60
        if days > 0 or hours > 0 or minutes > 0:
            result += str(minutes)
            
            result += " minute"
            if minutes != 1: 
                result += "s"

            result += ", "
            secs %= 60

        result += str(secs)
        
        result += " second"
        if secs != 1: 
            result += "s"

        return result
    
    def format_flags(flags):
        result = ""

        flag_online            = 0x01
        flag_goocorp_unlocked  = 0x02
        flag_goocorp_destroyed = 0x04
        flag_whistle           = 0x08
        flag_terms             = 0x10
        flag_32                = 0x20
        flag_64                = 0x40
        flag_128               = 0x80

        if flags & flag_online:
            result += "Online Enabled.\n"

        if flags & flag_goocorp_unlocked:
            result += "GooCorp Unlocked.\n"

        if flags & flag_goocorp_destroyed:
            result += "GooCorp Destroyed.\n"

        if flags & flag_whistle:
            result += "Whistle Found.\n"

        if flags & flag_terms:
            result += "Terms Accepted.\n"

        if flags & flag_32:
            result += "Flag32.\n"

        if flags & flag_64:
            result += "Flag64.\n"

        if flags & flag_128:
            result += "Flag128.\n"

        return result
