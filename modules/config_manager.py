import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

SALT = config['Security']['SALT']
OPENAI_API_KEY = config['OpenAI']['API_KEY']