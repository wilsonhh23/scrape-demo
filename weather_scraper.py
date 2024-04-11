from selenium import webdriver  # Provides the WebDriver API for controlling browsers
from selenium.webdriver.chrome.service import Service  # Helps manage the ChromeDriver service
from selenium.webdriver.common.by import By  # For locating elements by their attributes
from selenium.webdriver.support.ui import WebDriverWait  # Allows waiting for certain conditions
from selenium.webdriver.support import expected_conditions as EC  # Provides conditions for WebDriverWait
from selenium.webdriver.chrome.options import Options  # For setting options on ChromeDriver
from bs4 import BeautifulSoup  # For parsing HTML and navigating the parse tree

# Function to convert temperature from Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius_temp):
    """Convert Celsius to Fahrenheit."""
    return (celsius_temp * 9/5) + 32

# Function to fetch and display weather data for a specified city using Selenium
def fetch_weather(city):
    """Fetch and display weather data for a specified city using Selenium in headless mode."""
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
    for row in weather_rows:
        # Extract the city name, weather condition, and temperature details
        details_cell = row.find_all('td')[1]
        city_name = details_cell.find('a').text.strip()
        condition = details_cell.find('b').find_next_sibling('b').text.strip() if details_cell.find('b') else 'Condition not found'
        temperature_celsius = details_cell.find('span', class_='badge').text.strip()[:-2]  # Remove '°С'
        temperature_fahrenheit = celsius_to_fahrenheit(float(temperature_celsius))

        # Print the formatted weather information
        print(f"{city_name}: {temperature_celsius}°С ({temperature_fahrenheit:.1f}°F), {condition}")

# Entry point of the script
def main():
    city = input("Enter a city to get its weather forecast: ")
    fetch_weather(city)

if __name__ == "__main__":
    main()
