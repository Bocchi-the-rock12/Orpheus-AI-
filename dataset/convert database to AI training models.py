import json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot(
    'ChatBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///A:/College/Orpheus-AI-/dataset/Training data/chatbot_database.db',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
    ]
)

trainer = ChatterBotCorpusTrainer(chatbot)

# Load your own custom data
with open('A:/College/Orpheus-AI-/dataset/Training data/combined_data.json') as json_file:
    training_data = json.load(json_file)
    for entry in training_data:
        chatbot.train([entry])  # Train each entry (a dictionary with 'Input' and 'Output' keys)


