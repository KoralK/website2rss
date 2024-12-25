import os
import requests

def post_to_blogger_with_api_key(blog_id, title, content):
    """
    Post the generated HTML content to Google Blogger using an API key.
    """
    # Retrieve the Blogger API key from the environment
    api_key = os.getenv("BLOGGER_API_KEY")
    if not api_key:
        raise ValueError("BLOGGER_API_KEY is not set in the environment.")

    # Endpoint for creating a new post
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/?key={api_key}"

    # Request payload
    post_body = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }

    # Make the POST request
    try:
        response = requests.post(url, json=post_body)
        response.raise_for_status()
        post = response.json()
        print(f"Post published successfully: {post.get('url')}")
    except requests.RequestException as e:
        print(f"Failed to publish post: {e}")

if __name__ == "__main__":
    try:
        # Load and process the HTML content
        html_file_name = "smart_home_news.html"
        with open(html_file_name, "r") as html_file:
            dynamic_html = html_file.read()

        # Blogger integration
        blog_id = "7130434432160656322"  # Replace with your Blogger blog ID
        post_to_blogger_with_api_key(blog_id, "Latest Smart Home News", dynamic_html)

    except FileNotFoundError:
        print(f"Error: '{html_file_name}' not found.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")
