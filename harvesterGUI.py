#!/usr/bin/env python3
# harvesterGUI.py

# Import necessary libraries
# This GUI uses PySimpleGUI as the library for the GUI. Find documentation here: https://www.pysimplegui.org/en/latest/
import PySimpleGUI as sg
import subprocess

class HarvesterGUI:
    def __init__(self):
        # Initializes the self.domain variable
        self.domain = ""

        # Define the layout for the GUI
        self.layout = [
            [sg.Text("Select Data Source:")],
            [sg.Radio("Harvester", "source", default=True, key="harvester_source"),
             sg.Radio("API", "source", key="api_source"),
             sg.Radio("File", "source", key="file_source"),
             sg.Input(key="file_path", disabled=True),
             sg.FileBrowse(file_types=(("Text Files", "*.txt"), ("All Files", "*.*")))],
            [sg.Text("API Endpoint:", visible=False, key="api_label"), sg.Input(key="api_endpoint", visible=False)],
            [sg.Button("Begin"), sg.Button("Exit")]
        ]

        # Create the window
        self.window = sg.Window("Intelligent Application GUI", self.layout, resizable=True)

    def execute_harvester(self):
        try:
            # Run the Harvester or your selected data source based on user input
            if self.window["harvester_source"].get():
                completed_process = subprocess.run(['python3', "theHarvester/theHarvester.py", self.get_user_options()], capture_output=True, text=True)
                print(completed_process)
                self.display_output(completed_process)
            elif self.window["api_source"].get():
                # Implement logic to call your API based on the user input
                api_endpoint = self.window["api_endpoint"].get()
                print(f"API call will be implemented for: {api_endpoint}")
            elif self.window["file_source"].get():
                file_path = self.window["file_path"].get()
                # Implement logic to process data from the selected file
                # Replace the following line with your actual file processing logic
                print(f"File processing will be implemented for: {file_path}")

        except FileNotFoundError:
            sg.popup_error("Error: The file theHarvester/theHarvester.py does not exist.")

    def display_output(self, completed_process):
        # Display the output in a new window
        sg.popup_scrolled("Execution Output", completed_process.stdout)

    # Function will get user output
    def get_user_options(self):
        # String will be passed thru to command
        options = "-d "

        # Layout for a new window
        optionsLayout = [
            [sg.Text("Enter the domain name you would like to search:")],
            [sg.Input(key="domain")],
            [sg.Button("Enter")]
        ]

        window = sg.Window("Harvester Options", optionsLayout, resizable=True)

        event, values = window.read()

        while True:
            event, values = window.read()

            # Perform actions based on user events
            if event == "Enter":
                self.domain = values["domain"] # Sets global variable domain with this
                options += self.domain + " " # Appends domain to options
                break
            elif event == sg.WIN_CLOSED:
                break
    
        window.close()
        return options

    def run(self):
        # Create an event loop
        while True:
            event, values = self.window.read()

            # Perform actions based on user events
            if event == "Begin":
                self.execute_harvester()
            elif event == sg.WIN_CLOSED or event == "Exit":
                break
            elif event == "file_source":
                # Enable/disable file-related fields based on user selection
                self.window["file_path"].update(disabled=not values["file_source"])

        # Close the window
        self.window.close()

if __name__ == "__main__":
    # Create an instance of the HarvesterGUI class and run the GUI
    gui = HarvesterGUI()
    gui.run()