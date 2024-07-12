import os
import openai
import logging
import time
import json
from dotenv import load_dotenv

# Load .env file and set up logging
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

def process_text(input_text):
    try:
        prompt = f"Using this info:\n\n{input_text}\n\nQuery:\nRemove everything from the info above that isn’t medical info. Place just the medical info into a code block. Include ALL the bullet points."
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=max_tokens
        )
        processed_text = response['choices'][0]['text'].strip()

        # Read existing data
        try:
            with open('summary_data.json', 'r') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {}

        # Update data with medical info
        data['medical_info'] = processed_text

        # Write updated data back to the JSON file
        with open('summary_data.json', 'w') as json_file:
            json.dump(data, json_file)

        logging.info("Text processing successful.")
        return processed_text
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        time.sleep(1)  # Simple retry logic
        return f"Error: {str(e)}"

if __name__ == "__main__":
    input_text = "text copied from website"
    medical_info = process_text(input_text)
    print(medical_info)
