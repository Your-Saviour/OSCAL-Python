from spire.doc import *
from spire.doc.common import *
import re
import shutil
#from docx import Document

# Regex for {{ variable }} placeholders (supports dot-notation)
#pattern = r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*\}\}"

def inject_filters_with_spire(template_path, output_path, pattern):
    shutil.copy(template_path, output_path)

    regex = Regex(pattern)
    document = Document()
    document.LoadFromFile(output_path)

    document.Replace(regex, "| mark() }}")

    

    document.SaveToFile(output_path, FileFormat.Docx2016)
    document.Close()




if __name__ == "__main__":
    template_path = "/home/appuser/scripts/mydoc.docx"
    output_path="ReplaceTextUsingRegexPattern.docx"
    pattern = r"\}\}"
    inject_filters_with_spire(template_path, output_path, pattern)

    