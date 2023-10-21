import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

OPENAI_API_KEY = config['OpenAI']['API_KEY']