import os
from dotenv import load_dotenv
from groq import Groq

# Test 1: Basic Groq API
def test_groq_api():
    load_dotenv()
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ GROQ_API_KEY not found!")
        return False
    
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Hello! Can you respond briefly?"}],
            max_tokens=50
        )
        print(f"✅ Groq API Test: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ Groq API Error: {e}")
        return False

# Test 2: CrewAI with Groq
def test_crewai_integration():
    try:
        from config import Config
        from agents.voice_assistant import VoiceAssistantAgent
        
        if not Config.GROQ_API_KEY:
            print("❌ Config API key missing!")
            return False
        
        # Create agent
        assistant = VoiceAssistantAgent(Config.GROQ_API_KEY)
        print("✅ CrewAI Agent created successfully!")
        
        # Test the LLM wrapper
        test_response = assistant.groq_llm.invoke("Say hello briefly")
        print(f"✅ Agent LLM Test: {test_response}")
        
        return True
        
    except Exception as e:
        print(f"❌ CrewAI Integration Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Testing Groq Integration ===")
    test1 = test_groq_api()
    if test1:
        test2 = test_crewai_integration()
        if test2:
            print("\\n✅ All tests passed! Your integration should work now.")
        else:
            print("\\n❌ CrewAI integration failed.")
    else:
        print("\\n❌ Basic Groq API test failed.")