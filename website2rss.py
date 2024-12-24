import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json
import time

def fetch_website_content(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Referer": url
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return response.text
        except requests.Timeout:
            print(f"Timeout while fetching {url}. Attempt {attempt + 1} of {retries}.")
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}. Attempt {attempt + 1} of {retries}.")
        time.sleep(delay)
    print(f"Failed to fetch {url} after {retries} retries.")
    return None

def parse_website_to_rss(html_content, base_url):
    if not html_content:
        print("Error: No HTML content provided for parsing.")
        return None

    soup = BeautifulSoup(html_content, 'html.parser')

    # Parse articles (assuming <a> tags with titles and links represent articles)
    items = []
    for link in soup.find_all('a', href=True):
        title = link.text.strip()
        if title:
            item = {
                "title": title,
                "link": link['href'] if link['href'].startswith('http') else base_url + link['href']
            }
            items.append(item)
    return items

def generate_bundle_rss_json(urls):
    all_feeds = {}
    for url in urls:
        print(f"Processing URL: {url}")
        html_content = fetch_website_content(url)

        if html_content:
            rss_items = parse_website_to_rss(html_content, url)
            if rss_items:
                all_feeds[url] = rss_items
                print(f"Successfully fetched and parsed content for {url}")
            else:
                print(f"No valid RSS items found for {url}")
        else:
            print(f"Failed to fetch or parse content for {url}")

    return json.dumps(all_feeds, indent=4)

def save_bundle_rss_json(json_data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(json_data)
        print(f"RSS feed bundle saved to {filename}")
    except IOError as e:
        print(f"Error saving RSS feed bundle: {e}")

if __name__ == "__main__":
    urls = [
        "https://blog.ring.com/category/products-innovation/",
        "https://press.aboutamazon.com/press-release-archive?q=blink&s=0",
        "https://www.wyze.com/blogs/smart-home/tagged/news",
        "https://community.reolink.com/category/15/announcements%20and%20news",
        "https://reolink.com/blog/category/news/",
        "https://www.lorex.com/blogs/news/tagged/press-release",
        "https://community.arlo.com/t5/Announcements/bd-p/arlo-announcements",
        "https://www.arlo.com/en-us/press",
        "https://blog.google/products/google-nest/"
    ]

    bundle_rss_json = generate_bundle_rss_json(urls)
    save_bundle_rss_json(bundle_rss_json, "bundle_rss.json")
    print("Generated Bundle RSS Feed JSON:")
    print(bundle_rss_json)
