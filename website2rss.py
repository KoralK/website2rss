import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def fetch_website_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_website_to_rss(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Create the root of the RSS feed
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')

    # Add channel metadata
    ET.SubElement(channel, 'title').text = "Website RSS Feed"
    ET.SubElement(channel, 'link').text = base_url
    ET.SubElement(channel, 'description').text = "Automatically generated RSS feed"

    # Parse articles (assuming <a> tags with titles and links represent articles)
    for link in soup.find_all('a', href=True):
        title = link.text.strip()
        if title:
            item = ET.SubElement(channel, 'item')
            ET.SubElement(item, 'title').text = title
            ET.SubElement(item, 'link').text = base_url + link['href']

    # Generate RSS XML
    return ET.tostring(rss, encoding='utf-8').decode('utf-8')

def save_rss_feed(rss_content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(rss_content)

if __name__ == "__main__":
    url = input("Enter the website URL: ")
    base_url = url.rstrip('/')
    html_content = fetch_website_content(url)
    rss_content = parse_website_to_rss(html_content, base_url)
    save_rss_feed(rss_content, "rss_feed.xml")
    print("RSS feed saved as rss_feed.xml")
