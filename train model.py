import os
import subprocess

project_path = r"C:\Users\irmao\PycharmProjects\Orpheus-AI-2"
dataset_path = os.path.join(project_path, "dataset")
domain_path = os.path.join(dataset_path, "domain.yml")
nlu_path = os.path.join(dataset_path, "nlu.yml")
stories_path = os.path.join(dataset_path, "stories.yml")
config_path = os.path.join(dataset_path, "config.yml")

# Ask user for the output directory for the model
models_path = input("Enter the directory to save the trained model: ").strip()

# Create the directory if it does not exist
if not os.path.exists(models_path):
    os.makedirs(models_path)

os.chdir(project_path)

command = [
    "rasa", "train",
    "--domain", domain_path,
    "--data", nlu_path, stories_path,  # Separate paths for nlu and stories
    "--config", config_path,
    "--out", models_path
]

result = subprocess.run(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

if result.returncode != 0:
    print("Error during training:")
    print(result.stderr)
else:
    print("Training completed successfully!")
    print("Training process output:")
    print(result.stdout)
    print(result.stderr)


