"""
This script generates a strip plot from the data in 
../data/extracted_job_data.txt. The x-axis lists different technologies and the
y-axis contains the number of mentions for each technology in the job 
descriptions.
"""

import json
import statistics
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load data from the JSON file
with open("../data/extracted_job_data.txt", "r", encoding="utf-8") as file:
    extracted_job_data = json.load(file)

# Prepare data for plotting
strip_plot_data = []
tech_data = {}
tech_companies = {}  # To track companies associated with each technology

for href in extracted_job_data:
    job = extracted_job_data[href]
    if job.get("currency") != "USD":
        continue
    if job.get("salary_min") is None:
        continue

    salary_min = job.get("salary_min")
    salary_max = job.get("salary_max")

    if salary_min is None and salary_max is None:
        continue
    if salary_min is None:
        salary_average = salary_max
    elif salary_max is None:
        salary_average = salary_min
    else:
        salary_average = (salary_min + salary_max) / 2

    tech_stack = job.get("tech_stack", [])
    company_name = job.get("company_name")
    if not company_name:
        continue  # Skip if company name is missing

    for tech in tech_stack:
        strip_plot_data.append({"Technology": tech, "Salary": salary_average})

        if tech in tech_data:
            tech_data[tech]["salary_data"].append(salary_average)
        else:
            tech_data[tech] = {
                "salary_data": [salary_average],
                "salary_average": [],  # Will be calculated later
            }

        if tech in tech_companies:
            tech_companies[tech].add(company_name)
        else:
            tech_companies[tech] = {company_name}

# Keep only technologies with more than 10 companies
techs_with_multiple_companies = {
    tech for tech, companies in tech_companies.items() if len(companies) > 10
}

tech_data = {
    tech: data
    for tech, data in tech_data.items()
    if tech in techs_with_multiple_companies
}
strip_plot_data = [
    entry
    for entry in strip_plot_data
    if entry["Technology"] in techs_with_multiple_companies
]

# Compute salary averages
for tech in tech_data:
    tech_data[tech]["salary_average"] = statistics.mean(tech_data[tech]["salary_data"])

# Order the technologies by their average salary
tech_ordered_list = sorted(
    tech_data.keys(), key=lambda tech: tech_data[tech]["salary_average"], reverse=True
)

# Create a DataFrame for the strip plot
df = pd.DataFrame(strip_plot_data)

# Create a DataFrame for the averages
avg_data = [(tech, tech_data[tech]["salary_average"]) for tech in tech_ordered_list]
avg_df = pd.DataFrame(avg_data, columns=["Technology", "Salary"])

# Convert Technology to a categorical type with the specified order
df["Technology"] = pd.Categorical(
    df["Technology"], categories=tech_ordered_list, ordered=True
)
avg_df["Technology"] = pd.Categorical(
    avg_df["Technology"], categories=tech_ordered_list, ordered=True
)

plt.figure(figsize=(14, 8))

# Plot the strip plot with the specified order
sns.stripplot(
    x="Technology", y="Salary", data=df, order=tech_ordered_list, jitter=True, alpha=0.7
)

# Overlay the averages as contrasting points
# Removed the 'order' parameter here
sns.scatterplot(
    x="Technology",
    y="Salary",
    data=avg_df,
    color="red",  # Contrasting color
    s=100,  # Size of the points
    marker="D",  # Diamond-shaped marker for distinction
    edgecolor="black",
)

plt.xticks(rotation=90)
plt.xlabel("Technology")
plt.ylabel("Average Salary (USD)")
plt.title("Average Salary by Technology (Technologies Used by More Than 10 Companies)")
plt.ylim(0, 300000)
plt.tight_layout()
plt.show()
