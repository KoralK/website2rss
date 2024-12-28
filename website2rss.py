import os
import json
import requests
import feedparser


def fetch_rss_data():
    """
    Fetches RSS data from various sources.
    """
    rss_urls = [
        "https://blog.ring.com/category/products-innovation/rss",
        "https://press.aboutamazon.com/press-release-archive?q=blink&s=0",
        "https://www.wyze.com/blogs/smart-home/tagged/news/rss",
        "https://community.reolink.com/category/15/announcements%20and%20news/rss",
        "https://reolink.com/blog/category/news/rss",
        "https://www.lorex.com/blogs/news/tagged/press-release/rss",
        "https://community.arlo.com/t5/Announcements/bd-p/arlo-announcements/rss",
        "https://blog.google/products/google-nest/rss"
    ]

    all_data = {}
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            source_name = feed.feed.title if 'title' in feed.feed else url
            all_data[source_name] = [
                {"title": entry.title, "link": entry.link}
                for entry in feed.entries
            ]
            print(f"Successfully fetched and parsed content for {url}")
        except Exception as e:
            print(f"Failed to fetch or parse content for {url}: {e}")

    return all_data


def filter_smart_home_data(data):
    """
    Filters the fetched RSS data to include only smart home-related content.
    """
    filtered_data = {}
    keywords = ["smart home", "security", "camera", "device", "automation"]

    for source, articles in data.items():
        filtered_articles = [
            article for article in articles
            if any(keyword in article['title'].lower() for keyword in keywords)
        ]
        if filtered_articles:
            filtered_data[source] = filtered_articles

    return filtered_data


def send_rss_to_webhook(data, webhook_url):
    """
    Sends the RSS data to the provided webhook URL.
    """
    try:
        print("Payload being sent to webhook:")
        print(json.dumps(data, indent=2))  # Log the payload for debugging

        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        print("RSS data successfully sent to webhook.")
    except requests.RequestException as e:
        print(f"Failed to send RSS data to webhook: {e}")


if __name__ == "__main__":
    try:
        # Step 1: Fetch RSS data
        new_data = fetch_rss_data()
        print("Fetched RSS data successfully.")

        # Step 2: Filter smart home-related data
        filtered_data = filter_smart_home_data(new_data)
        print("Filtered RSS data successfully.")

        # Step 3: Send filtered RSS data to the webhook
        webhook_url = os.getenv("MAKE_COM_WEBHOOK_URL")
        if not webhook_url:
            raise ValueError("MAKE_COM_WEBHOOK_URL environment variable not set.")
        
        send_rss_to_webhook(filtered_data, webhook_url)

    except Exception as e:
        print(f"Error: {e}")
