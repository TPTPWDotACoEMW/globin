from bs4 import BeautifulSoup
from lxml import etree
from math import floor
import os
import platform
import shutil
import sys
import subprocess
import zipfile
import shutil
import errno
from collections import namedtuple

AddinInfo = namedtuple("AddinInfo", ["name", "author", "type", "version", "description", "folder_name"])

def main() :
    user_action         = ""
    user_action_choices = ["build", "run", "add", "enable", "disable", "list", "help"]

    if len(sys.argv) <= 1:
        user_action = "help"
    else:
        user_action = sys.argv[1]

    #Display the correct usage on unknown options
    if user_action not in user_action_choices:
        user_action = "help"

    if user_action == "build" or user_action == "run":
        print("Checking wog_directory.txt...\n")
        wog_dir = read_directory_from_file("wog_directory.txt")
        print(f"World of Goo directory set to {wog_dir}.")

        try:
            if build_addins(wog_dir) and user_action == "run":
                launch_world_of_goo(wog_dir)
        
        except FileNotFoundError as e:
            if e.filename == "wog_dir":
                print("ERROR: Files were not verified successfully. You may be using an old version of World of Goo,")
                print("or a demo version. Globin will not work with these versions. If you are using the latest version,")
                print("make sure you've specified the directory correctly.\n\nGlobin will now exit.")    

            elif e.filename == "steam_dir":
                if platform.system() == "Windows":
                    print("LAUNCH ERROR. It seems you are using Steam version of the game,")
                    print("but the Steam directory you have specified is not correct.")
                    print("Please provide the correct directory in steam_directory.txt.")
                
                else:
                    print("LAUNCH ERROR. It seems you are using Steam version of the game,")
                    print("but there was a problem launching Steam.")

    if user_action == "add":
        if len(sys.argv) <= 2 or not os.path.isfile(sys.argv[2]) or not sys.argv[2].endswith(".goomod"):
            print("Please provide a valid addin file!")
        else:
            new_addin = add_addin(sys.argv[2])
            if new_addin is None:
                print("Please provide a valid addin file!")

    if user_action == "enable" or user_action == "disable":
        if len(sys.argv) <= 2:
            print("Please provide the folder name of an installed addin!")

        elif user_action == "enable":
            move_addin(sys.argv[2], "not-in-use", "addins")

        elif user_action == "disable":
            move_addin(sys.argv[2], "addins", "not-in-use")

    if user_action == "list":
        addin_list_selected_option = "names"
        addin_list_option_choices = ["paths", "names", "all"]
        if len(sys.argv) >= 3 and sys.argv[2] in addin_list_option_choices:
            addin_list_selected_option = sys.argv[2]

        display_addin_list(addin_list_selected_option)

    if user_action == "help":
        display_help()

def display_help():
    print("--- Globin ver. 0.9.5 ---")
    print("A tool for installing mods for World of Goo 1.5\n")

    print("Usage:")
    print("python globin.py build:                   Installs the addins to the World Of Goo directory")
    print("python globin.py run:                     Installs the addins and launches World Of Goo")
    print("python globin.py list <names|paths|all>:  Displays the list of installed addins")
    print("python globin.py add <filename>:          Adds the addin to the list of installed addins")
    print("python globin.py enable <addin folder>:   Marks the addin as in-use")
    print("python globin.py disable <addin folder>:  Marks the addin as not-in-use")
    print("python globin.py help:                    Displays this message")

