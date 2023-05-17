  ▄███████▄                                      
 ███████████                                     ▄▀▀▀▄
███▀     ▀███   ███                 ███          █ ▀ █
███             ███                 ███           ▀▀▀
███             ███                 ███                 
███    ██████   ███    ▄███████▄    █████████▄    ███   █████████▄
███    ▀▀▀███   ███   ▄██▀   ▀██▄   ███▀   ▀██▄   ███   ███▀   ▀██▄
███       ███   ███   ███     ███   ███     ███   ███   ███     ███
███▄     ▄███   ███   ███     ███   ███     ███   ███   ███     ███
 ███████████    ███   ▀██▄   ▄██▀   ▀██▄   ▄██▀   ███   ███     ███
  ▀███████▀     ███    ▀███████▀     ▀███████▀    ███   ███     ███

--- A tool for installing mods for World of Goo 1.5 ---

~~~

### Table of Contents
- 1: What You Need To Know First
  -- 1.1: Current Constraints of Globin
  -- 1.2: Extra Notes for GitHub
- 2: Setting Up Globin
  -- 2.1: Setting Your World of Goo Directory
     --- 2.1.1: (Optional) Setting Your Steam Directory
  -- 2.2: Adding Addins
     --- 2.2.1: Unpacking .goomod Files Automatically
     --- 2.2.2: Unpacking .goomod Files Manually
  -- 2.3: Incompatible Addins
  -- 2.4: Dependencies
- 3: Using Globin
  -- 3.1: Running Globin From Command Line
  -- 3.2: Uninstalling Mods Installed With Globin
- 4: Playing With Your Addins
- 5: Reporting Bugs or Asking Questions
  -- 5.1: Known Problems

~~~

### 1: What You Need To Know First

Globin is a tool for installing mods created for GooTool on the latest version of World of Goo,
which GooTool is no longer compatible with. It uses the file hierarchy of .goomod files used for
GooTool so that there's no need to update already-made addins for the latest version.

If this is your first time using Globin, it is recommended to start with Section 2.4, which will
explain what you need to install before you start running Globin. Without the dependencies, Globin
will either throw errors or not run at all.

Globin will mess with your files and install directly to your chosen World of Goo directory. If
you are not playing on a version that can easily restore modified files, it is recommended you make
a backup of the game and/or the game's saves so your file with 100% OCDs is not lost when attempting
to restore the game to a modless state. More information on where your save file is located can be
found in Section 3.2.

Globin runs on many assumptions about how it is placed relative to the folders it uses, and how the
folders in your World of Goo directory are organized. If its folder systems are altered, it may
install addins improperly. This is highly unlikely to destroy your computer, or even do any lasting
damage at all, but if you want to avoid taking that risk the easiest way to avoid it is to leave
the folders in your installation of Globin alone unless this document explicitly instructs
modifying these folders' contents.

    ## 1.1: Current Constraints of Globin

    Globin is a new, incomplete software. For now, it does the bare minimum in terms of installing
    and playing addins. This means there will be a few constraints to how it can be used.

    With the way Globin is currently put together, it will place level buttons in the first chapter
    even when mods that replace it are active. This may cause added buttons to overlap with buttons
    native to that chapter. The only solution for this is to remove installed addins not part of that
    chapter until this no longer happens. Although this may change at a later point, there are not
    currently plans for such a change.

    Two of the most visible features in GooTool are the tower snapshot and the save-file record keeper.
    These both rely on reading the player's save file (pers2.dat in 1.3 and below) to show interesting
    information. For the time being, Globin is unable to replicate these features.

    In versions 1.5 and above, almost every image in the game has a 2x resolution version. The game
    scales the images with increased resolution according to their increased resolution, so in most
    cases addins do not need to be modified to compensate for upscaling. The only exception in this
    regard is if a level uses a pipe sprite outside of the levelpipe itself. The pipe sprites do
    not have lower-resolution counterparts, since the images for them are handled by the pipe and
    not the scene layers. As such, their sprites are twice the size of those in versions 1.3 and
    below and are not scaled accordingly. This has no effect on gameplay, but will cause these pipes
    to be twice the size, sometimes interfering with the visuals. For the same reason, level arrows
    that appear above incomplete levels will be half the size if overridden by a mod such as Lost
    in Paradise. It is not currently known if this applies to other sprites; if one is found, please
    send a bug report so we can list it here. For now, Globin does not fix this issue. It is unknown
    if it will eventually do so.

    Addins that override images will not show most overridden images if 2x resolution is enabled.
    As such, Globin disables 2x graphics by default. It can be re-enabled by modifying
    "properties/config.template.ini" in the "addin_rsc" folder.
    
    The cutscenes in the latest version of World of Goo use a different type of binary. This means
    that custom cutscenes will be skipped, and overriden cutscenes will crash the game. This is
    prevented by preserving the resources file of each vanilla cutscene. These cutscenes can still
    be modified by directly modifying the resources directly, however.
    
    ## 1.2: Extra Notes for GitHub
    
    GitHub does not support adding empty directories. This means the "addins" and "not-in-use" folder
    have to be added manually. This may also apply to a few other folders in the repository.

