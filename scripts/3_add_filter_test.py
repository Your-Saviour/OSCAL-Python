import re
import shutil
from docx import Document
from typing import Tuple, List
import uuid

## GO BACK TO ADD RUNS IT SHOULD WORK YOU JUST NEED TO RUN iter_inner_content() before you print!!!!!!

def regex_matches(text: str, pattern: str) -> Tuple[int, List[str]]:
    """
    Find regex matches for a given pattern in a string.

    Args:
        text (str): The input string to search in.
        pattern (str): The regex pattern to match.

    Returns:
        Tuple[int, List[str]]: A tuple containing the number of matches 
                               and a list of the matches.
    """
    matches = re.findall(pattern, text)
    return len(matches), matches

def encode_to_zw(text: str) -> str:
    return ''.join('\u200B' if bit == '0' else '\u200C'
                   for ch in text
                   for bit in format(ord(ch), '08b'))

def decode_from_zw(zw_text: str) -> str:
    binary_data = ''.join('0' if ch == '\u200B' else '1' for ch in zw_text)
    return ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))

def show_zero_width(encoded: str) -> str:
    mapping = {
        '\u200B': '\\u200B',  # must be double backslash in source
        '\u200C': '\\u200C',
    }
    return ''.join(mapping.get(ch, ch) for ch in encoded)

def decode_from_zw_safe(zw_text: str) -> str:
    # Collect only the two zero-width chars
    binary_data = ''.join(
        '0' if ch == '\u200B' else
        '1' if ch == '\u200C' else
        '' for ch in zw_text
    )

    # Rebuild text from 8-bit binary chunks
    decoded = ''.join(
        chr(int(binary_data[i:i+8], 2))
        for i in range(0, len(binary_data), 8)
        if len(binary_data[i:i+8]) == 8
    )
    return decoded

def decode_zw_in_place(text: str) -> str:
    """
    Decode zero-width characters (\u200B = 0, \u200C = 1) *in place*,
    keeping all other visible characters as-is.
    Each contiguous run of zw chars is decoded into normal text and inserted back.
    """
    out = []
    buffer = []

    for ch in text:
        if ch in ('\u200B', '\u200C'):
            # Collect binary bits
            buffer.append('0' if ch == '\u200B' else '1')
        else:
            # Flush buffer before adding visible char
            if buffer:
                out.append(_decode_binary_buffer(buffer))
                buffer = []
            out.append(ch)

    # Flush if buffer ends the string
    if buffer:
        out.append(_decode_binary_buffer(buffer))

    return ''.join(out)


def _decode_binary_buffer(buffer):
    """Helper to convert a binary string (list of '0'/'1') into text."""
    binary_str = ''.join(buffer)
    chars = [
        chr(int(binary_str[i:i+8], 2))
        for i in range(0, len(binary_str), 8)
        if len(binary_str[i:i+8]) == 8
    ]
    return ''.join(chars)


def md_main(path : str):
    with open(path, "r", encoding="utf-8") as file:
        markdown_content = file.read()
    print(markdown_content)
    print(decode_zw_in_place(markdown_content))









if __name__ == "__main__":
    # Example usage:
    #message = "Hi!"

    md_main("scripts/amazon_case_study.md")

    quit()
    message = str(uuid.uuid4())
    encoded = encode_to_zw(message)
    decoded = decode_from_zw(encoded)

    print("Original:", message)
    print("Encoded (invisible):", encoded)
    print("Visible escapes:", show_zero_width(encoded))  
    print("Decoded:", decoded)

    #quit()
    template_path = "/home/appuser/scripts/filled2.docx"
    output_path="ReplaceTextUsingRegexPattern.docx"
    pattern = r"\}\}"
    #inject_filters_with_spire(template_path, output_path, pattern)

    pattern = r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*\}\}"
    uuid_pattern=r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}"
    document = Document(template_path)
    regex_pattern = re.compile(pattern)  # Find text like [[DATE]]
    replacement_string = "October 5, 2025"
    my_obj = document
    print("\r\n"*3)
    print(dir(my_obj.paragraphs[0]))
    print("\r\n"*3)
    print(my_obj)
    print("\r\n"*3)
    #[print("start:", x.text,"end\n", regex_matches(x.text,uuid_pattern), "\r\n", "\r\n") for x in my_obj.paragraphs]

    #quit()
    for paragraph in my_obj.paragraphs:
        print(paragraph.text)
        print(decode_zw_in_place(paragraph.text))
        print(show_zero_width(paragraph.text))

    quit()
    current_uuid = {
        "text": [],
        "uuid": [],
        "done":False
    }
    all_uuid = {}
    for paragraph in my_obj.paragraphs:
        print(len(current_uuid["uuid"]))
        print("start:", paragraph.text,"end")
        num, matches = regex_matches(paragraph.text,uuid_pattern)
        if num == 2:
            print("Found 2")
            if matches[0] == matches[1]:
                current_uuid["text"].append(paragraph)
                current_uuid["uuid"].append(matches[1])
                current_uuid["done"] = True
        elif num == 1:
            print("Found 1")
            if len(current_uuid["uuid"]) == 0:
                print("Found 1 Start new")
                current_uuid["uuid"].append(matches[0])
                current_uuid["text"].append(paragraph)
                current_uuid["text"][0].text += "\n"
            elif  len(current_uuid["uuid"]) == 1:
                print("Found 1 Using old")
                if current_uuid["uuid"][0] == matches[0]:
                    for run in paragraph.runs:
                        print("adding run :", run.text)
                        current_uuid["text"][0].text += run.text
                    current_uuid["done"] = True
                else:
                    raise NameError
        elif num == 0:
            print("Found 0")
            if len(current_uuid["uuid"]) == 1:
                print("Found 0 Added on")
                print("Found 1 Using old")
                for run in paragraph.runs:
                    print("adding run :", run.text)
                    #print("adding run :", run)
                    #print(current_uuid["text"][0].runs)
                    #print("adding run :", run)
                    current_uuid["text"][0].text += run.text
                    #rint(current_uuid["text"][0].runs)
                    #print(type(current_uuid["text"][0]))
                current_uuid["text"][0].text += "\n"
        else:
            raise NameError
        
        if current_uuid["done"] == True:
            print("Done :", current_uuid["uuid"][0])
            all_uuid[current_uuid["uuid"][0]] = current_uuid
            current_uuid = {
                "text": [],
                "uuid": [],
                "done":False
            }
        print()

    print(all_uuid)
    print("\r\n"*3)
    #[print(x, ":", all_uuid[x]["text"][0].text, "\r\n") for x in all_uuid]
    [[[print(y.text, end="") for y in all_uuid[x]["text"][0].runs], print("")] for x in all_uuid]
    #docx_replace_regex(document, regex_pattern, replacement_string)
    #document.save(output_path)