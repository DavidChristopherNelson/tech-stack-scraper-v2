"""
Warning! Potentially expensive API calls exist in this script. 
This script converts the text scraped from the job description web page into a
json file saved in extracted_job_data.txt. It does this by making API calls to 
ChatGPT.
"""

import json
import os
import time
from datetime import datetime 
import openai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv("OPEN_AI_PASSWORD")


def strip_whitespace(text):
    """Does some preprocessing on data."""
    # Remove code block markers and whitespace
    cleaned_text = text.strip()
    if cleaned_text.startswith("```") and cleaned_text.endswith("```"):
        first_newline = cleaned_text.find("\n")
        cleaned_text = cleaned_text[first_newline + 1 : -3]
    return cleaned_text

# Get data from .txt file
with open("../data/raw_job_descriptions.txt", "r", encoding="utf-8") as file:
    raw_job_descriptions = json.load(file)

extracted_job_data = {}
LOOP_NUM = 1
start_time = time.time()
time_now = datetime.now().strftime("%Y_%m_%d_%H_%M")
for href, raw_job_description in raw_job_descriptions.items():
    time.sleep(0.5)
    progress_status_percentage = 100 * LOOP_NUM / len(raw_job_descriptions)
    print(f"{progress_status_percentage}%")
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"{minutes}min and {seconds}sec since the start of the program.")
    print(
        f"""Program is estimated to finish in 
        {(100*elapsed_time/progress_status_percentage)/60}min."""
    )
    LOOP_NUM = LOOP_NUM + 1
    chatgpt_response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"""Your response should be valid json without any 
                code block markers or additional text. It will be a dictionary 
                containing the following keys 'salary_min', 'salary_max', 
                'equity_min', 'equity_max', 'currency', 'tech_stack', 
                'company_name', 'location', 'commitment', 'job_title', 
                'required_experience', 'company_size' and 'industry'. For 
                multiple locations use a list of strings. For tech_stack use a 
                list of strings. For salary_min, salary_max, equity_min, 
                equity_max, required_experience and company_size the value 
                should be a single number. Each string corresponds to the name 
                of any technologies or skills that are mentioned in the job 
                description. {raw_job_description}""",
            },
        ],
        temperature=0.7,
        max_tokens=350,
    )
    try:
        # Extract and clean the JSON content
        response_content = chatgpt_response["choices"][0]["message"]["content"]
        json_content = strip_whitespace(response_content)
        extracted_job_data[href] = json.loads(json_content)
        # Save extracted job data as it is received
        with open(f"../data/extracted_job_data_{time_now}.txt", "w", encoding="utf-8") as file:
            json.dump(extracted_job_data, file, indent=4)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print(f"Response text was: {chatgpt_response}")

# Save extracted job data to extracted_job_data.txt
with open(f"../data/extracted_job_data_{time_now}.txt", "w", encoding="utf-8") as file:
    json.dump(extracted_job_data, file, indent=4)