~~~

### 2: Setting Up Globin

Although Globin is almost entirely automatic, before it can run it requires some preliminary setup.
This section assumes you understand the basics of the following:

- Opening text files
- Editing text files
- Extracting contents of compressed folders
- Basic file operations (moving, copying, etc.)
- Reading and writing of filepaths
- Installation and use of Python3 and PIP

If you do not understand the basics of one of these, it will probably be best to search the internet
for a beginner's guide, which will explain far better than this section will be able to.

    ## 2.1: Setting Your World of Goo Directory

    In the Globin folder, there should be an empty file named "wog_directory.txt". If there is not one,
    you need to create one. Open this file and, on the first line, write the filepath from your current
    drive (e.g. C: or D:) to the folder where your copy of World of Goo is located.

    The program will probably run fine if you add additional lines. However, note that it will only read
    the VERY FIRST line, and it will read the ENTIRE line. Once you've written out the path, leave it
    alone.

        # 2.1.1: (Optional) Setting Your Steam Directory

        Globin is able to launch World of Goo with "run" command line argument. However, the Steam version 
        of World Of Goo will not start if you try to launch the executable directly. If you have the Steam
        version of the game and want to launch World of Goo after building the addins, provide the directory
        of Steam in "steam_directory.txt".

        The rules for specifying the Steam directory are the same as the rules for specifying World of Goo
        directory.

    ## 2.2: Adding Addins

    As mentioned in section 1, Globin operates using the organization system of .goomod files. However,
    Globin is unable to read these files while they are compressed. To make them readable to Globin, 
    they need to be extracted to the "addins" folder. There are two ways to do it: automatic and manual.
    
        # 2.2.1: Unpacking .goomod Files Automatically
    
        To automatically extract the contents of a .goomod file into the Globin folder, run the Globin 
        with "add" command line option. For example, to extract "C:\Users\Me\Documents\addin.goomod",
        execute the following command:
        - python3 globin.py add "C:\Users\Me\Documents\addin.goomod" 

        # 2.2.2: Unpacking .goomod Files Manually
    
        Extracting the contents of a .goomod file is required for Globin to read them. This is a fairly
        simple step, but caution must be taken to not skip it. To extract the contents of a .goomod file,
        first use the rename function to change the file's extension from .goomod to .zip. Some OSes will
        warn you that this can make the file unstable; proceed anwyays. Once the file's extension is
        changed, the .zip file can be opened as normal and extracted to the "addins" folder.

        Most file extraction software will do this properly, but if you want to check, make sure that the 
        addin's "addin.xml" is two folders down. For example, if your addin is named "addin_name", make sure 
        that "Globin/addins/addin_name/addin.xml" is a valid filepath. If the addin data (including "addin.xml") 
        is a layer too shallow or a layer too deep, Globin will not be able to install it properly.

    ## 2.3: Incompatible Addins

    Not all addins you install will be compatible with each other, and sometimes you may wish to remove 
    some addins. In cases where you wish to table an incompatible addin or one you just don't want anymore, 
    you can move that addin to the "not-in-use" folder. This folder is not read by Globin, it is simply
    there for ease of moving addins to and from the "addins" folder.

    ## 2.4: Dependencies

    Globin is a program that runs on Python3. As such, your system needs Python3 installed to run Globin.
    In addition, the program uses a Python library called "bs4" or "beautifulsoup4" to read and write
    XML files, as well as a Python library called "lxml" to interpret them. These libraries can be easily
    installed using "PIP Installs Python", a dedicated installer for Python3 libraries that comes bundled
    with the latest versions of Python3.

    Once Python3, beautifulsoup4, and lxml are installed, Globin can be run.

~~~

