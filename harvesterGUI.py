#!/usr/bin/env python3
# harvesterGUI.py

# This GUI uses PySimpleGUI as the library for the GUI. Find documentation here: https://www.pysimplegui.org/en/latest/
import PySimpleGUI as sg
import os
import subprocess

# This function will run a shell command
def execute_python_file(): 
    try:
        completed_process = subprocess.run(['python3', "theHarvester/theHarvester.py", get_user_options()], capture_output=True, text=True)
        if completed_process.returncode == 0:
            print("Execution successful.")
            print("Output:")
            print(completed_process.stdout)
        else:
            print(f"Error: Failed to execute theHarvester/theHarvester.py.")
            print("Error output:")
            print(completed_process.stderr)
    except FileNotFoundError:
        print(f"Error: The file theHarvester/theHarvester.py does not exist.")

def get_user_options():
    options = "-d google.com"
    return options

if __name__ == "__main__":
    layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("Run Test")]]

    # Create the window
    window = sg.Window("Demo", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        if event == "Run Test":
            execute_python_file() 

        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break

    window.close()
