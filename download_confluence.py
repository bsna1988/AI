# This script downloads all pages from a Confluence space and saves them as HTML files.
import os
import requests
import json
import base64
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# --- Configuration ---
CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL")
CONFLUENCE_USERNAME = os.environ.get("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.environ.get("CONFLUENCE_API_TOKEN")
SPACE_KEY = os.getenv('CONFLUENCE_SPACES_FILTER')

# --- Base64 Encode Credentials for Basic Authentication ---
credentials = f"{CONFLUENCE_USERNAME}:{CONFLUENCE_API_TOKEN}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Basic {encoded_credentials}"
}


# Recursively download all child pages and save each page in its own file
def download_pages(session, page_id, parent_path=""):
    # Get the page content
    url = f"{CONFLUENCE_URL}/rest/api/content/{page_id}?expand=body.view,version,children.page"
    response = session.get(url)

    # Parse the JSON response and get the page title and content
    page = json.loads(response.text)
    title = page["title"]
    content = page["body"]["view"]["value"]

    # Create a new file with the page title as the filename and save the content to it
    path = os.path.join(parent_path, title)
    filename = f"{path}.html"
    # create the directory path if it doesn't exist
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    # write the content to the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Page {title} saved to {filename}! ")

    # Recursively download all child pages
    if "children" in page:
        children = page["children"]["page"]["results"]
        for child in children:
            child_id = child["id"]
            download_pages(session,child_id, path)


if __name__ == "__main__":
    # Create a session with the headers
    session = requests.Session()
    session.headers.update(HEADERS)

    # Get the root page of the space
    url = f"{CONFLUENCE_URL}/rest/api/space/{SPACE_KEY}/content?expand=children.page"
    response = session.get(url)
    space_data = json.loads(response.text)

    # Download all pages in the space
    for page in space_data["page"]["results"]:
        page_id = page["id"]
        download_pages(session,page_id, parent_path='/Users/sasha/AI/confluence_pages')
