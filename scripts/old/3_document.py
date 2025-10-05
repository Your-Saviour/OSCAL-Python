from docxtpl import DocxTemplate

# Load the template
doc = DocxTemplate("/home/appuser/scripts/mydoc.docx")

# Context: the data to fill in
context = {
    "name": "Jake Townsend",
    "role": "Cyber Security Engineer",
    "start_date": "05 October 2025",
    "items": ["Access Badge", "Laptop", "VPN Token"]
}

# Render (fill) the template
doc.render(context)

# Save as a new file
doc.save("filled.docx")