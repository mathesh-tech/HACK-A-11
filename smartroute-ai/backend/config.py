import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-prod')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
