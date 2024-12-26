from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Load OAuth credentials
credentials = Credentials.from_service_account_file('secret.json', scopes=["https://www.googleapis.com/auth/blogger"])

# Build the Blogger API service
blogger_service = build('blogger', 'v3', credentials=credentials)

def post_to_blogger(blog_id, title, content):
    """
    Posts a new blog entry to Blogger using OAuth.
    """
    post_body = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }
    try:
        request = blogger_service.posts().insert(blogId=blog_id, body=post_body)
        response = request.execute()
        print(f"Post created successfully: {response['url']}")
    except Exception as e:
        print(f"Failed to post on Blogger: {e}")
        raise

if __name__ == "__main__":
    # Define the Blog ID, title, and content
    blog_id = '7130434432160656322'  # Replace with your Blog ID
    title = "Test Post with OAuth"
    content = "<p>This is a test post created using OAuth authentication in Python.</p>"

    # Post to Blogger
    post_to_blogger(blog_id, title, content)