### 3: Using Globin

Running Globin is simple. This section assumes you understand the basics of the following:

- Use of the command line or an integrated development environment
- Copying and merging of files and folders
- Basic file operations for your launcher of choice (Steam, Epic Games, etc.) if any
- Use of Python3

If you do not understand the basics of one of these, it will probably be best to search the internet
for a beginner's guide, which will explain far better than this section will be able to.

    ## 3.1: Running Globin From Command Line

    The easiest way to run Globin is to use your computer's built-in command line terminal. To run
    Globin from the command line, navigate to the Globin directory and enter the command
    "python3 globin.py". This will automatically run Globin, installing all addins in the "addins"
    folder and placing a button in Chapter 1 for each installed level (except levels in full
    chapters). After that, Globin automatically launches World of Goo. If running Globin gives 
    an error, refer to section 5.

    Globin supports several command-line arguments:
    - "python3 globin.py add <filename>" adds a new addin to the "addins" folder;
    - "python3 globin.py run" is the default behavior, described above; 
    - "python3 globin.py build" installs all addins without launching World Of Goo;
    - "python3 globin.py help" displays the info message.

    Repeatedly using Globin will cause files with text appended to them (generally files in one or
    more "merge" folders) to build up with lots of text referencing the same object or objects.
    Generally, this is not going to cause any significant problems, but you may want to prevent
    it anyways. Globin automatically scrubs the two most important sources of buildup (island1.xml
    and island1.scene), as well as "text.xml" if the stripped-down version is moved to "addin-rsc".
    However, it does not currently do so for any other file. As such, you may want to consider
    uninstalling all mods (using the methods described in the next section) before using Globin
    multiple times.

    ## 3.2: Uninstalling Mods Installed With Globin

    Some mods will override the original contents of certain levels, change the design of certain
    Goo Balls, or occasionally remove entire chapters. Globin does not have a dedicated uninstall
    tool for removing these installed levels, so they must be uninstalled manually.
    
    If your install of World of Goo is based in Steam, you can return your game to its normal state
    by right-clicking it, opening "Properties", selecting "Local Files", and finally selecting
    "Verify integrity of game files." This will restore any modified files in the game's directory,
    but note that it will NOT remove any files that were added by Globin that DID NOT REPLACE a
    file that was already there. Those can be removed manually without worrying about accidentally
    deleting an important file; "Verify integrity of game files" will restore deleted filed from
    the original game.

    Although it is likely that Epic Games has a similar way to restore game files, it is unknown;
    the same applies to installations not based in a dedicated game launcher. For these versions,
    it is recommended to uninstall and reinstall. Before doing this, it is a good idea to make a
    backup of your save file, which is kept in the file "pers3.dat". Note that for certain
    installations and on certain OSes, "pers3.dat" is not saved in the same location as the main
    game directory Globin uses for addin installation. Where it is will vary depending on your OS
    and your installation.

~~~

### 4: Playing With Your Addins

Once Globin has run, and provided it has not thrown any errors, your installed addins should now be
playable. The addins can be found in Chapter 1, making up a growing tower of level buttons in the
top-left corner of the map. The levels are displayed in order of installation, left-to-right and then
top-to-bottom. Levels in packs will go together, but otherwise the only way to ensure the order of
installed addins is to alphabetize them manually.

For now, the only way to know which level a button corresponds to is to hover over the button. This
may change in the future, but for now it is not on the list of important changes.

~~~

### 5: Reporting Bugs and Asking Questions

This README will be unable to cover every possible test case, and the program could run into obscure
flaws that were not considered during creation. If you run into one of these questions or bugs, the
easiest way to get the issue resolved is to open a topic in the modding forums on the GooFans Discord
server. It can be accessed here: https://discord.gg/6BEecnD.

If you do not wish to create an account or otherwise join this server, Globin has a GitHub page where
issue requests can be opened for anything you believe to be a bug. Before opening, however, please
check the already-opened issues (if any) to make sure your issue has not already been opened by
another user of Globin. It can be accessed here: 

    ## 5.1: Known Problems

    This is a list of a handful of known issues with Globin that have yet to be fixed. This list is
    updated frequently on GitHub to reflect issues that have arisen or have been fixed.

    - Currently, the Experimental Level Project does not work with Globin. The first level crashes
      when being opened. It is not yet known why this is. If you think you might know the problem,
      please open a topic on the GooFans discord or raise an issue on GitHub.
