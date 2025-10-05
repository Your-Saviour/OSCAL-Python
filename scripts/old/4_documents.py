from docx import Document
from lxml import etree

def set_bookmark_text(doc, bookmark_name, new_text):
    """
    Replace text inside a bookmark by name.
    """
    # Access the raw XML tree
    xml = doc.element.body
    # Find all bookmarkStart tags
    for bookmark in xml.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}bookmarkStart"):
        name = bookmark.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}name")
        if name == bookmark_name:
            # Find the next sibling run (text inside the bookmark)
            parent = bookmark.getparent()
            for sib in parent.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
                sib.text = new_text
                return True
    return False


# Example usage
doc = Document("/home/appuser/scripts/mydoc2.docx")

set_bookmark_text(doc, "name", "Jake Townsend")
set_bookmark_text(doc, "role", "Cyber Security Engineer")
set_bookmark_text(doc, "start_date", "05 October 2025")

doc.save("filled2.docx")
