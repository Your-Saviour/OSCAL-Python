from md2docx_python.src.docx2md_python import word_to_markdown

markdown_file = "amazon_case_study.md"
word_file = "scripts/filled2.docx"

word_to_markdown(word_file, markdown_file)