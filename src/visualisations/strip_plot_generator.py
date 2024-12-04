import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statistics

# Load data from the JSON file
with open('extracted_job_data.txt', 'r') as file:
    extracted_job_data = json.load(file)

# Prepare data for plotting
strip_plot_data = []
tech_data = {}
tech_companies = {}  # To track companies associated with each technology

for href in extracted_job_data:
    job = extracted_job_data[href]
    if job.get('currency') != "USD":
        continue
    if job.get('salary_min') == None:
        continue

    salary_min = job.get('salary_min')
    salary_max = job.get('salary_max')

    if salary_min is None and salary_max is None:
        continue
    if salary_min is None:
        salary_average = salary_max
    elif salary_max is None:
        salary_average = salary_min
    else:
        salary_average = (salary_min + salary_max) / 2

    tech_stack = job.get('tech_stack', [])
    company_name = job.get('company_name')
    if not company_name:
        continue  # Skip if company name is missing

    for tech in tech_stack:
        strip_plot_data.append({"Technology": tech, "Salary": salary_average})
        
        # Update tech_data
        if tech in tech_data:
            tech_data[tech]["salary_data"].append(salary_average)
        else:
            tech_data[tech] = {
                "salary_data": [salary_average],
                "salary_average": []  # Will be calculated later
            }
        
        # Update tech_companies
        if tech in tech_companies:
            tech_companies[tech].add(company_name)
        else:
            tech_companies[tech] = {company_name}

# Remove technologies associated with only one company
techs_with_multiple_companies = {
    tech for tech, companies in tech_companies.items() if len(companies) > 10
}

# Filter tech_data to include only technologies with multiple companies
tech_data = {tech: data for tech, data in tech_data.items() if tech in techs_with_multiple_companies}

# Filter strip_plot_data to include only technologies with multiple companies
strip_plot_data = [
    entry for entry in strip_plot_data if entry['Technology'] in techs_with_multiple_companies
]

# Now compute salary_average for each tech
for tech in tech_data:
    tech_data[tech]["salary_average"] = statistics.mean(tech_data[tech]["salary_data"])

# Create the ordered list of technologies
tech_ordered_list = sorted(
    tech_data.keys(),
    key=lambda tech: tech_data[tech]["salary_average"],
    reverse=True  # Sort in descending order
)

for tech in tech_ordered_list:
    print(tech)

# Create a DataFrame
df = pd.DataFrame(strip_plot_data)

# Plot the strip plot
plt.figure(figsize=(14, 8))
sns.stripplot(x='Technology', y='Salary', data=df, jitter=True, order=tech_ordered_list)
plt.xticks(rotation=90)
plt.xlabel('Technology')
plt.ylabel('Average Salary (USD)')
plt.title('Average Salary by Technology (Technologies Used by More Than 10 Companies)')
plt.ylim(0, 300000)
plt.tight_layout()
plt.show()
