import subprocess
import sys
import os

def check_files_exist(files):
    missing_files = [file for file in files if not os.path.isfile(file)]
    if missing_files:
        print(f"The following required files are missing: {', '.join(missing_files)}")
        sys.exit(1)

def train_rasa_model():
    try:
        print("Starting Rasa model training...")

        # Define the base directory where your files are located
        base_dir = r"A:\College\Orpheus-AI-\dataset"

        # Define the paths to your configuration and data files
        config_file = os.path.join(base_dir, 'config.yml')
        domain_file = os.path.join(base_dir, 'domain.yml')
        data_dir = base_dir  # Assuming your NLU and stories files are also in this directory

        # Check if necessary files exist
        required_files = [
            config_file,
            domain_file,
            os.path.join(data_dir, 'nlu.yml'),
            os.path.join(data_dir, 'stories.yml')
            # Add rules.yml if you have it
            # os.path.join(data_dir, 'rules.yml')
        ]
        check_files_exist(required_files)

        # Ensure the 'models' directory exists
        os.makedirs('models', exist_ok=True)

        # Call the rasa train command with specific paths
        result = subprocess.run(
            [
                'rasa', 'train',
                '--config', config_file,
                '--domain', domain_file,
                '--data', data_dir
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("Rasa model training completed successfully.")
        # Uncomment the line below if you want to see the detailed output
        # print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("An error occurred during Rasa model training.")
        print("Return code:", e.returncode)
        print("Standard Output:", e.stdout)
        print("Error Output:", e.stderr)
        sys.exit(1)

if __name__ == '__main__':
    train_rasa_model()