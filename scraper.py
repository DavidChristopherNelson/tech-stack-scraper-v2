from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Set up the WebDriver (adjust to your browser of choice)
driver = webdriver.Chrome()  # Or use webdriver.Firefox(), etc.

# URL for the login page
url = "https://account.ycombinator.com/?continue=https%3A%2F%2Fwww.workatastartup.com%2Fapplication&defaults%5BsignUpActive%5D=true"

# Navigate to the login page
driver.get(url)

# Pause to allow the page to load (adjust based on your network speed)
time.sleep(1)

# Locate the "Log In" button and click it
login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]")
login_button.click()
time.sleep(1)

# Locate the username field and enter the username
username_field = driver.find_element(By.ID, "ycid-input")
username_field.send_keys("DavidCNelson")
print(username_field.get_attribute("value"))

# Locate the password field and enter the password
password_field = driver.find_element(By.ID, "password-input")
yc_password = os.getenv("YC_PASSWORD")
password_field.send_keys(yc_password)
print(password_field.get_attribute("value"))
time.sleep(1)

# Locate the "Log In" button and click it
login_button = driver.find_element(By.XPATH, "//button[contains(@class, 'orange-button')]")
login_button.click()
time.sleep(10)

# Get the rendered HTML
rendered_html = driver.page_source

# Prettify the HTML using BeautifulSoup
soup = BeautifulSoup(rendered_html, "html.parser")
pretty_html = soup.prettify()

# Save the HTML to a file
output_file = "pretty_html.html"  # Save as .html
with open(output_file, "w", encoding="utf-8") as file:
    file.write(pretty_html)

# Print the HTML to verify (or save it for further processing)
# print(rendered_html)

# Close the WebDriver
driver.quit()
