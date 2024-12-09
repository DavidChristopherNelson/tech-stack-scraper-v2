"""
This script scrapes raw data from the YCombinator's job board (scraper.py), it
extracts data via API calls to ChatGPT (gpt_data_extractor.py) and generates
all of the plots used in the blog post https://medium.com/@david.nelson1_80288/
in-demand-the-skills-yc-companies-want-in-2024-0e0c809bd8fa. 
test_chat_gpt_api.py allows you to test the API call before 
gpt_data_extractor.py makes several hundred API calls. 
"""

import subprocess

# Run other Python scripts in the same directory
subprocess.run(["python3", "scraper.py"])
subprocess.run(["python3", "gpt_data_extractor.py"])
subprocess.run(["python3", "visualisations/bar_plot_generator.py"])
subprocess.run(["python3", "visualisations/strip_plot_generator.py"])
subprocess.run(["python3", "visualisations/pie_chart_open_vs_proprietary.py"])