def display_addin_list(addin_list_selected_option):
    addins_dir     = os.path.join(os.getcwd(), "addins")
    not_in_use_dir = os.path.join(os.getcwd(), "not-in-use") 
    
    addin_infos            = gather_addin_infos(addins_dir)
    not_in_use_addin_infos = gather_addin_infos(not_in_use_dir)

    if len(addin_infos) == 0 and len(not_in_use_addin_infos) == 0:
        print("There are no addins installed.")
    else:
        if len(addin_infos) > 0:
            print("Installed addins:")

            for addin_info in addin_infos:
                if addin_list_selected_option == "paths":
                    print("- " + addin_info.folder_name)
                elif addin_list_selected_option == "names":
                    print("- " + addin_info.name)
                elif addin_list_selected_option == "all":
                    print("- [" + addin_info.folder_name + "] " + addin_info.name)

            print("")

        if len(not_in_use_addin_infos) > 0:
            print("Addins not in use:")

            for addin_info in not_in_use_addin_infos:
                if addin_list_selected_option == "paths":
                    print("- " + addin_info.folder_name)
                elif addin_list_selected_option == "names":
                    print("- " + addin_info.name)
                elif addin_list_selected_option == "all":
                    print("- [" + addin_info.folder_name + "] " + addin_info.name)

            print("")

def gather_addin_infos(addins_dir):
    addin_infos = []

    if os.path.isdir(addins_dir):
        addins_dir_contents = os.listdir(addins_dir)

        for addin_folder in addins_dir_contents:
            addin_infos.append(read_addin_info(addin_folder, addins_dir))

    return addin_infos

def read_addin_info(addin_folder, addin_parent_dir):
    addin_name        = ""
    addin_author      = ""
    addin_type        = ""
    addin_version     = ""
    addin_description = ""

    addin_xml_path = os.path.join(addin_parent_dir, addin_folder + "/addin.xml")
    if os.path.isfile(addin_xml_path):
        addin_info = open(addin_xml_path, "r", errors="ignore")
        addin_parser = BeautifulSoup(addin_info, "xml")

        addin_name_record = addin_parser.find("name")
        if addin_name_record is not None:
            addin_name = addin_name_record.contents[0]

        addin_author_record = addin_parser.find("author")
        if addin_author_record is not None:
            addin_author = addin_author_record.contents[0]

        addin_type_record = addin_parser.find("type")
        if addin_type_record is not None:
            addin_type = addin_type_record.contents[0]

        addin_version_record = addin_parser.find("version")
        if addin_version_record is not None:
            addin_version = addin_version_record.contents[0]

        addin_description_record = addin_parser.find("description")
        if addin_description_record is not None:
            addin_description = addin_description_record.contents[0]

        addin_info.close()

    return AddinInfo(name=addin_name, author=addin_author, type=addin_type, version=addin_version, description=addin_description, folder_name=addin_folder)

def add_addin(filename):
    addins_dir = os.path.join(os.getcwd(), "addins")
    not_in_use_dir = os.path.join(os.getcwd(), "not-in-use")
    if not os.path.isdir(addins_dir):
        os.mkdir(addins_dir)

    addin_name = os.path.splitext(os.path.basename(filename))[0]
    addin_dir = os.path.join(addins_dir, addin_name)
    not_in_use_addin_dir = os.path.join(not_in_use_dir, addin_name)

    if os.path.isdir(addin_dir) or os.path.isdir(not_in_use_addin_dir):
        raise FileExistsError("Addin already exists!")

    os.mkdir(addin_dir)

    try:
        with zipfile.ZipFile(filename, 'r') as addin_archive:
            addin_archive.extractall(addin_dir)

    except zipfile.BadZipFile:
        os.rmdir(addin_dir)
        return None

    return read_addin_info(addin_dir, addins_dir)

def move_addin(addin_name, dir_from, dir_to):
    path_from = os.path.join(os.getcwd(), dir_from)
    path_from = os.path.join(path_from, addin_name)

    path_to = os.path.join(os.getcwd(), dir_to)
    if not(os.path.isdir(path_to)):
        os.mkdir(path_to)
        
    path_to = os.path.join(dir_to, addin_name)

    if os.path.exists(path_to):
        return #Enabling an enabled addin or disabling a disabled addin is not considered an error
    
    if not os.path.exists(path_from):
        print("Please provide the folder name of an installed addin!")
        return

    shutil.move(path_from, path_to)

def is_valid_game_directory(wog_dir):
    verifier = os.path.join(wog_dir, "game/res/levels/island3/pipecon_03@2x.png")
    return os.path.isfile(verifier)

