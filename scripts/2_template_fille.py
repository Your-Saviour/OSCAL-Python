from docxtpl import DocxTemplate, R
import jinja2
import re, shutil, zipfile
import uuid
import json

def encode_to_zw(text: str) -> str:
    return ''.join('\u200B' if bit == '0' else '\u200C'
                   for ch in text
                   for bit in format(ord(ch), '08b'))

def mark(value, uuid):
    #key = encode_to_zw(str(uuid.uuid4()))
    uuid = encode_to_zw(uuid)
    return R(f'|{uuid}>{value}<{uuid}|')
# --- Usage ---
template = "/home/appuser/scripts/mydoctest1.docx"
json_file = "/home/appuser/examples/ISM_catalog.json"

# Load it
doc = DocxTemplate(template)

# Register Jinja2 environment and filter
jinja_env = jinja2.Environment()
jinja_env.filters['mark'] = mark


with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

context = data

#print(context["user"])
doc.render(context, jinja_env=jinja_env)
doc.save("filled.docx")