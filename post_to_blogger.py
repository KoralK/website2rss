import os
import requests

def post_to_blogger(html_content, blogger_api_key, blog_id):
    """
    Posts the generated HTML content to Blogger.
    """
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {blogger_api_key}"
    }
    post_data = {
        "kind": "blogger#post",
        "title": "Latest Smart Home News",
        "content": html_content
    }

    try:
        response = requests.post(url, headers=headers, json=post_data)
        response.raise_for_status()
        print("Post created successfully on Blogger!")
    except requests.RequestException as e:
        print(f"Failed to post on Blogger: {e}")
        raise

if __name__ == "__main__":
    # Read the HTML content from the generated file
    html_file_name = "smart_home_news.html"
    blog_id = "7130434432160656322"  # Replace with your Blogger blog ID

    try:
        with open(html_file_name, "r") as html_file:
            html_content = html_file.read()
        
        blogger_api_key = os.getenv("BLOGGER_API_KEY")
        if not blogger_api_key:
            raise ValueError("BLOGGER_API_KEY is not set in the environment.")
        
        post_to_blogger(html_content, blogger_api_key, blog_id)
    except FileNotFoundError:
        print(f"Error: '{html_file_name}' not found.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")
