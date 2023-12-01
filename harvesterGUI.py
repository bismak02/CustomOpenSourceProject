#!/usr/bin/env python3
# harvesterGUI.py

# Import necessary libraries
# This GUI uses PySimpleGUI as the library for the GUI. Find documentation here: https://www.pysimplegui.org/en/latest/
import PySimpleGUI as sg
import os
import subprocess
from datetime import datetime
import json

class HarvesterGUI:
    def __init__(self):
        # Getting absolute path of the harvester python script to avoid nonsense
        self.dirname = os.path.dirname(__file__)
        self.harvesterPath = os.path.join(self.dirname, 'theHarvester/theHarvester.py')

        # Initializes the self.domain variable for use across the program
        self.domain = ""

        # Define the layout for the GUI
        self.layout = [
            [sg.Text("Select Data Source:")],
            [sg.Radio("Harvester", "source", default=True, key="harvester_source"),
             sg.Radio("DomainDB Search", "source", key="api_source"),
             sg.Radio("Analyze JSON File", "source", key="file_source"),
             sg.Input(key="file_path", disabled=True),
             sg.FileBrowse(file_types=(("JSON Files", "*.json"),))],
            [sg.Button("Begin"), sg.Button("Exit")]
        ]

        # Create the window
        self.window = sg.Window("Intelligent Application GUI", self.layout, resizable=True)

    def execute_harvester(self):
        # Run the Harvester or your selected data source based on user input
        if self.window["harvester_source"].get():
            command = ['python3', self.harvesterPath] + self.get_user_options() # Create the command to run
            sg.popup_non_blocking("Application is running. Please be patient...", keep_on_top=True, auto_close=True) # Create a popup that closes once the following line is done executing
            completed_process = subprocess.run(command, capture_output=True, text=True) # Runs the command to execute the harvester
            self.display_output(completed_process) # Creates the output window
        elif self.window["api_source"].get():
            # Calls domainDB method and all is handled within the call.
            self.domainDB()
        elif self.window["file_source"].get():
            file_path = self.window["file_path"].get()
            self.formatJSON(file_path)

    def display_output(self, completed_process):
        # Display the output in a new window
        sg.popup_scrolled("Execution Output", completed_process.stdout)

    def domainDB(self):
        domainDBLayout = [
            [sg.Text("Enter the name of the domain you would like to search domainDB for:")],
            [sg.Input(key="user_input_source", default_text=self.domain)],
            [sg.Button("Search")]
        ]

        domainDBWindow = sg.Window("domainDB Search", domainDBLayout, resizable=True)

        while True:
            event, values = domainDBWindow.read()
            
            if event == "Search":
                self.domain = values["user_input_source"] # Sets global variable domain with this

                command = ['curl', '-X', 'GET', '--header', '\'Accept: application/json\'', f'https://api.domainsdb.info/v1/domains/search?limit=50&domain={self.domain}', '|', 'json_pp'] # Create the command to run
                sg.popup_non_blocking("Searching domainDB. Please be patient...", keep_on_top=True, auto_close=True) # Create a popup that closes once the following line is done executing
                completed_process = subprocess.run(command, capture_output=True, text=True) # Runs the command to execute the harvester
                self.display_output(completed_process) # Creates the output window
                break
            elif event == sg.WIN_CLOSED:
                break

        domainDBWindow.close()

    # Function will get user output
    def get_user_options(self):
        # String will be passed thru to command
        options = ["-d"]

        # Layout for a new window
        optionsLayout = [
            [sg.Text("Enter the domain name you would like to search:")],
            [sg.Input(key="user_input_source", default_text=self.domain)],
            [sg.Text("-------------------------------------------------------------------------------")],
            [sg.Text("Choose your search API:")],
            [sg.Radio("anubis", "search", key="anubis", default=True),
             sg.Radio("baidu", "search", key="baidu"),
             sg.Radio("bevigil", "search", key="bevigil")],
            [sg.Radio("binaryedge", "search", key="binaryedge"),
             sg.Radio("bing", "search", key="bing"),
             sg.Radio("bingapi", "search", key="bingapi")],
            [sg.Radio("bufferoverun", "search", key="bufferoverun"),
             sg.Radio("brave", "search", key="brave"),
             sg.Radio("censys", "search", key="censys")],
            [sg.Radio("certspotter", "search", key="certspotter"),
             sg.Radio("criminalip", "search", key="criminalip"),
             sg.Radio("crtsh", "search", key="crtsh")],
            [sg.Radio("dnsdumpster", "search", key="dnsdumpster"),
             sg.Radio("duckduckgo", "search", key="duckduckgo"),
             sg.Radio("fullhunt", "search", key="fullhunt")],
            [sg.Radio("github-code", "search", key="github-code"),
             sg.Radio("hackertarget", "search", key="hackertarget"),
             sg.Radio("hunter", "search", key="hunter")],
            [sg.Radio("hunterhow", "search", key="hunterhow"),
             sg.Radio("intelx", "search", key="intelx"),
             sg.Radio("netlas", "search", key="netlas")],
            [sg.Radio("onyphe", "search", key="onyphe"),
             sg.Radio("otx", "search", key="otx"),
             sg.Radio("pentesttools", "search", key="pentesttools")],
            [sg.Radio("projectdiscovery", "search", key="projectdiscovery"),
             sg.Radio("rapiddns", "search", key="rapiddns"),
             sg.Radio("rocketreach", "search", key="rocketreach")],
            [sg.Radio("securityTrails", "search", key="securityTrails"),
             sg.Radio("sitedossier", "search", key="sitedossier"),
             sg.Radio("subdomaincenter", "search", key="subdomaincenter")],
            [sg.Radio("subdomainfinderc99", "search", key="subdomainfinderc99"),
             sg.Radio("threatminer", "search", key="threatminer"),
             sg.Radio("tomba", "search", key="tomba")],
            [sg.Radio("urlscan", "search", key="urlscan"),
             sg.Radio("virustotal", "search", key="virustotal"),
             sg.Radio("yahoo", "search", key="yahoo")],
            [sg.Radio("zoomeye", "search", key="zoomeye")],
            [sg.Text("-------------------------------------------------------------------------------")],
            [sg.Text("Would you like to save this output?"), sg.Radio("Yes", "save", key="y"), sg.Radio("No", "save", key="n", default=True)],
            [sg.Button("Enter")]
        ]

        # Creates option window
        optionsWindow = sg.Window("Harvester Options", optionsLayout, resizable=True)

        while True:
            event, values = optionsWindow.read()

            # Perform actions based on user events
            if event == "Enter":
                self.domain = values["user_input_source"] # Sets global variable domain with this
                searchChoice = None
                saveChoice = []
                # Loop checks for what option the user selected and sets searchChoice equal to the user input.
                for choice in ["anubis", "baidu", "bevigil", "binaryedge", "bing", "bingapi", 
                                "bufferoverun", "brave", "censys", "certspotter", "criminalip", "crtsh", 
                                "dnsdumpster", "duckduckgo", "fullhunt", "github-code", "hackertarget", 
                                "hunter", "hunterhow", "intelx", "netlas", "onyphe", "otx", "pentesttools",
                                "projectdiscovery", "rapiddns", "rocketreach", "securityTrails", 
                                "sitedossier", "subdomaincenter", "subdomainfinderc99", "threatminer",
                                "tomba", "urlscan", "virustotal", "yahoo", "zoomeye"]:
                    if values[choice]:
                        searchChoice = choice
                for choice in ["y", "n"]:
                    if values[choice] and choice == "y":
                        saveChoice = ["-f", "theHarvester_"+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")]
                options.extend([self.domain, "-b", searchChoice] + saveChoice) # Appends options
                break
            elif event == sg.WIN_CLOSED:
                break
    
        optionsWindow.close()
        return options
    
    def formatJSON(self, unformatted_file):
        with open(unformatted_file, 'r') as file:
            data = json.load(file)

            formatted_json = json.dumps(data, indent=4, sort_keys=True)
            with open(unformatted_file, 'w') as file2:
                file2.write(formatted_json)
            file2.close()
        file.close()

        sg.popup_scrolled("Analyzed Output:", self.count_json_pairs(unformatted_file))

    
    def count_json_pairs(self, file_path):
        pair_counts = {}

        with open(file_path, 'r') as file:
            data = json.load(file)

        def count_pairs(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    pair = f"{key}: {json.dumps(value)}"
                    pair_counts[pair] = pair_counts.get(pair, 0) + 1
                    count_pairs(value)
            elif isinstance(obj, list):
                for item in obj:
                    count_pairs(item)

        count_pairs(data)

        return pair_counts

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
