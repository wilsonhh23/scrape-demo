from selenium import webdriver  # Provides the WebDriver API for controlling browsers
from selenium.webdriver.chrome.service import Service  # Helps manage the ChromeDriver service
from selenium.webdriver.common.by import By  # For locating elements by their attributes
from selenium.webdriver.support.ui import WebDriverWait  # Allows waiting for certain conditions
from selenium.webdriver.support import expected_conditions as EC  # Provides conditions for WebDriverWait
from selenium.webdriver.chrome.options import Options  # For setting options on ChromeDriver
from bs4 import BeautifulSoup  # For parsing HTML and navigating the parse tree

# Function to convert temperature from Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius_temp):
    return (celsius_temp * 9/5) + 32

# Function to fetch and display weather data for a specified city using Selenium
def fetch_weather(city):
    # Specify the path to your ChromeDriver
    driver_path = '/Users/wilsonhaynie/Downloads/chromedriver-mac-x64/chromedriver'
    # Initialize the WebDriver service
    service = Service(executable_path=driver_path)
    # Setup Chrome options to run in headless mode (without a GUI)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    # Initialize the Chrome WebDriver with the specified service and options
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Construct and navigate to the search URL
    url = f'https://openweathermap.org/find?q={city}'
    driver.get(url)

    # Wait for the dynamic content to load
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table.table tbody"))
    )

    # Retrieve the page source and quit the driver
    page_source = driver.page_source
    driver.quit()

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')
    # Locate the weather data rows in the HTML
    weather_rows = soup.find('table', class_='table').find('tbody').find_all('tr')
    
    # Iterate through each row to extract and print the weather details
    # Each 'tr' (table row) element contains data for one weather entry
for row in weather_rows:
    # The weather data is divided into 'td' (table data) elements. 
    # Here, we're interested in the second 'td' which contains the main details.
    details_cell = row.find_all('td')[1]
    
    # Extract the city name, which is contained within an 'a' (anchor) element.
    city_name = details_cell.find('a').text.strip()
    
    # The condition (e.g., "scattered clouds") is located next to a 'b' element.
    # If the 'b' element exists, find the next sibling 'b' element and get its text.
    # If not found, default to 'Condition not found'.
    condition = details_cell.find('b').find_next_sibling('b').text.strip() if details_cell.find('b') else 'Condition not found'
    
    # The temperature is displayed inside a 'span' with class 'badge' and includes '°С'.
    # Extract the text, remove the '°С' suffix, and convert it to a float.
    temperature_celsius = details_cell.find('span', class_='badge').text.strip()[:-2]  # Remove '°С'
    
    # Convert the temperature from Celsius to Fahrenheit using a helper function.
    temperature_fahrenheit = celsius_to_fahrenheit(float(temperature_celsius))


# Entry point of the script
def main():
    city = input("Enter a city to get its weather forecast: ")
    fetch_weather(city)

if __name__ == "__main__":
    main()
