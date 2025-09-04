from crewai import Agent
from config import Config

class VoiceAssistantAgent:
    def __init__(self, groq_api_key: str):
        # CrewAI uses litellm under the hood; specify provider via model="groq/<model>"
        self.agent = Agent(
            role='Voice Assistant',
            goal='Provide helpful responses to user voice queries and ensure proper logging',
            backstory='''You are a friendly and helpful voice assistant designed to interact with users 
            through speech. You excel at understanding user queries, providing accurate information, 
            and maintaining conversation context. You always ensure that user interactions are logged 
            properly for quality assurance and improvement purposes.''',
            verbose=True,
            allow_delegation=False,
            model=f"gemini/{Config.GEMINI_MODEL}",
            api_key=Config.GEMINI_API_KEY,
        )

class LoggerAgent:
    def __init__(self):
        self.agent = Agent(
            role='Query Logger',
            goal='Accurately log all user queries and system responses',
            backstory='''You are responsible for maintaining detailed logs of all user interactions. 
            Your job is to ensure that every query is properly recorded with timestamps and context 
            for analysis and improvement of the voice assistant system.''',
            verbose=True,
            allow_delegation=False
        )