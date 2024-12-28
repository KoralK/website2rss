import os
import json
import requests


def fetch_rss_data():
    """
    Fetches RSS data from various sources.
    Replace this with actual implementation to fetch RSS feeds.
    """
    # Example RSS data structure
    return {
        "Source1": [
            {"title": "News Article 1", "link": "https://example.com/article1"},
            {"title": "News Article 2", "link": "https://example.com/article2"}
        ],
        "Source2": [
            {"title": "News Article A", "link": "https://example.com/articleA"},
            {"title": "News Article B", "link": "https://example.com/articleB"}
        ]
    }


def filter_smart_home_data(data):
    """
    Filters the fetched RSS data to include only smart home-related content.
    Replace this with actual filtering logic based on your requirements.
    """
    # Placeholder filtering logic: Return data as-is
    return data


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