def build_addins(wog_dir):
    print("Starting...")
    print("Verifying game files...")

    if not is_valid_game_directory(wog_dir):
        raise FileNotFoundError(errno.ENOENT, "World of Goo directory not found, or contains an unsupported version of World of Goo", "wog_dir")

    else:
        print("Game files verified. Beginning installation...")
        addins_dir = os.path.join(os.getcwd(), "addins")
        game_folder = os.path.join(os.fspath(wog_dir), "game")
        print("Importing useful resources...\n")
        mergedir(os.getcwd(), "addin_rsc", game_folder)
        
        level_id_list = []
        for addin in os.listdir(addins_dir) :
            print(f"Copying {os.fsdecode(addin)}...")
            print("Editing file extensions...")
            addin_path = os.path.join(addins_dir, addin)
            levels_path = os.path.join(addin_path, "compile/res/levels")
            if os.path.isdir(levels_path) :
                snip_xml(levels_path)
            balls_path = os.path.join(addin_path, "compile/res/balls")
            if os.path.isdir(balls_path) :
                snip_xml(balls_path) # For those pesky balls with ".xml.xml" file extensions
                tack_xml(balls_path, ["balls", "resources"])
            islands_path = os.path.join(addin_path, "compile/res")
            if os.path.isdir(islands_path) :
                snip_xml(os.path.join(islands_path,"islands"))
                tack_xml(islands_path, ["island1","island2","island3","island4","island5"])
            
            print(f"Copying level contents to {os.fspath(game_folder)}...")
            mergedir(addin_path, "compile", game_folder)
            mergedir(addin_path, "override", game_folder)

            if os.path.isdir(os.path.join(addin_path, "merge")) :
                print("\"merge\" folder detected. Merging contents...")
                merge_dir = os.path.join(addin_path, "merge")
                for contents in os.listdir(merge_dir) :
                    xsl_copy(merge_dir, "", contents, game_folder)
                
            
            print("Parsing level information...")
            addin_info_path = os.path.join(addin_path, "addin.xml")
            addin_info = open(addin_info_path, "r", errors="ignore")
            addin_parser = BeautifulSoup(addin_info, "xml")
            text_info_path = os.path.join(addin_path, "text.xml")
            if os.path.isfile(text_info_path) :
                text_info = open(text_info_path, "r", errors="ignore")
                text_parser = BeautifulSoup(text_info, "xml")
            else :
                text_info = open(text_info_path, "x", errors="ignore")
                text_parser = BeautifulSoup("", "xml")
            

            text_path = os.path.join(game_folder, "properties/text.xml")
            text_file = open(text_path, "r+")
            text_soup = BeautifulSoup(text_file, "xml")

            island_path = os.path.join(game_folder, "res/islands/island1.xml")
            island_file = open(island_path, "r+")
            island_soup = BeautifulSoup(island_file, "xml")

            # Step 1: Parse out all the levels
            levels = addin_parser.find_all("level")
            for level in levels :
                # Step 2: Add the level's ID and OCD
                interpreter = BeautifulSoup(str(level), "xml")
                id = interpreter.find("dir").contents[0]
                ocd_list = interpreter.find("ocd").contents
                if len(ocd_list) == 0 :
                    add_to_island = f"<level id=\"{id}\" name=\"LEVEL_NAME_{id.upper()}\" text=\"LEVEL_TEXT_{id.upper()}\" />"
                else :
                    ocd = ocd_list[0]
                    add_to_island = f"<level id=\"{id}\" name=\"LEVEL_NAME_{id.upper()}\" text=\"LEVEL_TEXT_{id.upper()}\" ocd=\"{ocd}\" />"

                island_soup.island.append(BeautifulSoup(add_to_island, "xml"))

                # Step 3: Add level name and subtitle
                name_path = interpreter.find("name").get("text")
                name = name_path.replace("\"","&quot;")
                subtitle_path = interpreter.subtitle.get("text")
                subtitle = subtitle_path.replace("\"","&quot;")
                add_to_text = f"<string id=\"LEVEL_NAME_{id.upper()}\" text=\"{name}\" />"
                text_soup.find(name="strings").append(BeautifulSoup(add_to_text, "xml"))
                add_to_text = f"<string id=\"LEVEL_TEXT_{id.upper()}\" text=\"{subtitle}\" />"
                text_soup.find(name="strings").append(BeautifulSoup(add_to_text, "xml"))

                level_id_list.append(id)

            # Step 4: Add contents of text.xml, unchanged
            text = text_parser.find_all(name = "string")
            all_strings = ""
            for string in text :
                text_soup.find(name="strings").append(string)

            # Step 5: Write to text and island files
            text_file.seek(0)
            text_file.write(text_soup.prettify())
            text_file.truncate()
            text_file.close()
            
            island_file.seek(0)
            island_file.write(island_soup.prettify())
            island_file.truncate()
            island_file.close()
            addin_info.close()
            text_info.close()

            # Step 6: Merge contents of the merge folder. If the merge folder does not exist, skip this step.
            # The code for this step is not yet implemented.

            print("Addin installed successfully.\n")

        print("Placing level buttons...")

        buttons_path = os.path.join(game_folder, "res/levels/island1/island1.scene")
        buttons_file = open(buttons_path, "r+")
        buttons_soup = BeautifulSoup(buttons_file, "xml")
        buttons_soup.scene['maxy'] = max(float((1200 + (120 * floor(len(level_id_list) / 10)))), float(buttons_soup.scene.get("maxy")))
        buttons_soup.scene['backgroundcolor'] = "138,145,232"
        for i in range (len(level_id_list), 0, -1) :
            id = level_id_list[i - 1]
            multiplier = len(level_id_list) - (i)
            x = (-75 * (multiplier % 10))
            y = 900 + (120 * floor(multiplier / 10))
            ocd_y = y + 40
            buttons_soup.buttongroup.append(BeautifulSoup(f"<button id=\"lb_{id}\" depth=\"8\" x=\"{x}\" y=\"{y}\" scalex=\"1\" scaley=\"1\" rotation=\"0\" alpha=\"1\" colorize=\"255,255,255\" up=\"IMAGE_SCENE_ISLAND1_LEVELMARKERA_UP\" over=\"IMAGE_SCENE_ISLAND1_LEVELMARKERA_OVER\" onclick=\"pl_{id}\" onmouseenter=\"ss_{id}\" onmouseexit=\"hs_{id}\" />", "xml"))
            buttons_soup.find("scene").append(BeautifulSoup(f"<SceneLayer id=\"ocd_{id}\" name=\"OCD_flag1\" depth=\"7.2\" x=\"{x + 10}\" y=\"{ocd_y}\" scalex=\"1\" scaley=\"1\" rotation=\"0\" alpha=\"1\" colorize=\"255,255,255\" image=\"IMAGE_SCENE_ISLAND1_OCD_FLAG1\" anim=\"ocdFlagWave\" animspeed=\"1\"/>", "xml"))

        buttons_file.seek(0)
        buttons_file.write(buttons_soup.prettify())
        buttons_file.truncate()
        buttons_file.close()

        print("Cleaning up...")
        mergedir(os.getcwd(), "addin_cleanup", game_folder)

        print("All addins installed. Thank you for using Globin.\n")

        return True

