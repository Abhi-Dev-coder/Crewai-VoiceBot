import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Test Groq API directly
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    print("❌ No GROQ_API_KEY found!")
    exit(1)

print(f"✅ API Key found: {api_key[:10]}...")

try:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Hello! Say hi back briefly."}],
        max_tokens=50
    )
    print(f"✅ Groq works: {response.choices[0].message.content}")
    
    # Test CrewAI integration
    from agents.voice_assistant import VoiceAssistantAgent
    assistant = VoiceAssistantAgent(api_key)
    test_response = assistant.groq_llm.invoke("Say hello briefly")
    print(f"✅ CrewAI integration works: {test_response}")
    
except Exception as e:
    print(f"❌ Error: {e}")