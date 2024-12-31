import os
import platform

SCORES_FILE_NAME = "Scores.txt"
BAD_RETURN_CODE = 1

def screen_cleaner():
    """
       Clears the terminal screen.

       Works on Windows, macOS, and Linux.
       """
    current_os = platform.system()

    if current_os == "Windows":
        # For Windows
        os.system('cls')
    else:
        # For macOS and Linux (POSIX)
        os.system('clear')