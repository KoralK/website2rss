import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def initialize_blogger_service():
    """
    Initialize the Blogger API service using credentials from a file.
    """
    credentials = Credentials.from_service_account_file(
        'secret.json', scopes=["https://www.googleapis.com/auth/blogger"]
    )
    return build('blogger', 'v3', credentials=credentials)


def list_blogs(blogger_service):
    """
    List all blogs for the authenticated user.
    """
    try:
        blogs = blogger_service.blogs().listByUser(userId="self").execute()
        print("\nAvailable Blogs:")
        for idx, blog in enumerate(blogs["items"], start=1):
            print(f"{idx}. {blog['name']} (ID: {blog['id']})")
        return blogs["items"]
    except Exception as e:
        print(f"Error fetching blogs: {e}")
        raise


def map_post_parameters(blog_id, title, content, status="live", labels=None, location=None):
    """
    Map the post parameters to a structure suitable for the Blogger API.
    """
    return {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "status": status,
        "labels": labels or [],
        "location": location or {"name": "", "lat": "", "lng": "", "span": "1,1"}
    }


def post_to_blogger(blogger_service, blog_id, title, content, status="live", labels=None, location=None):
    """
    Create a new post in Blogger.
    """
    post_body = map_post_parameters(blog_id, title, content, status, labels, location)
    try:
        response = blogger_service.posts().insert(blogId=blog_id, body=post_body).execute()
        print(f"Post created successfully: {response['url']}")
    except Exception as e:
        print(f"Failed to post to Blogger: {e}")
        raise


def main():
    blogger_service = initialize_blogger_service()
    blogs = list_blogs(blogger_service)
    
    blog_choices = {str(idx): blog for idx, blog in enumerate(blogs, start=1)}
    choice = input("\nChoose a blog by number: ")

    if choice not in blog_choices:
        print("Invalid choice. Exiting.")
        return

    selected_blog = blog_choices[choice]
    print(f"You selected: {selected_blog['name']} (ID: {selected_blog['id']})")

    # Define title and content (can be dynamically passed)
    title = "Generated Post Title"
    with open("smart_home_news.html", "r") as html_file:
        content = html_file.read()

    post_to_blogger(blogger_service, selected_blog['id'], title, content)


if __name__ == "__main__":
    main()
