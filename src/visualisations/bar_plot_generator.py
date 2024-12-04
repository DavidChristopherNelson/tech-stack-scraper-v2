import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Load data from the JSON file
with open('extracted_job_data.txt', 'r') as file:
    extracted_job_data = json.load(file)

skills_list = []
for href, job_data in extracted_job_data.items():
    if job_data.get('currency') != "USD":
        continue
    for skill in job_data.get('tech_stack'):
        skills_list.append(skill)

sorted_skills = sorted(Counter(skills_list).items(), key=lambda x: x[1], reverse=True)
with open("junk.txt", "a", encoding="utf-8") as file:
    for skill in sorted_skills:
        file.write(f"{skill[0]} {skill[1]}\n")

# Extract technologies and counts
technologies = [item[0] for item in sorted_skills]
counts = [item[1] for item in sorted_skills]

# Limit to top 50 technologies
top_n = 2000
top_technologies = technologies[:top_n]
top_counts = counts[:top_n]

# Create the bar graph
plt.figure(figsize=(12, 8))
plt.bar(top_technologies, top_counts, color='skyblue')
plt.xlabel('Technology')
plt.ylabel('Count')
plt.title('Top 50 Technologies')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
