import os
import platform
from dataclasses import dataclass

def get_profile_filename():
    profile_folder = ""

    if platform.system() == "Windows":
        profile_base_folder = os.getenv('LOCALAPPDATA')
        profile_folder = os.path.join(profile_base_folder, "2DBoy/WorldOfGoo")

    elif platform.system() == "Linux":
        profile_base_folder = os.getenv('HOME')
        profile_folder = os.path.join(profile_base_folder, ".WorldOfGoo")

    elif platform.system() == "Darwin":
        profile_base_folder = os.getenv('HOME')
        profile_folder = os.path.join(profile_base_folder, "Library/Application Support/WorldOfGoo")

    return os.path.join(profile_folder, "pers3.dat")

@dataclass
class LevelResult:
    level_id:    str
    most_balls:  int
    least_moves: int
    least_time:  int

class Profile:
    def __init__(self, profile_string):
        profile_tokens = profile_string.split(",")

        try:
            token_index = 0

            self.name = profile_tokens[token_index]
            token_index += 1

            self.flags = int(profile_tokens[token_index])
            token_index += 1

            self.play_time = int(profile_tokens[token_index])
            token_index += 1

            level_count = int(profile_tokens[token_index])
            token_index += 1

            self.level_results = []
            for i in range(0, level_count):
                level_id = profile_tokens[token_index]
                token_index += 1

                most_balls  = int(profile_tokens[token_index])
                token_index += 1

                least_moves = int(profile_tokens[token_index])
                token_index += 1

                least_time  = int(profile_tokens[token_index])
                token_index += 1

                self.level_results.append(LevelResult(level_id, most_balls, least_moves, least_time))

            skipped_level_count = int(profile_tokens[token_index])
            token_index += 1

            self.skipped_level_ids = []
            for i in range(0, skipped_level_count):
                skipped_level_id = profile_tokens[token_index]
                token_index     += 1

                self.skipped_level_ids.append(skipped_level_id)

            #Skip tower for now
            _tower_str = profile_tokens[token_index]
            token_index += 1

            self.online_id = profile_tokens[token_index][1:]
            token_index += 1

            self.new_balls = profile_tokens[token_index]
            token_index += 1

        except IndexError:
            pass
        

class ProfileCollection:
    mrpp_key = "mrpp"

    def __init__(self):
        self.profiles_data = {}

        profiles_filename = get_profile_filename()
        if os.path.isfile(profiles_filename):
            self.read_profile_collection_data(profiles_filename)

    def get_current_profile(self):
        curr_profile_key = "profile_" + self.profiles_data[ProfileCollection.mrpp_key]
        return self.profiles_data[curr_profile_key]

    def get_profile_by_index(self, profile_index):
        profile_key = "profile_" + str(profile_index)

        if profile_key in self.profiles_data:
            return self.profiles_data[profile_key]
        else:
            return None

    def read_profile_collection_data(self, profile_filename):
        profile_collection_file = open(profile_filename, "rb")

        key = self.read_next_element(profile_collection_file)
        while key is not None:
            value = self.read_next_element(profile_collection_file)

            if key == ProfileCollection.mrpp_key:
                self.profiles_data[key] = value
            else:
                self.profiles_data[key] = Profile(value)

            key = self.read_next_element(profile_collection_file)

        profile_collection_file.close()

    def read_next_element(self, profile_collection_file):
        length = 0
        sanity = 0 #From original Gootool code: prevents eternal loop reading non-profile data

        ch = profile_collection_file.read(1)
        while ch != b',':
            if ch == b'':
                return None

            length = (length * 10) + ord(ch) - ord('0')
            
            sanity = sanity + 1
            if sanity > 5:
                raise IOError("Insane profile data")
            
            ch = profile_collection_file.read(1)
            
        if length == 0:
            return None
        
        buf = profile_collection_file.read(length)
        if len(buf) < length:
            raise IOError("Invalid profile data")
        
        return str(buf, encoding="utf-8")