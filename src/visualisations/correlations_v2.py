import json
import itertools
from collections import defaultdict, Counter
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

# Calculate observed and expected co-occurrences, and compute lift
lift_values = []
for tech1, co_occurs in tech_cooccurrence.items():
    N_A = tech_job_counts[tech1]
    for tech2, observed_cooccurrence in co_occurs.items():
        if tech1 >= tech2:  # Avoid duplicates and self-pairs
            continue
        N_B = tech_job_counts[tech2]
        expected_cooccurrence = (N_A * N_B) / total_jobs
        if expected_cooccurrence > 0:
            lift = observed_cooccurrence / expected_cooccurrence
            lift_values.append((lift, observed_cooccurrence, expected_cooccurrence, tech1, tech2))

# Sort lift values from highest to lowest
sorted_lifts = sorted(lift_values, key=lambda x: x[0], reverse=True)

# Write the results to a text file
with open('tech_lift_output_v2.txt', 'w', encoding='utf-8') as output_file:
    output_file.write("Technology Pairs with Highest Lift Values (Indicates Stronger Than Expected Co-occurrence):\n\n")
    output_file.write("{:<5} {:<20} {:<20} {:<15} {:<15} {:<10}\n".format(
        "Rank", "Technology A", "Technology B", "Observed Co-occ.", "Expected Co-occ.", "Lift"
    ))
    for idx, (lift, observed_cooccurrence, expected_cooccurrence, tech1, tech2) in enumerate(sorted_lifts[:100], start=1):
        output_file.write("{:<5} {:<20} {:<20} {:<15} {:<15.2f} {:<10.2f}\n".format(
            idx, tech1.title(), tech2.title(), observed_cooccurrence, expected_cooccurrence, lift
        ))

    output_file.write("\nTechnology Pairs with Lowest Lift Values (Indicates Less Frequent Co-occurrence Than Expected):\n\n")
    output_file.write("{:<5} {:<20} {:<20} {:<15} {:<15} {:<10}\n".format(
        "Rank", "Technology A", "Technology B", "Observed Co-occ.", "Expected Co-occ.", "Lift"
    ))
    # Sort lifts from lowest to highest for negative deviations
    sorted_lifts_low = sorted(lift_values, key=lambda x: x[0])
    for idx, (lift, observed_cooccurrence, expected_cooccurrence, tech1, tech2) in enumerate(sorted_lifts_low[:100], start=1):
        output_file.write("{:<5} {:<20} {:<20} {:<15} {:<15.2f} {:<10.2f}\n".format(
            idx, tech1.title(), tech2.title(), observed_cooccurrence, expected_cooccurrence, lift
        ))

    # Analyze deviations for specific technologies like AWS
    target_techs = ['aws', 'docker', 'kubernetes', 'devops', 'python', 'java', 'react', 'node.js']
    output_file.write("\nVariations for Specific Technologies:\n\n")
    for tech in target_techs:
        if tech in tech_cooccurrence:
            output_file.write(f"Technology: {tech.title()}\n")
            co_occurs = tech_cooccurrence[tech]
            N_A = tech_job_counts[tech]
            deviations = []
            for other_tech, observed_cooccurrence in co_occurs.items():
                N_B = tech_job_counts[other_tech]
                expected_cooccurrence = (N_A * N_B) / total_jobs
                if expected_cooccurrence > 0:
                    lift = observed_cooccurrence / expected_cooccurrence
                    deviations.append((lift, observed_cooccurrence, expected_cooccurrence, other_tech))
            deviations_sorted = sorted(deviations, key=lambda x: x[0], reverse=True)
            output_file.write("{:<5} {:<20} {:<15} {:<15} {:<10}\n".format(
                "Rank", "Co-occurring Tech", "Observed Co-occ.", "Expected Co-occ.", "Lift"
            ))
            for idx, (lift, observed_cooccurrence, expected_cooccurrence, other_tech) in enumerate(deviations_sorted[:20], start=1):
                output_file.write("{:<5} {:<20} {:<15} {:<15.2f} {:<10.2f}\n".format(
                    idx, other_tech.title(), observed_cooccurrence, expected_cooccurrence, lift
                ))
            output_file.write("\n")
        else:
            output_file.write(f"Technology: {tech.title()} not found in data.\n\n")
