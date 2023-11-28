#!/usr/bin/env python3
# harvesterGUI.py

# This GUI uses PySimpleGUI as the library for the GUI. Find documentation here: https://www.pysimplegui.org/en/latest/

import PySimpleGUI as sg
import os
import subprocess

def execute_python_file(file_path):
    try:
        completed_process = subprocess.run(['python3', file_path, get_user_options()], capture_output=True, text=True)
        if completed_process.returncode == 0:
            print("Execution successful.")
            print("Output:")
            print(completed_process.stdout)
        else:
            print(f"Error: Failed to execute '{file_path}'.")
            print("Error output:")
            print(completed_process.stderr)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")

def get_user_options():
    options = "-d google.com"
    return options

layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")], [sg.Button("Run Test")]]

# Create the window
window = sg.Window("Demo", layout)

# Create an event loop
while True:
    event, values = window.read()
    if event == "Run Test":
       execute_python_file("theHarvester/theHarvester.py") 

    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()
