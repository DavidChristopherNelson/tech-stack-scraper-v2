import matplotlib.pyplot as plt
import math

# Data for the first pie chart
labels1 = ['React', 'Python', 'TypeScript (TS)', 'PostgreSQL', 'Node.js',
           'JavaScript (JS)', 'Docker', 'Kubernetes', 'Next.js', 'Redis']
sizes1 = [20.84, 15.99, 14.23, 12.12, 10.19, 7.30, 5.69, 5.40, 4.33, 3.90]

# Data for the second pie chart
labels2 = ['AWS', 'GCP', 'Google Cloud', 'Azure', 'DynamoDB', 'Firebase',
           'Vercel', 'OpenAI', 'Heroku', 'GitHub']
counts2 = [443, 87, 53, 46, 43, 34, 32, 30, 24, 21]
total_counts2 = sum(counts2)
sizes2 = [(count / total_counts2) * 100 for count in counts2]

# Calculate radii based on area ratio
area_ratio = 2  # Area1 is twice Area2
radius2 = 1     # Radius for the second pie chart (default)
radius1 = math.sqrt(area_ratio) * radius2  # ~1.414

# Create a figure
fig = plt.figure(figsize=(15, 8))

# Add axes for the first pie chart (larger)
# [left, bottom, width, height] in fractions of figure size
ax1 = fig.add_axes([0.1, 0.1, 0.5, 0.8])  # Adjusted to accommodate larger pie

# Add axes for the second pie chart (smaller)
ax2 = fig.add_axes([0.7, 0.4, 0.25, 0.25])  # Positioned to the right

# Define color palettes for consistency
colors1 = plt.cm.tab20.colors[:10]  # First 10 colors for the first pie chart
colors2 = plt.cm.Paired.colors[:10]  # First 10 colors for the second pie chart

# First pie chart with larger radius
ax1.pie(
    sizes1, 
    labels=labels1, 
    autopct='%1.0f%%',  # Rounded to nearest whole number
    startangle=0, 
    radius=radius1,
    colors=colors1
)
ax1.axis('equal')  # Ensures the pie chart is a circle
ax1.set_title('Top Open Source Technologies')

# Second pie chart with default radius
ax2.pie(
    sizes2, 
    labels=labels2, 
    autopct='%1.0f%%',  # Rounded to nearest whole number
    startangle=0, 
    radius=radius2,
    colors=colors2
)
ax2.axis('equal')  # Ensures the pie chart is a circle
ax2.set_title('Top Proprietary Technologies')

# Display the plots
plt.show()
