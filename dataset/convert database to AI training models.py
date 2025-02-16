import yaml
import json

with open('A:\College\Orpheus-AI-\dataset\Subtitle Database\personal database.json', 'r') as file:
    json_data = json.load(file)

def generate_nlu_file(data):
    nlu_data = {
        "version": "2.0",
        "nlu": [
            {
                "intent": "custom_intent",
                "examples": "\n".join([f"- {entry['Input']}" for entry in data])
            }
        ]
    }
    with open("nlu.yml", "w") as file:
        yaml.dump(nlu_data, file, allow_unicode=True, default_flow_style=False)

# Função para gerar o arquivo domain.yml
def generate_domain_file():
    domain_data = {
        "version": "2.0",
        "intents": ["custom_intent"],
        "entities": [],
        "responses": {
            "utter_custom_intent": [
                {"text": "I'm here! How can I help you?"}
            ]
        },
        "actions": [],
        "slots": {}
    }
    with open("domain.yml", "w") as file:
        yaml.dump(domain_data, file, allow_unicode=True, default_flow_style=False)

# Função para gerar o arquivo stories.yml
def generate_stories_file():
    stories_data = {
        "version": "2.0",
        "stories": [
            {
                "story": "greet",
                "steps": [
                    {"intent": "custom_intent"},
                    {"action": "utter_custom_intent"}
                ]
            }
        ]
    }
    with open("stories.yml", "w") as file:
        yaml.dump(stories_data, file, allow_unicode=True, default_flow_style=False)

# Gerar os arquivos
generate_nlu_file(json_data)
generate_domain_file()
generate_stories_file()

print("Arquivos nlu.yml, domain.yml e stories.yml gerados com sucesso!")
