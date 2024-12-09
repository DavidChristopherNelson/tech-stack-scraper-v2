"""
This script automates the scraping of job postings from YCombinator's 
job board. It logs in using credentials from environment variables, navigates 
the job board, filters by role, collects job links, and extracts page text for 
analysis. Extracted data is saved in JSON format.
"""

import os
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidArgumentException, NoSuchElementException
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()
yc_password = os.getenv("YC_PASSWORD")
openai.api_key = os.getenv("OPEN_AI_PASSWORD")

# Set up the WebDriver
driver = webdriver.Chrome()

# Navigate to the login page
driver.get(
    """https://account.ycombinator.com/?continue=https%3A%2F%2Fwww.
    workatastartup.com%2Fapplication&defaults%5BsignUpActive%5D=true"""
)
time.sleep(1)

# Navigate through the log in sequence.
login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]")
login_button.click()
time.sleep(1)

username_field = driver.find_element(By.ID, "ycid-input")
username_field.send_keys("BobbyBots")

password_field = driver.find_element(By.ID, "password-input")
password_field.send_keys(yc_password)
time.sleep(1)

login_button = driver.find_element(
    By.XPATH, "//button[contains(@class, 'orange-button')]"
)
login_button.click()
time.sleep(80)

# Navigate to the job board page
link = driver.find_element(By.XPATH, "//a[@href='/companies']")
link.click()
time.sleep(1)

# Fill out filter fields
role_input_field = driver.find_element(By.ID, "react-select-2-input")
role_input_field.send_keys("engineering")
time.sleep(0.5)
role_input_field.send_keys(Keys.ENTER)
time.sleep(0.5)

# Scroll to expose more search results
for _ in range(1):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(5)
# This delay is to allow the user to manually scroll to expose more search
# results. The automatic scrolling didn't work.
# time.sleep(120)

# Collect hrefs to individual job listings
job_links = driver.find_elements(
    By.XPATH,
    """//a[contains(text(), 'View job')
     and starts-with(@href, 'https://www.workatastartup.com/jobs/')]""",
)
hrefs = [link.get_attribute("href") for link in job_links]
for href in hrefs:
    print(href)
print(f"len(hrefs)={len(hrefs)}")

# Visit each individual job listing and scrape data
raw_job_descriptions = {}
for href in hrefs:
    try:
        driver.get(href)
        time.sleep(0.5)

        page_text = driver.find_element("tag name", "body").text
        if "Other jobs at" in page_text:
            raw_job_descriptions[href] = page_text.split("Other jobs at")[0]
        else:
            raw_job_descriptions[href] = page_text
    except InvalidArgumentException as e:
        print(f"Invalid URL: {href} - {e}")
        raw_job_descriptions[href] = "Invalid URL"
    except NoSuchElementException as e:
        print(f"Element not found on page: {href} - {e}")
        raw_job_descriptions[href] = "Element not found"

# Save scraped data to a file
time_now = datetime.now().strftime("%Y_%m_%d_%H_%M")
with open(f"raw_job_descriptions_{time_now}.txt", "w", encoding="utf-8") as file:
    json.dump(raw_job_descriptions, file, indent=4)

driver.quit()
