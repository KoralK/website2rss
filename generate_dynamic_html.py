import os
import google.generativeai as genai
import json

def generate_dynamic_html(json_data, api_key):
    """
    Generates dynamic HTML content using the Gemini 2.0 Flash API.

    Args:
        json_data (dict): JSON data for HTML generation.
        api_key (str): The Gemini API key.

    Returns:
        str: The generated HTML content.
    Raises:
        Exception: If HTML generation fails.
    """
    # Configure the Gemini API client
    genai.configure(api_key=api_key)

    # Convert JSON data to a suitable prompt format (if necessary)
    prompt = (
        "Generate a dynamic HTML page for smart home device news "
        "with a responsive design. JSON data: " + json.dumps(json_data)
    )

    # Generate HTML using Gemini API
    try:
        # Using the GenerativeModel class for generating content
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([prompt])  # Pass prompt as a list
        return response["text"]  # Ensure the response structure matches
    except Exception as e:
        print(f"Error generating HTML: {e}")
        raise

if __name__ == "__main__":
    try:
        # Load JSON data
        json_file_name = "bundle_rss.json"
        with open(json_file_name, "r") as json_file:
            json_data = json.load(json_file)
        print("JSON data loaded successfully.")

        # Retrieve API key from environment
        gemini_api_key = os.getenv("GEMINI_FLASH_API_KEY")
        if not gemini_api_key:
            raise ValueError("GEMINI_FLASH_API_KEY is not set in the environment.")

        # Generate the HTML
        print("Generating HTML...")
        dynamic_html = generate_dynamic_html(json_data, gemini_api_key)

        # Save the HTML to a file
        html_file_name = "smart_home_news.html"
        with open(html_file_name, "w") as html_file:
            html_file.write(dynamic_html)
        print(f"HTML file '{html_file_name}' created successfully.")

    except FileNotFoundError:
        print(f"Error: '{json_file_name}' not found. Ensure the RSS generation step completed successfully.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")