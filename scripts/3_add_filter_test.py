import re
import shutil
from docx import Document

def docx_replace_regex(doc_obj, regex, replace):
    def replacer(match):
            var_expr = match.group(1).strip()
            return f'{{{{ {var_expr} | mark("{var_expr}") }}}}'
    
    for p in doc_obj.paragraphs:
        print(p.text)
        if regex.search(p.text):
            print("IN SEARCH")
            inline = p.runs
            print(inline)
            # Loop added to work with runs (strings with same style)
            for i in range(len(inline)):
                print("INLINE:",inline[i].text)
                if regex.search(inline[i].text):
                    text = regex.sub(replacer, inline[i].text)
                    inline[i].text = text

    # Also handle tables if needed
    for table in doc_obj.tables:
        for row in table.rows:
            for cell in row.cells:
                docx_replace_regex(cell, regex, replace) # Recursively apply to cells


if __name__ == "__main__":
    template_path = "/home/appuser/scripts/mydoc.docx"
    output_path="ReplaceTextUsingRegexPattern.docx"
    pattern = r"\}\}"
    #inject_filters_with_spire(template_path, output_path, pattern)

    pattern = r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*\}\}"
    document = Document(template_path)
    regex_pattern = re.compile(pattern)  # Find text like [[DATE]]
    replacement_string = "October 5, 2025"
    docx_replace_regex(document, regex_pattern, replacement_string)
    document.save(output_path)