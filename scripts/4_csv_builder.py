import jinja2
import re, shutil, zipfile
import uuid
import json
import csv

template = "/home/appuser/scripts/"
json_file = "/home/appuser/examples/ISM_catalog.json"

with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)



# Configure Jinja2 environment and load the template
template_loader = jinja2.FileSystemLoader(searchpath=template) # Assuming template is in current directory
env = jinja2.Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=True)
template = env.get_template("csv_template.j2")

print(data.keys())

# Render the template with the data
rendered_csv = template.render(data=data)

# Write the rendered content to a CSV file
with open("output.csv", "w", newline="") as f:
    f.write(rendered_csv)

print("CSV file 'output.csv' created successfully.")

