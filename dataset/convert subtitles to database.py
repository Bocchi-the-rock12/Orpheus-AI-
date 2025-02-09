import json
import re


def load_subtitles(file_path):
    """Load subtitle JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def remove_sound_effects(text):
    """Removes sound effects enclosed in () or (( )) and unnecessary labels."""

    # Remove text inside double parentheses ((...))
    text = re.sub(r'\(\(.*?\)\)', '', text)

    # Remove text inside single parentheses (...)
    text = re.sub(r'\(.*?\)', '', text)

    # Remove labels like "Input:", "Output:"
    text = re.sub(r'^(Input:|Output:)\s*', '', text)

    # Fix multiple spaces and trim
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def clean_subtitles(sub):
    """Cleans up subtitle entries in JSON by removing sound effects."""

    cleaned_sub = []

    for entry in sub:
        cleaned_input = remove_sound_effects(entry["Input"])
        cleaned_output = remove_sound_effects(entry["Output"])

        if cleaned_input and cleaned_output:
            cleaned_sub.append({
                "Input": cleaned_input,
                "Output": cleaned_output
            })

    return cleaned_sub

def save_fixed_subtitles(subs, output):
    """Save cleaned subtitles to a new JSON file."""
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(subs, f, indent=4, ensure_ascii=False)