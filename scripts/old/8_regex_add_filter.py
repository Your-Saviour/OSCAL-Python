import zipfile, re, shutil
from lxml import etree

def inject_filters(template_path, output_path):
    shutil.copy(template_path, output_path)

    with zipfile.ZipFile(output_path, "a") as docx:
        xml = docx.read("word/document.xml").decode("utf-8")

        # Regex to wrap variables: {{ var }} → {{ var | mark("var") }}
        def replacer(match):
            var_name = match.group(1).strip()
            return f'{{{{ {var_name} | mark("{var_name}") }}}}'

        xml_new = re.sub(r'{{\s*(\w+)\s*}}', replacer, xml)

        docx.writestr("word/document.xml", xml_new)