def is_valid_steam_directory(steam_dir):
    steam_executable = ""
    
    if platform.system() == "Windows":
        steam_executable = os.path.join(steam_dir, "Steam.exe")
    elif platform.system() == "Linux":
        steam_executable = os.path.join(steam_dir, "steam")
    elif platform.system() == "Darwin":
        steam_executable = os.path.join(steam_dir, "steam_osx")

    return os.path.isfile(steam_executable)

def launch_world_of_goo(wog_dir):
    if platform.system() == "Windows":
        launch_world_of_goo_windows(wog_dir)
    
    if platform.system() == "Linux":
        launch_world_of_goo_linux(wog_dir)

    if platform.system() == "Darwin":
        launch_world_of_goo_macos(wog_dir)

def launch_world_of_goo_windows(wog_dir):
    is_steam_version = os.path.isfile(os.path.join(wog_dir, "steam_api.dll"))

    if is_steam_version:
        steam_path = read_directory_from_file("steam_directory.txt")
        steam_executable = os.path.join(steam_path, "Steam.exe")

        if not os.path.isfile(steam_executable):
            raise FileNotFoundError(errno.ENOENT, "Steam directory not found", "steam_dir")
        
        subprocess.Popen([steam_executable, "-applaunch", "22000"])
            
    else:
        #Apparently Epic Games version can also be launched directly from game .exe, starting the launcher if needed
        game_executable = os.path.join(os.fspath(wog_dir), "WorldOfGoo.exe")
        subprocess.Popen(game_executable)

