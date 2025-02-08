import re
import json
import os


def ass_file_format(path):
    return path.endswith('.ass')

def subtitle_file_format(path):
    return path.endswith('.srt') or path.endswith('.vtt')

def clean_subtitle_text(path, text):
    """ Clean subtitles to get clear text """

    # Handle .ass file cleaning
    if ass_file_format(path):
        cleaned_text = re.sub(r'\\[a-zA-Z0-9]+', '', text)  # Remove styles
        cleaned_text = re.sub(r'{\\[a-zA-Z0-9]+}', '', cleaned_text)  # Remove styles
        cleaned_text = cleaned_text.replace('\\N', ' ')  # Handle line breaks
        cleaned_text = re.sub(r'^\d+\)', '', cleaned_text)  # Remove numbered dialogue
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,!?\'"]', '', cleaned_text)  # Remove unwanted characters
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Clean extra spaces
        return cleaned_text
    else:
        return text.strip()


# Get subtitles from either .ass, .srt, or .vtt file
def get_subtitles(path):
    """ Get subtitles from file and clean them """
    sub = []

    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        if ass_file_format(path):
            for line in lines:
                stripped_line = line.strip()
                if stripped_line.startswith("Dialogue"):
                    content = stripped_line.split(",")
                    dialogue = content[10]  # .ass specific
                    cleaned_dialogue = clean_subtitle_text(path, dialogue)
                    sub.append(cleaned_dialogue)

        elif subtitle_file_format(path):
            for line in lines:
                stripped_line = line.strip()
                if stripped_line and not stripped_line[0].isdigit() and "-->" not in stripped_line:
                    cleaned_dialogue = clean_subtitle_text(path, stripped_line)
                    sub.append(cleaned_dialogue)
    return sub

def save_subtitles_as_json(input_filename, output_dir):
    # Remove the extension from input_filename and add .json
    base_filename = os.path.splitext(os.path.basename(input_filename))[0]
    output_filename = os.path.join(output_dir, f"{base_filename}_subtitles.json")

    # Assuming you have the subtitles data gathered in subtitles_data
    subtitles_data = get_subtitles(input_filename)

    # Ensure the directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write the subtitles data as JSON
    with open(output_filename, "w", encoding="utf-8") as json_file:
        json.dump(subtitles_data, json_file, ensure_ascii=False, indent=4)

    print(f"Subtitles saved to {output_filename}")



# Save subtitles in different files
save_subtitles_as_json("A:\\College\\Orpheus-AI-\\dataset\\movie subtitles\\Titanic (1997).DVD.NonHI.pcc.en.PRMNT.ass",
              "A:\\College\\Orpheus-AI-\\dataset\\movie subtitles")
