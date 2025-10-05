# downloader.py
import os
import sys
import json
import argparse
import requests
from urllib.parse import urlparse
from datetime import datetime
from logger import get_logger

logger = get_logger("my_script")


def download_json(url: str, output_folder: str) -> str:
    """
    Download a JSON file from the given URL and save it into output_folder.
    Returns the saved file path.
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Fetch JSON
    response = requests.get(url)
    response.raise_for_status()  # raise error if request failed
    data = response.json()  # will raise if not valid JSON

    # Make filename from URL or timestamp
    parsed = urlparse(url)
    base_name = os.path.basename(parsed.path) or f"download_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    if not base_name.endswith(".json"):
        base_name += ".json"

    file_path = os.path.join(output_folder, base_name)

    # Save JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return file_path


def main():
    parser = argparse.ArgumentParser(description="Download a JSON file from a URL and save it to a folder.")
    parser.add_argument("--url", help="The URL to the JSON file")
    parser.add_argument("-o", "--output", help="Output folder (default: ./downloads)")
    args = parser.parse_args()
    logger.debug(args)

    try:
        saved_file = download_json(args.url, args.output)
        logger.debug("✅ JSON saved to: {saved_file}")
        print(f"✅ JSON saved to: {saved_file}")
    except Exception as e:
        print(f"❌ Failed to download JSON: {e}", file=sys.stderr)
        logger.debug(f"❌ Failed to download JSON: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
