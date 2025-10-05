from docx import Document
from lxml import etree

def get_bookmark_text(doc, bookmark_name):
    """
    Read text stored inside a bookmark by name.
    """
    xml = doc.element.body
    for bookmark in xml.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}bookmarkStart"):
        name = bookmark.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}name")
        if name == bookmark_name:
            parent = bookmark.getparent()
            for sib in parent.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
                return sib.text
    return None


# Example usage
doc2 = Document("/home/appuser/scripts/filled2.docx")

print("Name:", get_bookmark_text(doc2, "name"))
print("Role:", get_bookmark_text(doc2, "role"))
print("Start Date:", get_bookmark_text(doc2, "start_date"))