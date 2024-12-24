import json
import openai
import os

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

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use GPT-4 or GPT-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates HTML code."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000
    )

    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    try:
        # Load the JSON data generated by the previous script
        with open("bundle_rss.json", "r") as json_file:
            json_data = json.load(json_file)

        # Retrieve the API key from the environment
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set")

        # Generate the HTML
        dynamic_html = generate_dynamic_html(json_data, openai_api_key)

        # Save the HTML to a file
        with open("smart_home_news.html", "w") as html_file:
            html_file.write(dynamic_html)

        print("Dynamic HTML generated and saved as smart_home_news.html.")
    except FileNotFoundError:
        print("Error: 'bundle_rss.json' not found. Ensure the RSS generation step completed successfully.")
    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
