import asyncio
import json
from datetime import datetime
from agents.voice_assistant import VoiceAssistantAgent, LoggerAgent
from tools.speech_tools import SpeechRecognitionTool, TextToSpeechTool
from tools.json_logger import JSONLoggerTool
from config import Config

class VoiceBot:
    def __init__(self, init_audio: bool = True):
        self.config = Config
        # Simple in-memory conversation history per session_id
        self.session_histories: dict[str, list[dict]] = {}
        
        # Initialize tools (audio tools optional for web environments)
        if init_audio:
            try:
                self.speech_recognition = SpeechRecognitionTool()
            except Exception as e:
                print(f"Warning: Failed to initialize microphone: {e}")
                self.speech_recognition = None
            try:
                self.text_to_speech = TextToSpeechTool()
            except Exception as e:
                print(f"Warning: Failed to initialize text-to-speech: {e}")
                self.text_to_speech = None
        else:
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
    
    async def process_voice_interaction(self):
        """Main interaction loop for voice input"""
        print("VoiceBot is ready! Say something...")
        
        try:
            # 1. Capture voice input
            if not self.speech_recognition:
                raise RuntimeError("SpeechRecognitionTool not initialized.")
            
            user_query = self.speech_recognition._run()
            
            if "Could not understand" in user_query or "Error" in user_query:
                error_response = "I'm sorry, I couldn't understand. Please try again."
                if self.text_to_speech:
                    self.text_to_speech._run(error_response)
                return {"error": "Speech recognition failed"}
            
            # 2. Process the query
            result = self.process_text_query(user_query)
            
            if result["success"]:
                # 3. Speak the response
                if self.text_to_speech:
                    self.text_to_speech._run(result["assistant_response"])
            
            return result
            
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            print(error_msg)
            if self.text_to_speech:
                self.text_to_speech._run("I encountered an error. Please try again.")
            return {"error": error_msg}

def main():
    if not Config.GROQ_API_KEY:
        print("Error: GROQ_API_KEY environment variable not set!")
        return
    
    # Test text processing
    voicebot = VoiceBot(init_audio=False)
    
    # Test with a simple query
    test_query = "Hello, how are you today?"
    result = voicebot.process_text_query(test_query)
    
    if result["success"]:
        print(f"✅ Success! Response: {result['assistant_response']}")
    else:
        print(f"❌ Failed: {result['error']}")

if __name__ == "__main__":
    main()