import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

OPENAI_API_KEY = config['OpenAI']['API_KEY']

# Global params
PAGE_CONFIG = {"page_title": "JournAI",
               "page_icon": "logo.png"}
