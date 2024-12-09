"""
This script sends one raw job description to ChatGPT for processing. The 
purpose is to estimate how much a complete run would cost and to see if the 
output is satisfactory.
"""

import json
import os
import random
from dotenv import load_dotenv
import openai

load_dotenv()  # Load environment variables from .env file
openai.api_key = os.getenv("OPEN_AI_PASSWORD")

with open("../data/raw_job_descriptions.txt", "r", encoding="utf-8") as file:
    raw_job_descriptions = json.load(file)

raw_job_description = random.choice(list(raw_job_descriptions.values()))

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",  # Use "gpt-3.5-turbo" for ChatGPT 3.5
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"""Your response should be valid json without any code block 
            markers or additional text. It will be a dictionary 
            containing the following keys 'salary_min', 'salary_max', 
            'equity_min', 'equity_max', 'currency', 'tech_stack', 
            'company_name', 'location', 'commitment', 'job_title', x
            'required_experience', 'company_size' and 'industry'. For 
            multiple locations use a list of strings. For tech_stack use a 
            list of strings. For salary_min, salary_max, equity_min, 
            equity_max, required_experience and company_size the value 
            should be a single number. Each string corresponds to the name 
            of any technologies or skills that are mentioned in the job 
            description. 
            {raw_job_description}""",
        },
    ],
    temperature=0.7,
    max_tokens=100,
)

print("----------------------------- response -------------------------------")
print(response)

print("------------------------ extracted_job_data --------------------------")
extracted_job_string = response["choices"][0]["message"]["content"]
print(extracted_job_string)

print("---------------------- try to turn into json -------------------------")
try:
    extracted_job_data = json.loads(extracted_job_string)
    print(extracted_job_data)
    print(type(extracted_job_data))
except json.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")
    print(f"Response was: {response}")

print("end of program")
