from config import Config
from agents.voice_assistant import VoiceAssistantAgent
from tools.json_logger import JSONLoggerTool
from tasks.voice_tasks import create_voice_response_task
from crewai import Crew

def test_voicebot():
    if not Config.GROQ_API_KEY:
        print("❌ GROQ_API_KEY not found in environment!")
        return
    
    print("🚀 Testing VoiceBot with Groq...")
    
    try:
        # Initialize components
        assistant = VoiceAssistantAgent(Config.GROQ_API_KEY)
        logger_tool = JSONLoggerTool()
        
        # Create a simple test query
        test_query = "What is the weather like today?"
        
        # Create task
        task = create_voice_response_task(
            assistant.agent,
            [logger_tool],
            test_query
        )
        
        # Create crew and run
        crew = Crew(
            agents=[assistant.agent],
            tasks=[task],
            verbose=True
        )
        
        print(f"📝 Processing query: {test_query}")
        result = crew.kickoff()
        
        print(f"✅ Response: {result}")
        
        # Log the interaction
        logger_tool._run(
            query=test_query,
            response=str(result),
            query_type="test_interaction"
        )
        
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_voicebot()