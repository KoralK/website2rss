import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Load credentials and initialize Blogger API
credentials = Credentials.from_service_account_file('secret.json', scopes=["https://www.googleapis.com/auth/blogger"])
blogger_service = build('blogger', 'v3', credentials=credentials)


def list_blogs():
    """
    Lists all blogs for the authenticated user.
    """
    blogs = blogger_service.blogs().listByUser(userId="self").execute()
    print("\nAvailable Blogs:")
    for idx, blog in enumerate(blogs["items"], start=1):
        print(f"{idx}. {blog['name']} (ID: {blog['id']})")
    return blogs["items"]


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


def main():
    blogs = list_blogs()
    blog_choices = {str(idx): blog for idx, blog in enumerate(blogs, start=1)}

    choice = input("\nChoose a blog by number (or type 'new' to create a new blog): ")
    if choice == "new":
        print("Blog creation not implemented yet.")
        return

    if choice not in blog_choices:
        print("Invalid choice. Exiting.")
        return

    selected_blog = blog_choices[choice]
    print(f"You selected: {selected_blog['name']} (ID: {selected_blog['id']})")

    action = input("Do you want to (1) overwrite an existing post or (2) create a new post? [1/2]: ")
    if action == "1":
        print("Overwriting an existing post is not implemented yet.")
    elif action == "2":
        # Define the title and content (can be dynamically passed from other scripts)
        title = "Generated Post Title"
        with open("smart_home_news.html", "r") as html_file:
            content = html_file.read()

        post_to_blogger(selected_blog['id'], title, content)
    else:
        print("Invalid action. Exiting.")


if __name__ == "__main__":
    main()