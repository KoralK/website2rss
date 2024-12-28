import os
import json
from sendhtml import push_html_to_webhook

def fetch_rss_data():
    """
    Placeholder function to fetch RSS data from various sources.
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

def save_html(data, filename="smart_home_news.html"):
    """
    Saves the filtered RSS data as an HTML file.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            html_content = "<html><body>"
            for source, articles in data.items():
                html_content += f"<h1>{source}</h1>"
                for article in articles:
                    html_content += f"<p><a href='{article['link']}'>{article['title']}</a></p>"
            html_content += "</body></html>"
            file.write(html_content)
        print(f"HTML file saved to {filename}")
    except IOError as e:
        print(f"Error saving HTML file: {e}")

if __name__ == "__main__":
    try:
        # Fetch RSS data
        new_data = fetch_rss_data()
        print("Fetched RSS data successfully.")

        # Filter smart home-related data
        filtered_data = filter_smart_home_data(new_data)
        print("Filtered RSS data successfully.")

        # Save filtered data as HTML
        save_html(filtered_data, "smart_home_news.html")

        # Push the generated HTML to Make.com webhook
        html_file_name = "smart_home_news.html"
        with open(html_file_name, "r") as html_file:
            html_content = html_file.read()
        print(f"HTML file '{html_file_name}' loaded successfully.")

        # Get Make.com webhook URL from environment variable
        webhook_url = os.getenv("MAKE_COM_WEBHOOK_URL")
        if not webhook_url:
            raise ValueError("MAKE_COM_WEBHOOK_URL is not set in the environment.")

        # Push the HTML content to Make.com
        push_html_to_webhook(html_content, webhook_url)

    except Exception as e:
        print(f"Error: {e}")
