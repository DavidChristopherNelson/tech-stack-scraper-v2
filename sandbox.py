import json

# Load the extracted_job_data.txt file
with open("extracted_job_data.txt", "r") as file:
    data = json.load(file)

# Extract all company names
industries = set()

for job in data.values():
    if "industry" in job:
        industries.add(job["industry"])

# Count unique companies
unique_industry_count = len(industries)
for industry in industries:
    print(industry)

# Print the result
print(f"Number of unique industries: {unique_industry_count}")
