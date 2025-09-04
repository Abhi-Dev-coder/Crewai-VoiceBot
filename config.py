import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = 'llama-3.1-8b-instant'
    
    # Gemini (Google) LLM Settings
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = 'gemini-1.5-flash'
    
    # Speech Recognition Settings
    SPEECH_RECOGNITION_TIMEOUT = 5
    SPEECH_RECOGNITION_PHRASE_TIMEOUT = 1
    
    # Text-to-Speech Settings
    TTS_RATE = 200
    TTS_VOLUME = 0.9
    
    # JSON Logging
    LOG_FILE_PATH = 'logs/user_queries.json'
    
    # Flask Settings
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    FLASK_DEBUG = True