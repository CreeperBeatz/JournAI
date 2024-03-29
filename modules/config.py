import yaml
from yaml.loader import SafeLoader
import os

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

PAGE_CONFIG = {"page_title": "JournAI", "page_icon": "logo.png"}
CHATS_FOLDER = "chats"
