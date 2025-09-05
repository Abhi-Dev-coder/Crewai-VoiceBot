import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = 'llama-3.1-8b-instant'
    
    # Speech Recognition Settings
    SPEECH_RECOGNITION_TIMEOUT = 5
    SPEECH_RECOGNITION_PHRASE_TIMEOUT = 1
    
    # Text-to-Speech Settings
    TTS_RATE = 200
    TTS_VOLUME = 0.9
    
    # JSON Logging (absolute path to project logs)
    LOG_FILE_PATH = os.path.join(BASE_DIR, 'logs', 'user_queries.json')
    
    # Flask Settings
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('PORT', os.getenv('FLASK_PORT', 5000)))
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

# Ensure no OpenAI fallback
if 'OPENAI_API_KEY' in os.environ:
    del os.environ['OPENAI_API_KEY']