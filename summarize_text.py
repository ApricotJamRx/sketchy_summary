import os
import openai
import json
import logging
from dotenv import load_dotenv

# Load .env file and setup logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load variables from .env
api_key = os.getenv('OPENAI_API_KEY')
engine = os.getenv('GPT_ENGINE', 'text-davinci-003')
max_tokens = int(os.getenv('MAX_TOKENS', 1024))

if not api_key:
    logging.error("API key not found. Please set OPENAI_API_KEY in the environment variables.")
    raise ValueError("API key not found.")

openai.api_key = api_key

def generate_final_summary():
    # Load data from JSON file
    with open('summary_data.json', 'r') as json_file:
        data = json.load(json_file)
    
    medical_info = data.get('medical_info', '')
    first_draft_summary = data.get('first_draft_summary', '')

    # Construct the prompt for the GPT-4 model
    prompt = f"""
    Here is my next query:
    Context:

    Lesson Info:
    {medical_info}

    First Draft Summary:
    {first_draft_summary}

    Query:
    Using the Lesson Info for reference, edit the First Draft Summary into a Final Draft, following the guidelines below.

    Final Draft Guidelines:
    - Write like an easy-to-follow medical textbook, but be sure there is a clear narrative and things transition smoothly.
    - Bold key concepts
    - Assure ALL the medical information from the Lesson Info is included in the final draft summary***
    """

    try:
        # Make API call to OpenAI
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=max_tokens
        )
        final_summary = response['choices'][0]['text'].strip()
        logging.info("Summary generation successful.")
        return final_summary
    except Exception as e:
        logging.error(f"An error occurred during summary generation: {str(e)}")
        return None

if __name__ == "__main__":
    final_summary = generate_final_summary()
    if final_summary:
        print(final_summary)
    else:
        print("Failed to generate summary.")