def launch_world_of_goo_linux(wog_dir):
    is_steam_version = os.path.isfile(os.path.join(wog_dir, "lib/libsteam_api.so"))

    if is_steam_version:
        steam_command = "steam" #Steam on Linux can be launched with a single command
        subprocess.Popen([steam_command, "-applaunch", "22000"])
            
    else:
        game_executable = os.path.join(os.fspath(wog_dir), "WorldOfGoo.bin.x86_64")
        subprocess.Popen(game_executable)

def launch_world_of_goo_macos(wog_dir):
    is_steam_version = os.path.isfile(os.path.join(wog_dir, "../Frameworks/libsteam_api.dylib"))

    if is_steam_version:
        steam_executable = "/Applications/Steam.app/Contents/MacOS/steam_osx" #Apparently apps on Mac are always installed in /Applications?
        
        if not os.path.isfile(steam_executable):
            raise FileNotFoundError(errno.ENOENT, "Steam directory not found", "steam_dir")
        
        subprocess.Popen([steam_executable, "-applaunch", "22000"])
            
    else:
        game_executable = os.path.join(os.fspath(wog_dir), "../MacOS/World of Goo")
        subprocess.Popen(game_executable)

def read_directory_from_file(filename):
    read_directory = open(filename, "r")
    directory = read_directory.readline().strip()
    read_directory.close()

    return directory

def mergedir(home, target, game_folder) :
    content = os.path.join(home, target)
    if os.path.isdir(content) :
        shutil.copytree(content, game_folder, dirs_exist_ok = True)
    else :
        print(f"\"{target}\" not found in target folder. Skipping...")

def snip_xml(fil) :
    if os.path.isdir(fil) :
        for contents in os.listdir(fil) :
            snip_xml(os.path.join(fil, contents))
    elif os.path.isfile(fil) :
        if fil.endswith(".xml") :
            os.rename(fil,os.fsdecode(fil).replace(".xml","",1))

def tack_xml(fil, targets) :
    for contents in os.listdir(fil) :
        for name in targets :
            target = os.path.join(os.path.join(fil, contents), name)
            if os.path.isfile(target) :
                os.rename(target, (target + ".xml"))

def xsl_copy(merge_dir, current_path, target_file, game_folder) :
    next_path = os.path.join(current_path, target_file)
    full_path = os.path.join(merge_dir, next_path)
    if os.path.isdir(full_path) :
        for contents in os.listdir(full_path) :
            xsl_copy(merge_dir, next_path, contents, game_folder)
    elif os.path.isfile(full_path) :
        if full_path.endswith(".xsl") :
            parser = etree.XMLParser()
            xsl = open(full_path, "r")
            xsl_root = etree.parse(xsl, parser)


            target_in_game_files = target_file.replace(".xsl","")
            target_game_directory = os.path.join(os.path.join(game_folder, current_path), target_in_game_files)
            xml = open(target_game_directory, "r+")
            xml_target = etree.parse(xml, parser)

            transform = etree.XSLT(xsl_root)
            xml.seek(0)
            xml.write(str(transform(xml_target)))
            xml.truncate()
            xml.close()
            xsl.close()
        else :
            print(f"WARNING: File \"{target_file}\" was found in \"merge\" folder but is not a .xsl file. Globin does not merge non-xsl files - this addin may not have been installed properly.")

main()
