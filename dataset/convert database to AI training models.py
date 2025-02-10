import json

files = [
    r"A:\College\Orpheus-AI-\dataset\Subtitle Database\Contigo en el futuro 2025 1080p WEBRip x264 AAC5.1 [YTS.MX]_subtitles.json",
    r"A:\College\Orpheus-AI-\dataset\Subtitle Database\Edens Zero 2nd Season - Subtitles_subtitles.json",
    r"A:\College\Orpheus-AI-\dataset\Subtitle Database\Perfect match sub_subtitles.json",
    r"A:\College\Orpheus-AI-\dataset\Subtitle Database\personal database.json",
    r"A:\College\Orpheus-AI-\dataset\Subtitle Database\Titanic (1997).DVD.NonHI.pcc.en.PRMNT_subtitles.json"
]

combined_data = []

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        for item in data:
            combined_data.append({
                "Input": item.get("Input"),
                "Output": item.get("Output")
            })

output_file_path = r"A:\College\Orpheus-AI-\dataset\Training data\combined_data.json"


with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(combined_data, output_file, ensure_ascii=False, indent=4)

print(f"Data successfully combined and saved to {output_file_path}")

