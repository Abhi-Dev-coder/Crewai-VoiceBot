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
'''
# Simple test script to verify the fix

# test_direct.py - Test the direct approach

# from config import Config
# from agents.voice_assistant import VoiceAssistantAgent
# from tools.json_logger import JSONLoggerTool

# def test_direct_approach():
#     if not Config.GROQ_API_KEY:
#         print("❌ GROQ_API_KEY not found!")
#         return
    
    # print("🚀 Testing Direct Groq Approach (No CrewAI tasks)...")
    
    # try:
    #     # Initialize without CrewAI crew
    #     assistant = VoiceAssistantAgent(Config.GROQ_API_KEY)
    #     logger = JSONLoggerTool()
        
    #     # Test direct processing
    #     test_query = "What are your store hours?"
    #     print(f"📝 Query: {test_query}")
        
    #     # Use direct method (bypasses CrewAI completely)
    #     response = assistant.process_query(test_query)
    #     print(f"✅ Response: {response}")
        
    #     # Log the interaction
    #     logger._run(
    #         query=test_query,
    #         response=response,
    #         query_type="direct_test"
    #     )
        
    #     print("✅ Test completed successfully - NO CrewAI tasks used!")
        
    # except Exception as e:
    #     print(f"❌ Test failed: {e}")
    #     import traceback
    #     traceback.print_exc()

if __name__ == "__main__":
    test_direct_approach()
'''