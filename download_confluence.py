# This script downloads all pages from a Confluence space and saves them as HTML files.
import os
import requests
import json
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get the base URL, space key, username, and API token from environment variables
base_url = os.getenv('CONFLUENCE_URL')
space_key = os.getenv('CONFLUENCE_SPACES_FILTER')
username = os.getenv('CONFLUENCE_USERNAME')
api_token = os.getenv('CONFLUENCE_API_TOKEN')

# Create a session object and set the username and password or API token
session = requests.Session()
session.auth = (username, api_token)

# Get the list of all pages in the space
url = f"{base_url}/rest/api/content?spaceKey={space_key}&type=page"
response = session.get(url)

# Parse the JSON response and get the list of page IDs
print(f"Response status code: {response.status_code}")
if response.status_code != 200:
    print(f"Failed to fetch pages: {response.text}")
    exit(1)
pages = json.loads(response.text)["results"]
page_ids = [page["id"] for page in pages]

# Recursively download all child pages and save each page in its own file
def download_pages(page_id, parent_path=""):
    # Get the page content
    url = f"{base_url}/rest/api/content/{page_id}?expand=body.view,version,children.page"
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
    print(f"{filename} {directory}")
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Page {title} saved to {filename}")

    # Recursively download all child pages
    if "children" in page:
        children = page["children"]["page"]["results"]
        for child in children:
            child_id = child["id"]
            download_pages(child_id, path)


# set the path of the output directory
parent_path="./confluence_pages"

# Loop through the page IDs and download each page and its child pages
for page_id in page_ids:
    download_pages(page_id, parent_path=parent_path)
