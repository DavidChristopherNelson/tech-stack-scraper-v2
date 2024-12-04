from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from selenium.common.exceptions import (
    InvalidArgumentException,
    NoSuchElementException
)
import openai
import json
import random

# Load environment variables from .env file
load_dotenv()
yc_password = os.getenv("YC_PASSWORD")
openai.api_key = os.getenv("OPEN_AI_PASSWORD")

# Set up the WebDriver
driver = webdriver.Chrome()

# Navigate to the login page
driver.get("https://account.ycombinator.com/?continue=https%3A%2F%2Fwww.workatastartup.com%2Fapplication&defaults%5BsignUpActive%5D=true")
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

login_button = driver.find_element(By.XPATH, "//button[contains(@class, 'orange-button')]")
login_button.click()
time.sleep(8)

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

# experience_drop_down_button = driver.find_element(By.XPATH, "//div[@id='minExperience']//div[contains(@class, 'css-tlfecz-indicatorContainer')]")
# experience_drop_down_button.click()
# time.sleep(0.2)
# driver.switch_to.active_element.send_keys(Keys.ARROW_DOWN)
# time.sleep(0.2)
# driver.switch_to.active_element.send_keys(Keys.ARROW_DOWN)
# time.sleep(0.5)
# driver.switch_to.active_element.send_keys(Keys.ENTER)
# time.sleep(0.5)
# experience_drop_down_button.click()
# time.sleep(0.5)
# driver.switch_to.active_element.send_keys(Keys.ENTER)
# time.sleep(0.5)

# remote_drop_down_button = driver.find_element(By.XPATH, "//div[@id='remote']//div[contains(@class, 'css-tlfecz-indicatorContainer')]")
# remote_drop_down_button.click()
# time.sleep(0.2)
# driver.switch_to.active_element.send_keys(Keys.ARROW_DOWN)
# time.sleep(0.2)
# driver.switch_to.active_element.send_keys(Keys.ARROW_DOWN)
# time.sleep(0.2)
# driver.switch_to.active_element.send_keys(Keys.ENTER)

# This delay is to allow the user to manually scroll to expose more search results. The automatic scrolling didn't work. 
time.sleep(120)

# Scroll to expose more search results
# for _ in range(1):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     page_height = driver.execute_script("return document.body.scrollHeight")
#     time.sleep(5)

# Collect hrefs to individual job listings
job_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'View job') and starts-with(@href, 'https://www.workatastartup.com/jobs/')]")
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
        marker = "Other jobs at"
        if "Other jobs at" in page_text:
            raw_job_descriptions[href] = page_text.split(marker)[0]
        else:
            raw_job_descriptions[href] = page_text
    except InvalidArgumentException as e:
        print(f"Invalid URL: {href} - {e}")
        raw_job_descriptions[href] = "Invalid URL"
    except NoSuchElementException as e:
        print(f"Element not found on page: {href} - {e}")
        raw_job_descriptions[href] = "Element not found"

# Save scraped data to results.txt
with open("raw_job_descriptions.txt", "w", encoding="utf-8") as file:
    json.dump(raw_job_descriptions, file, indent=4)

extracted_job_data = {}
chatgpt_response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": 
            f"""Your response should be valid json. It will be a dictionary 
                containing the following keys 'salary_min', 'salary_max', 
                'equity_min', 'equity_max', 'currency', 'tech_stack', 
                'company_name', 'location', 'commitment', 'job_title', 
                'required_experience', 'company_size' and 'industry'. For 
                multiple locations use a list of strings. For tech_stack use a 
                list of strings. For salary_min, salary_max, equity_min, 
                equity_max, required_experience and company_size the value 
                should be a single number. Be consistent in your tech naming, 
                for example either use js or javascript but not a mix of both. 
                Each string corresponds to the name of any technologies or 
                skills that are mentioned in the job description. 
                {list(raw_job_descriptions.values())[0]}"""
        }
    ],
    temperature=0.7,
    max_tokens=250
)
try:
    extracted_job_data["test"] = json.loads(chatgpt_response['choices'][0]['message']['content'])
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")
    print(f"Response text was: {chatgpt_response}")

print("extracted_job_data['test']")
print(extracted_job_data["test"])
driver.quit()
exit()

# for href, raw_job_description in raw_job_descriptions.items():
#     chatgpt_response = openai.ChatCompletion.create(
#         model="gpt-4",  # Use "gpt-3.5-turbo" for ChatGPT 3.5
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": 
#                 f"""Your response should be a python dictionary with four keys. First 
#                 key is "average_salary". First key's value is a single number that is 
#                 the average between the lower salary range limit and the higher 
#                 salary range limit contained in the following job description. If no 
#                 salary range is provided than the first key's value should be "NA". 
#                 The second key is "currency". The second key's value is a three 
#                 letter string representing the currency that the salary range is given.
#                 The third key is "tech_stack". The third key's value is a list of 
#                 strings. These strings are the names of any technologies or skills 
#                 that are mentioned in the job description. Examples of strings 
#                 include Torch, PyTorch, Python, TypeScriptnext.js, nest.js, python, 
#                 aws, gcp, azure, kubernetes, Typescript, Javascript, Golang, API, 
#                 Django, React Native, Webflow, React Web, CSS, HTML, JS, Python 3.0, 
#                 Nginx, Wireless, XML, SMTP, Scrapy, Five 9s of availability, 
#                 multithreading, Git, SMTP, IMAP, SMS, MMS, and the like. The forth key 
#                 is "company". The forth key value is the name of the company. Here is 
#                 the job description. {raw_job_descriptions}"""
#             }
#         ],
#         temperature=0.7,
#         max_tokens=100
#     )
#     try:
#         extracted_job_data[href] = json.loads(chatgpt_response['choices'][0]['message']['content'])
#     except json.JSONDecodeError as e:
#         print(f"Failed to parse JSON: {e}")
#         print(f"Response text was: {chatgpt_response}")
# 
# # Save extracted job data to extracted_job_data.txt
# with open("extracted_job_data.txt", "w", encoding="utf-8") as file:
#     json.dump(extracted_job_data, file, indent=4)



# print("------------------------------------- response -------------------------------------")
# print(response)
# response_text = response['choices'][0]['message']['content']
# try:
#     response_dict = json.loads(response_text)
# #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX I need to write this line of code XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# except json.JSONDecodeError as e:
#     print(f"Failed to parse JSON: {e}")
#     print(f"Response text was: {response_text}")

# for result in results:
#     response = openai.ChatCompletion.create(
#         model="gpt-4",  # Use "gpt-3.5-turbo" for ChatGPT 3.5
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": "How do I make an API call to ChatGPT?"}
#         ],
#         temperature=0.7,
#         max_tokens=100,
#     )

# Get the rendered HTML
# rendered_html = driver.page_source

# Prettify the HTML using BeautifulSoup
# soup = BeautifulSoup(rendered_html, "html.parser")
# pretty_html = soup.prettify()

# Save the HTML to a file
# output_file = "pretty_html.html"  # Save as .html
# with open(output_file, "w", encoding="utf-8") as file:
#     file.write(pretty_html)

# Print the HTML to verify (or save it for further processing)
# print(rendered_html)

# Close the WebDriver
# driver.quit()
