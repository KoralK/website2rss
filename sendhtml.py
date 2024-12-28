import os
import json
import requests

def push_html_to_webhook(html_content, webhook_url):
    """
    Pushes the generated HTML content to the Make.com webhook.

    Args:
        html_content (str): The HTML content to send.
        webhook_url (str): The Make.com webhook URL.

    Returns:
        Response object from the POST request.
    """
    try:
        response = requests.post(
            webhook_url,
            data={"html_content": html_content},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        print("HTML content successfully sent to webhook.")
        return response
    except requests.RequestException as e:
        print(f"Error sending HTML to webhook: {e}")
        raise

if __name__ == "__main__":
    try:
        # Load generated HTML from file
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

    except FileNotFoundError:
        print(f"Error: HTML file '{html_file_name}' not found.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")