import json


json_files = ["A:\\College\Orpheus-AI-\\dataset\Subtitle Database\\Contigo en el futuro 2025 1080p WEBRip x264 AAC5.1 [YTS.MX]_subtitles.json",
              "A:\College\Orpheus-AI-\\dataset\Subtitle Database\\Edens Zero 2nd Season - Subtitles_subtitles.json",
              "A:\College\Orpheus-AI-\\dataset\Subtitle Database\\Ladykillers (2004) sub_subtitles.json",
              "A:\College\Orpheus-AI-\\dataset\Subtitle Database\\Perfect match sub_subtitles.json",
              "A:\College\Orpheus-AI-\\dataset\Subtitle Database\\Personal database.json",
              "A:\College\Orpheus-AI-\\dataset\Subtitle Database\\Titanic (1997).DVD.NonHI.pcc.en.PRMNT_subtitles.json"]

formatted_data = []

for json_file in json_files:
    with open(json_file, "r") as f:
        data = json.load(f)

    for pair in data:
        formatted_data.append({
            "messages": [
                {"role": "system", "content": "You are a chatbot with a specific personality."},
                {"role": "user", "content": pair["Input"]},
                {"role": "assistant", "content": pair["Output"]}
            ]
        })

with open("training_data.jsonl", "w") as f:
    for entry in formatted_data:
        f.write(json.dumps(entry) + "\n")
