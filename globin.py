from bs4 import BeautifulSoup
from lxml import etree
from math import floor
import os
import platform
import shutil
import sys
import subprocess

def main() :
    user_action         = ""
    user_action_choices = ["build", "run", "help"]

    if len(sys.argv) <= 1:
        user_action = "run"
    else:
        user_action = sys.argv[1]

    #Display the correct usage on unknown options
    if user_action not in user_action_choices:
        user_action = "help"

    if user_action == "build" or user_action == "run":
        print("Checking wog_directory.txt...\n")
        wog_dir = read_directory_from_file("wog_directory.txt")
        print(f"World of Goo directory set to {wog_dir}.")

        if build_addins(wog_dir) and user_action == "run":
            launch_world_of_goo(wog_dir)

    if user_action == "help":
        display_help()

def display_help():
    print("--- Globin ver. 0.9 ---")
    print("A tool for installing mods for World of Goo 1.5\n")

    print("Usage:")
    print("python globin.py build: Installs the addins to the World Of Goo directory")
    print("python globin.py run:   Installs the addins and launches World Of Goo")
    print("python globin.py help:  Displays this message")

def build_addins(wog_dir):
    print("Starting...")
    print("Verifying game files...")
    verifier = os.path.join(wog_dir, "game/res/levels/island3/pipecon_03@2x.png")
    if os.path.isfile(verifier) :
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
    
    else :
        print("ERROR: Files were not verified successfully. You may be using an old version of World of Goo,")
        print("or a demo version. Globin will not work with these versions. If you are using the latest version,")
        print("make sure you've specified the directory correctly.\n\nGlobin will now exit.")

        return False

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

        if os.path.isfile(steam_executable):
            subprocess.Popen([steam_executable, "-applaunch", "22000"])

        else:
            print("LAUNCH ERROR. It seems you are using Steam version of the game,")
            print("but the Steam directory you have specified is not correct.")
            print("Please provide the correct directory in steam_directory.txt.")
            
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

        if os.path.isfile(steam_executable):
            subprocess.Popen([steam_executable, "-applaunch", "22000"])

        else:
            print("LAUNCH ERROR. It seems you are using Steam version of the game,")
            print("but there was a problem launching Steam.")
            
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
