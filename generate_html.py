import json
import openai

def generate_dynamic_html(json_data, api_key):
    openai.api_key = api_key

    prompt = f"""
    You are tasked with creating a dynamic HTML page about smart home devices. Here's the JSON data with news articles:
    {json.dumps(json_data, indent=4)}

    Create an HTML page with:
    - A header that says 'Latest Smart Home Device News'
    - A list of articles with their titles as clickable links, descriptions, and publication sources.
    - A responsive and mobile-friendly design using inline CSS.

    Output both the HTML and inline CSS.
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2000
    )

    return response["choices"][0]["text"]

if __name__ == "__main__":
    try:
        with open("bundle_rss.json", "r") as json_file:  # Use the updated file name
            json_data = json.load(json_file)

        # Replace with your OpenAI API key
        openai_api_key = "your_openai_api_key"

        # Generate the HTML
        dynamic_html = generate_dynamic_html(json_data, openai_api_key)

        # Save the HTML to a file
        with open("smart_home_news.html", "w") as html_file:
            html_file.write(dynamic_html)

        print("Dynamic HTML generated and saved as smart_home_news.html.")
    except FileNotFoundError:
        print("Error: 'bundle_rss.json' not found. Ensure the RSS generation step completed successfully.")

