import speech_recognition as sr
import pyttsx3
import asyncio
from typing import Optional, Any
from crewai.tools import BaseTool

class SpeechRecognitionTool(BaseTool):
    name: str = "Speech Recognition Tool"
    description: str = "Converts speech to text using Google Speech Recognition API"
    recognizer: Any = None
    microphone: Any = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        
        # List available microphones and select the first one
        mic_names = sr.Microphone.list_microphone_names()
        if not mic_names:
            raise Exception("No microphones found")
            
        print(f"Available microphones: {mic_names}")
        # Use the first microphone in the list (index 0)
        self.microphone = sr.Microphone(device_index=0)
        
        # Adjust for ambient noise
        try:
            with self.microphone as source:
                print("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source)
                print("Ambient noise adjustment complete")
        except Exception as e:
            print(f"Error during ambient noise adjustment: {e}")
            raise
    
    def _run(self, audio_data: Optional[Any] = None) -> str:
        try:
            if audio_data is None:
                # Record audio from microphone
                try:
                    with self.microphone as source:
                        print("Listening...")
                        print("Please speak now...")
                        # Increase timeout to give more time for speech input
                        audio_data = self.recognizer.listen(
                            source, 
                            timeout=10,  # Increased from 5 to 10 seconds
                            phrase_time_limit=15  # Increased from 10 to 15 seconds
                        )
                        print("Audio captured successfully")
                except Exception as e:
                    print(f"Error capturing audio: {e}")
                    return f"Error capturing audio: {e}"
            
            # Convert speech to text
            try:
                text = self.recognizer.recognize_google(audio_data)
                print(f"Recognized: {text}")
                return text
            except sr.UnknownValueError:
                print("Could not understand audio - no speech detected")
                return "Could not understand audio - no speech detected"
            except sr.RequestError as e:
                print(f"Error with speech recognition service: {e}")
                return f"Error with speech recognition service: {e}"
            
        except sr.WaitTimeoutError:
            print("Listening timeout - no speech detected")
            return "Listening timeout - no speech detected"
        except Exception as e:
            print(f"Unexpected error in speech recognition: {e}")
            return f"Unexpected error in speech recognition: {e}"

class TextToSpeechTool(BaseTool):
    name: str = "Text to Speech Tool"
    description: str = "Converts text to speech using pyttsx3"
    engine: Any = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def __init__(self):
        super().__init__()
        self.engine = pyttsx3.init()
        
        # Configure TTS settings
        voices = self.engine.getProperty('voices')
        if voices:
            # Use female voice if available
            for voice in voices:
                if 'female' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        
        self.engine.setProperty('rate', 200)
        self.engine.setProperty('volume', 0.9)
    
    def _run(self, text: str) -> str:
        try:
            print(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
            return f"Successfully spoke: {text}"
        except Exception as e:
            return f"Error in text-to-speech: {e}"