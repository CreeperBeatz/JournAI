import yaml
from yaml.loader import SafeLoader
import os

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

PAGE_CONFIG = {"page_title": "JournAI", "page_icon": "logo.png"}
CHATS_FOLDER = "persistent_storage/chats"
QUESTIONS_FOLDER = "persistent_storage/questions"
ANSWERS_FOLDER = "persistent_storage/answers"
VECTOR_FOLDER = "./persistent_storage/vectordb"
CHAT_MODEL = "gpt-3.5-turbo-1106"
EMBEDDING_MODEL = "text-embedding-3-small"

