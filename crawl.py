import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to retrieve all links on a web page
def get_links(url, base_url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                absolute_url = urljoin(base_url, href)
                links.append(absolute_url)
        return links
    else:
        print(f"Failed to fetch page: {url}")
        return []

# Function to crawl the website recursively
def crawl_website(url, depth):
    if depth <= 0:
        return
    print(f"Crawling: {url}")
    links = get_links(url, base_url)
    for link in links:
        crawl_website(link, depth - 1)

# Specify the starting URL and depth of crawling
start_url = "https://mlops-platform-documentation.craft.ai/"
base_url = "https://mlops-platform-documentation.craft.ai/"
crawl_depth = 2  # You can adjust the depth as needed

crawl_website(start_url, crawl_depth)
