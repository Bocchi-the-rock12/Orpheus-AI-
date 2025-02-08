import re
import json


def ass_file_format(path):
    """Check if the file is an .ass subtitle file."""
    return path.lower().endswith('.ass')

def clean_subtitle_text(path, text):
    """Clean subtitles by removing .ass formatting tags and unwanted characters."""
    if ass_file_format(path):
        cleaned_text = re.sub(r'\\[a-zA-Z0-9]+', '', text)
        cleaned_text = re.sub(r'{\\.*?}', '', cleaned_text)
        cleaned_text = cleaned_text.replace('\\N', ' ')
        cleaned_text = re.sub(r'^\d+\)', '', cleaned_text)
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,!?\'"-]', '', cleaned_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        return cleaned_text if cleaned_text else ""
    else:
        return text.strip()

def get_subtitles(path, output_path):
    """Extracts cleaned subtitles from an .ass file."""
    sub = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line.startswith("Dialogue:"):
                content = stripped_line.split(",", maxsplit=10)

                if len(content) > 10:
                    dialogue = content[10].strip()
                    cleaned_dialogue = clean_subtitle_text(path, dialogue)

                    if cleaned_dialogue:
                        sub.append(cleaned_dialogue)
                else:
                    print(f"Skipping line due to unexpected format: {line}")
    # Save subtitles to JSON
    output_file = r"A:\College\Orpheus-AI-\dataset\movie subtitles\Titanic_subtitles.json"
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(sub, json_file, ensure_ascii=False, indent=4)


# Save the subtitles in a file
get_subtitles("A:\\College\\Orpheus-AI-\\dataset\\movie subtitles\\Titanic (1997).DVD.NonHI.pcc.en.PRMNT.ass",
              "A:\\College\\Orpheus-AI-\\dataset\\movie subtitles")
