 
import requests
from bs4 import BeautifulSoup

url = "https://open-traffic.epfl.ch/index.php/downloads/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    # Parse and extract data from the HTML using BeautifulSoup
    # ...

    # Example: print the title of the page
    print(response.text)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
