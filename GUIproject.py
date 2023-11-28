import tkinter as tk
import requests

class APIDataFetcher:
    def __init__(self, root):
        self.root = root
        self.root.title("API Data Fetcher")

        self.label = tk.Label(self.root, text="Choose an API:")
        self.label.pack()

        self.api_options = ["OpenWeatherMap", "SpaceX", "Chuck Norris Jokes", "Quotes"]
        self.api_selection = tk.StringVar()
        self.api_selection.set(self.api_options[0])

        self.api_dropdown = tk.OptionMenu(self.root, self.api_selection, *self.api_options)
        self.api_dropdown.pack()

        self.fetch_button = tk.Button(self.root, text="Fetch Data", command=self.fetch_data)
        self.fetch_button.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

    def fetch_data(self):
        selected_api = self.api_selection.get()

        if selected_api == "OpenWeatherMap":
            # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
            api_key = 'YOUR_API_KEY'
            city = 'New York'  # Change to your desired city
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_desc = data['weather'][0]['description']
                temp_kelvin = data['main']['temp']
                temp_celsius = temp_kelvin - 273.15
                self.result_label.config(text=f"Weather: {weather_desc}, Temperature: {temp_celsius:.2f}°C")
            else:
                self.result_label.config(text="Failed to fetch data from OpenWeatherMap")

        elif selected_api == "SpaceX":
            url = 'https://api.spacexdata.com/v4/launches/latest'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                mission_name = data['name']
                launch_date = data['date_utc']
                self.result_label.config(text=f"Mission: {mission_name}, Launch Date: {launch_date}")
            else:
                self.result_label.config(text="Failed to fetch data from SpaceX")

        elif selected_api == "Chuck Norris Jokes":
            url = 'https://api.chucknorris.io/jokes/random'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                joke = data['value']
                self.result_label.config(text=f"Chuck Norris Joke: {joke}")
            else:
                self.result_label.config(text="Failed to fetch Chuck Norris joke")

        elif selected_api == "Quotes":
            url = 'https://api.quotable.io/random'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                quote = data['content']
                author = data['author']
                self.result_label.config(text=f"Quote: '{quote}' - {author}")
            else:
                self.result_label.config(text="Failed to fetch quote")

def main():
    root = tk.Tk()
    app = APIDataFetcher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
