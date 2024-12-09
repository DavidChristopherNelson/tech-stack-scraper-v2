"""
This script generates a bar plot from the data in 
../data/extracted_job_data.txt. The x-axis lists different technologies and the
y-axis contains the number of mentions for each technology in the job 
descriptions.
"""

import json
from collections import Counter
import matplotlib.pyplot as plt

# Load data from the JSON file
with open("../data/extracted_job_data.txt", "r", encoding="utf-8") as file:
    extracted_job_data = json.load(file)

skills_list = []
for href, job_data in extracted_job_data.items():
    if job_data.get("currency") != "USD":
        continue
    for skill in job_data.get("tech_stack"):
        skills_list.append(skill)

sorted_skills = sorted(Counter(skills_list).items(), key=lambda x: x[1], reverse=True)
with open("junk.txt", "a", encoding="utf-8") as file:
    for skill in sorted_skills:
        file.write(f"{skill[0]} {skill[1]}\n")

# Extract technologies and counts
technologies = [item[0] for item in sorted_skills]
counts = [item[1] for item in sorted_skills]

# Limit to only listing some of the top technologies
TOP_N = 50
top_technologies = technologies[:TOP_N]
top_counts = counts[:TOP_N]

# Create the bar graph
plt.figure(figsize=(12, 8))
plt.bar(top_technologies, top_counts, color="skyblue")
plt.xlabel("Technology")
plt.ylabel("Number of Mentions in the Job Descriptions")
plt.title("Top 50 Technologies")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
