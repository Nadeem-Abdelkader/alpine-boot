"""
ALPINE BOOT SCREEN Application
- Reads user data from .txt file then allows user to edit and writes back updated data to .txt file

Created by: Nadeem Abdelkader on 9/4/2022
Last updated by Nadeem Abdelkader on 10/4/2022

GUI framework = Tkinter
"""

# !/usr/bin/env python3

# importing the helper functions from functions.py
from functions import text_alert, create_buttons, my_root

if __name__ == '__main__':
    """
    Calling the helper functions from functions.py to start and run the application
    """
    text_alert()
    create_buttons()
    my_root.mainloop()
