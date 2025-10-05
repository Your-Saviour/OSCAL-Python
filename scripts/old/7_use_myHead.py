from docxtpl import DocxTemplate
from jinja2 import Environment

def custom_env(template):
    return Environment(
        block_start_string='<<%',
        block_end_string='%>>',
        variable_start_string='<<',
        variable_end_string='>>',
        comment_start_string='<<#',
        comment_end_string='#>>',
        autoescape=True,
    )

context = {"name": "Jake", "role": "Engineer", "start_date": "2025-10-05"}
doc = DocxTemplate("/home/appuser/scripts/mydoc.docx")
doc.render(context, jinja_env=custom_env(doc))
doc.save("filled.docx")
