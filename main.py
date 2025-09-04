import asyncio
import json
from datetime import datetime
from crewai import Crew
from agents.voice_assistant import VoiceAssistantAgent, LoggerAgent
from tasks.voice_tasks import create_voice_response_task, create_logging_task
from tools.speech_tools import SpeechRecognitionTool, TextToSpeechTool
from tools.json_logger import JSONLoggerTool
from config import Config

class VoiceBot:
    def __init__(self, init_audio: bool = True):
        # Use global Config (module-level class with attributes)
        self.config = Config
        
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
        
        # Initialize agents
        self.voice_assistant = VoiceAssistantAgent(self.config.GROQ_API_KEY)
        self.logger_agent = LoggerAgent()
        
        # Create crew
        self.crew = Crew(
            agents=[self.voice_assistant.agent, self.logger_agent.agent],
            tasks=[],  # We'll add tasks dynamically
            verbose=True
        )
    
    async def process_voice_interaction(self):
        """Main interaction loop"""
        print("VoiceBot is ready! Say something...")
        
        try:
            # 1. Capture voice input
            print("Listening for voice input...")
            if not self.speech_recognition:
                raise RuntimeError("SpeechRecognitionTool not initialized. Use web endpoint or enable init_audio.")
            user_query = self.speech_recognition._run()
            
            if "Could not understand" in user_query or "Error" in user_query or "no speech detected" in user_query.lower():
                print(f"Voice input error: {user_query}")
                error_response = "I'm sorry, I couldn't understand what you said. Please try again."
                if self.text_to_speech:
                    self.text_to_speech._run(error_response)
                return
            
            print(f"User said: {user_query}")
            
            # 2. Generate response using CrewAI
            response_task = create_voice_response_task(
                self.voice_assistant.agent,
                [self.json_logger],
                user_query
            )
            
            # Update crew with the task and execute
            self.crew.tasks = [response_task]
            crew_result = self.crew.kickoff()
            assistant_response = str(crew_result)
            
            print(f"Assistant response: {assistant_response}")
            
            # 3. Log the interaction
            self.json_logger._run(
                query=user_query,
                response=assistant_response,
                query_type="voice_interaction"
            )
            
            # 4. Speak the response
            if self.text_to_speech:
                self.text_to_speech._run(assistant_response)
            
            return {
                "user_query": user_query,
                "assistant_response": assistant_response,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            print(error_msg)
            if self.text_to_speech:
                self.text_to_speech._run("I'm sorry, I encountered an error. Please try again.")
            return {"error": error_msg}
    
    def run_continuous(self):
        """Run the voice bot continuously"""
        print("Starting VoiceBot in continuous mode...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                result = asyncio.run(self.process_voice_interaction())
                if result and "error" not in result:
                    print(f"Interaction completed successfully at {result['timestamp']}")
                
                # Small delay between interactions
                asyncio.run(asyncio.sleep(2))
                
        except KeyboardInterrupt:
            print("\nVoiceBot stopped by user.")
        except Exception as e:
            print(f"Fatal error: {e}")

def main():
    # Check if GROQ_API_KEY is set
    if not Config.GROQ_API_KEY:
        print("Error: GROQ_API_KEY environment variable not set!")
        print("Please set your Groq API key in a .env file or environment variable.")
        return
    
    # Initialize and run VoiceBot
    voicebot = VoiceBot()
    voicebot.run_continuous()

if __name__ == "__main__":
    main()

    