import json
import itertools
from collections import defaultdict, Counter
import numpy as np
import pandas as pd

# Load your data
with open('extracted_job_data.txt', 'r') as f:
    data = json.load(f)

# Initialize structures
tech_job_counts = Counter()               # Counts of jobs mentioning each tech
tech_cooccurrence = defaultdict(Counter) # Counts of co-occurrences between techs
job_tech_matrix = {}                      # Binary matrix of jobs and technologies

# Build counts and co-occurrences
job_ids = []  # To keep track of job postings
for idx, (job_id, job) in enumerate(data.items()):
    tech_stack = job.get('tech_stack', [])
    # Standardize technology names
    tech_stack = [tech.strip().lower() for tech in tech_stack]
    tech_stack = list(set(tech_stack))  # Remove duplicates
    job_ids.append(job_id)
    # Update counts
    for tech in tech_stack:
        tech_job_counts[tech] += 1
    # Update co-occurrences
    for tech1, tech2 in itertools.combinations(tech_stack, 2):
        tech_cooccurrence[tech1][tech2] += 1
        tech_cooccurrence[tech2][tech1] += 1
    # Update job-tech matrix
    job_tech_matrix[job_id] = tech_stack

# Total number of jobs
total_jobs = len(job_ids)

# Convert job-tech matrix to DataFrame for correlation calculation
all_techs = list(tech_job_counts.keys())
job_tech_df = pd.DataFrame(0, index=job_ids, columns=all_techs)

for job_id, techs in job_tech_matrix.items():
    for tech in techs:
        job_tech_df.at[job_id, tech] = 1

# Calculate correlation matrix
correlation_matrix = job_tech_df.corr(method='pearson')

# Prepare the tech list ordered by frequency
top_techs = tech_job_counts.most_common(100)

# Open a text file for writing
with open('tech_analysis_output.txt', 'w', encoding='utf-8') as output_file:
    output_file.write("Top 100 Technologies by Number of Job Mentions:\n\n")
    for rank, (tech, count) in enumerate(top_techs, start=1):
        output_file.write(f"{rank}. {tech.title()} - mentioned in {count} jobs\n")
        # Get co-occurring technologies
        cooccurring_techs = tech_cooccurrence[tech]
        # Order co-occurring techs by decreasing frequency
        sorted_cooccurring = cooccurring_techs.most_common()
        output_file.write("   Co-occurring technologies:\n")
        for other_tech, freq in sorted_cooccurring:
            # Get correlation coefficient
            corr_value = correlation_matrix.at[tech, other_tech]
            if not np.isnan(corr_value):
                output_file.write(f"      {other_tech.title()} - Co-mentioned in {freq} jobs, Correlation: {corr_value:.2f}\n")
        output_file.write("\n")

    # Prepare the list of correlations
    correlations = []

    for tech1 in all_techs:
        for tech2 in all_techs:
            if tech1 < tech2:  # Avoid duplicates and self-correlation
                corr_value = correlation_matrix.at[tech1, tech2]
                if not np.isnan(corr_value):
                    correlations.append((abs(corr_value), tech1, tech2, corr_value))

    # Sort correlations from highest to lowest
    sorted_correlations = sorted(correlations, key=lambda x: x[0], reverse=True)

    output_file.write("\nTop 100 Technology Correlations:\n\n")
    for idx, (abs_corr, tech1, tech2, corr_value) in enumerate(sorted_correlations[:100], start=1):
        output_file.write(f"{idx}. {tech1.title()} - {tech2.title()} : Correlation = {corr_value:.2f}\n")
