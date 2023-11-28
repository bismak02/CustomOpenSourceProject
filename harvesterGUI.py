#!/usr/bin/env python3
# harvesterGUI.py

# This GUI uses PySimpleGUI as the library for the GUI. Find documentation here: https://www.pysimplegui.org/en/latest/
import PySimpleGUI as sg
import os
import subprocess

# This function will run a shell command and will likely not need to be touched much.
def execute_python_file(): 
    try: # For error catching
        # Following line tells python to run a shell and execute the command. Command may look like such: `python3 theHarvester/theHarvester.py "USER OPTIONS HERE"`
        completed_process = subprocess.run(['python3', "theHarvester/theHarvester.py", get_user_options()], capture_output=True, text=True)
        # If command is successful output should be displayed in the window.
        if completed_process.returncode == 0:
            print("Execution successful.")
            print("Output:")
            print(completed_process.stdout)
        # If command fails (it shouldn't) output should be displayed in window as well.
        else:
            print(f"Error: Failed to execute theHarvester/theHarvester.py.")
            print("Error output:")
            print(completed_process.stderr)
    # Should never see this error since the location is hard coded.
    except FileNotFoundError:
        print(f"Error: The file theHarvester/theHarvester.py does not exist.")

# This function will get user input.
def get_user_options():
    options = "-d google.com"
    return options

# Main.
if __name__ == "__main__":
    # "layout" defines how the gui will appear. Just add modules to the array.
    # sg.Text will display text
    # sg.Button will add a button that can be pressed
    layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("Run Test")]]

    # Create the window
    window = sg.Window("Demo", layout)

    # Create an event loop to tell if a button is pressed. If more buttons are added, this can be modified for them.
    while True:
        event, values = window.read()
        if event == "Run Test":
            execute_python_file() 

        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break

    window.close()
