import os
import json
from sendhtml import push_html_to_webhook

# Save filtered RSS data as HTML
def save_html(data, filename="smart_home_news.html"):
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
    # ... existing logic for generating and filtering RSS ...
    filtered_data = filter_smart_home_data(new_data)

    # Save filtered data as HTML
    save_html(filtered_data, "smart_home_news.html")
