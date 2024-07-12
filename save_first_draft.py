import json

def save_first_draft_summary(first_draft_summary):
    # Read existing data, if any
    try:
        with open('summary_data.json', 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}
    
    # Update data with the first draft summary
    data['first_draft_summary'] = first_draft_summary

    # Write updated data back to the JSON file
    with open('summary_data.json', 'w') as json_file:
        json.dump(data, json_file)

if __name__ == "__main__":
    # Example text, replace with the actual copied text
    first_draft_summary = "Copied first draft summary text"
    save_first_draft_summary(first_draft_summary)
