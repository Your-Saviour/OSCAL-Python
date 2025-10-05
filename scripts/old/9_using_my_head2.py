from docxtpl import DocxTemplate
import jinja2
import re, shutil, zipfile

def mark(value, key):
    return f'[["{key}"]]{value}[["/{key}"]]'

def inject_filters(template_path, output_path):
    """Rewrites {{ var }} → {{ var | mark("var") }} in document.xml"""
    shutil.copy(template_path, output_path)

    with zipfile.ZipFile(output_path, "a") as docx:
        xml = docx.read("word/document.xml").decode("utf-8")

        # Regex replacer for simple and dot-notation
        def replacer(match):
            var_expr = match.group(1).strip()
            return f'{{{{ {var_expr} | mark("{var_expr}") }}}}'

        xml_new = re.sub(r'{{\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*}}', replacer, xml)
        docx.writestr("word/document.xml", xml_new)

# --- Usage ---
template = "/home/appuser/scripts/mydoc.docx"
prepared = "template_with_filters.docx"

# Prepare template with injected filters
inject_filters(template, prepared)

# Load it
doc = DocxTemplate(prepared)

# Register Jinja2 environment and filter
jinja_env = jinja2.Environment()
jinja_env.filters['mark'] = mark

context = {
    "user": {"first_name": "Jake", "last_name": "Townsend"},
    "job": {"role": "Cyber Security Engineer", "start_date": "2025-10-05"},
    "items": [
        {"name": "Alice Smith", "role": "Developer", "start_date": "2025-11-01"},
        {"name": "Bob Lee", "role": "Analyst", "start_date": "2025-12-15"},
    ]
}

doc.render(context, jinja_env=jinja_env)
doc.save("filled.docx")
