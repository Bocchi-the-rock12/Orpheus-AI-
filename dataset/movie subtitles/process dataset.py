import re


def ass_file_format(path):
    if path.endswith('.ass'):
        return True
    else:
        return False


def clean_subtitle_text(path, text):
    """ Clean subtitles to get clear text """

    # Cleans subtitles in case of file type being ass
    if ass_file_format(path):
        cleaned_text = re.sub(r'\\[a-zA-Z0-9]+', '', text)
        cleaned_text = re.sub(r'{\\[a-zA-Z0-9]+}', '', cleaned_text)
        cleaned_text = cleaned_text.replace('\\N', ' ')
        cleaned_text = re.sub(r'^\d+\)', '', cleaned_text)
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,!?\'"]', '', cleaned_text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        return cleaned_text
    else:
        return

def get_subtitles(path):
    """ Gets subtitles from file """
    sub = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped_line = line.strip()
            if stripped_line and stripped_line.split()[0].startswith("Dialogue"):
                # Checks file type
                if ass_file_format(path):
                    content = stripped_line.split(",")
                    dialogue = content[10]
                    cleaned_dialogue = clean_subtitle_text(path, dialogue)
                    sub.append(cleaned_dialogue)
                else:
                    content = stripped_line.split(",")
                    dialogue = content[10]
                    sub.append(dialogue)