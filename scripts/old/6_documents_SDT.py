import zipfile
from lxml import etree
import shutil
import os

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

def read_sdt_values(docx_path):
    with zipfile.ZipFile(docx_path) as docx:
        xml = docx.read("word/document.xml")
    root = etree.fromstring(xml)
    values = {}
    for sdt in root.xpath(".//w:sdt", namespaces=NS):
        tag = sdt.find(".//w:tag", namespaces=NS)
        if tag is not None:
            key = tag.get("{%s}val" % NS["w"])
            text_nodes = sdt.findall(".//w:t", namespaces=NS)
            text = "".join(t.text or "" for t in text_nodes)
            values[key] = text
    return values


def write_sdt_values(template_path, output_path, context):
    # Copy template to new file
    shutil.copy(template_path, output_path)

    with zipfile.ZipFile(output_path, "a") as docx:
        xml = docx.read("word/document.xml")
        root = etree.fromstring(xml)

        for sdt in root.xpath(".//w:sdt", namespaces=NS):
            tag = sdt.find(".//w:tag", namespaces=NS)
            if tag is not None:
                key = tag.get("{%s}val" % NS["w"])
                if key in context:
                    # clear old text
                    for t in sdt.findall(".//w:t", namespaces=NS):
                        t.text = ""
                    # put new text in the first <w:t>
                    first_t = sdt.find(".//w:t", namespaces=NS)
                    if first_t is not None:
                        first_t.text = context[key]

        # Write back
        new_xml = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")
        docx.writestr("word/document.xml", new_xml)

# Fill the template
context = {
    "name": "Jake Townsend",
    "role": "Cyber Security Engineer",
    "start_date": "05 October 2025"
}
write_sdt_values("template_with_sdt.docx", "filled.docx", context)

# Later, after manual edits in Word
print(read_sdt_values("filled.docx"))
# → {'name': 'Jacob Townsend', 'role': 'Cyber Security Engineer', 'start_date': '06 October 2025'}
