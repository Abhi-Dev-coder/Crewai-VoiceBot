import asyncio
import json
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.voice_assistant import VoiceAssistantAgent, LoggerAgent
from tools.json_logger import JSONLoggerTool
from config import Config

class VoiceBotWeb:
    def __init__(self):
        self.config = Config
        # Simple in-memory conversation history per session_id
        self.session_histories: dict[str, list[dict]] = {}
        
        # No audio tools for web deployment
        self.speech_recognition = None
        self.text_to_speech = None
        
        self.json_logger = JSONLoggerTool(self.config.LOG_FILE_PATH)
        
        # Initialize agents WITHOUT CrewAI crew system
        self.voice_assistant = VoiceAssistantAgent(self.config.GROQ_API_KEY)
        self.logger_agent = LoggerAgent(self.config.GROQ_API_KEY)
    
    def _get_history(self, session_id: str) -> list:
        return self.session_histories.get(session_id, [])

    def _append_history(self, session_id: str, query: str, response: str):
        history = self.session_histories.setdefault(session_id, [])
        history.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response
        })
        # keep last N to bound memory
        if len(history) > 50:
            self.session_histories[session_id] = history[-50:]

    def process_text_query(self, query: str, session_id: str | None = None) -> dict:
        """Process text query without using CrewAI tasks"""
        try:
            print(f"Processing query: {query}")
            
            # Prepare contextual history if available
            history = self._get_history(session_id) if session_id else []
            
            # Generate response using direct Groq client with context
            assistant_response = self.voice_assistant.process_query(query, history=history)
            
            print(f"Generated response: {assistant_response}")
            
            # Log the interaction
            self.json_logger._run(
                query=query,
                response=assistant_response,
                query_type="direct_interaction",
                session_id=session_id
            )
            
            # Update in-memory history
            if session_id:
                self._append_history(session_id, query, assistant_response)
            
            return {
                "success": True,
                "user_query": query,
                "assistant_response": assistant_response,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            print(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
