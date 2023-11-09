# Info
The goal of this project is to exercise and demonstrate the good practices in software development.

For more information on the project and contribution guidelines see the project Wiki.

# How to Run

- Technical requirements:
  - python 3
  - 'windows-curses' if you run the program in Windows. _curses_ is the text based user interface module that should be 
  already available on macOS and Linux
- The textbased user interface relies on the functionalities of the terminal. The program is started from the
terminal using the syntax `C:\path\to\project\folder> python main.py`.
    - Note: Some functionalities of the program may not be supported in all terminals. Appearance may differ as well.
    - Note: For the start of the program extend the terminal window size to relatively big portion of the screen.
  If the terminal is too small it will not offer enough characters for all the interface features. This will result in
  an error on start.

# How to Use

This program is at its current state entirely keyboard operated. 

The screen is split in multiple windows in the common arrangement for CAD software. The command input area 
is the lowest window labeled _Command_. Above it is the _Prompt_ window which will guide the user
what kind of input is expected. Most of the commands require multiple steps to complete. At the end of
the command execution a sound is audible.

Use the following shortcuts to initiate commands and then follow the instruction in the _Prompt_ window.


| Command      | Shortcut |
|--------------|----------|
| Add Element  | `a`      |
| Del Element  | `d`      |
| Insert Shape | `i`      |
| Clear All    | `c`      |
| Move         | `m`      |
| Rotate       | `r`      |
| Mirror       | `mi`     |
| Scale        | `s`      |

Many of the commands require navigation with the cursor and picking or placing objects in the _Canvas_ or _Palette_
window. Navigation is done with the numlock arrows. Selection is executed with the number _5_ button in the center,
end of navigation/selection is achieved with the _home/7_ button.

<img src="https://github.com/Vasc01/2d-cad-exercise/blob/main/assets/key_navigation.png" width="320" height="400">
