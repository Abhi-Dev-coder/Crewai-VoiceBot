from flask import Flask, render_template, request, jsonify, session
import uuid
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import VoiceBot
from config import Config

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Global VoiceBot instance
voicebot = None

def init_voicebot():
    global voicebot
    if voicebot is None:
        try:
            print("Initializing VoiceBot...")
            voicebot = VoiceBot(init_audio=False)
            print("VoiceBot initialized successfully")
        except Exception as e:
            print(f"Error initializing VoiceBot: {e}")
            import traceback
            traceback.print_exc()
            return None
    return voicebot

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process-voice', methods=['POST'])
def process_voice():
    try:
        data = request.get_json()
        user_text = data.get('text', '').strip()
        
        if not user_text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Initialize session ID if not exists
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        # Get or initialize VoiceBot
        bot = init_voicebot()
        if bot is None:
            return jsonify({'error': 'VoiceBot initialization failed'}), 500
        
        # Process the text query using direct method (NO CrewAI tasks)
        result = bot.process_text_query(user_text)
        
        if result["success"]:
            result['session_id'] = session['session_id']
            return jsonify(result)
        else:
            return jsonify({'error': result.get('error', 'Unknown error')}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/get-logs')
def get_logs():
    try:
        bot = init_voicebot()
        if bot is None:
            return jsonify({'error': 'VoiceBot not initialized'}), 500
        
        recent_logs = bot.json_logger.get_recent_logs(limit=20)
        return jsonify({
            'success': True,
            'logs': recent_logs
        })
    except Exception as e:
        return jsonify({'error': f'Error retrieving logs: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'voicebot_initialized': voicebot is not None,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    if not Config.GROQ_API_KEY:
        print("Error: GROQ_API_KEY environment variable not set!")
        exit(1)
    
    print("Starting VoiceBot Web Application...")
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)
'''

# Simple test script to verify the fix
test_direct = '''
# test_direct.py - Test the direct approach

from config import Config
from agents.voice_assistant import VoiceAssistantAgent
from tools.json_logger import JSONLoggerTool

def test_direct_approach():
    if not Config.GROQ_API_KEY:
        print("❌ GROQ_API_KEY not found!")
        return
    
    print("🚀 Testing Direct Groq Approach (No CrewAI tasks)...")
    
    try:
        # Initialize without CrewAI crew
        assistant = VoiceAssistantAgent(Config.GROQ_API_KEY)
        logger = JSONLoggerTool()
        
        # Test direct processing
        test_query = "What are your store hours?"
        print(f"📝 Query: {test_query}")
        
        # Use direct method (bypasses CrewAI completely)
        response = assistant.process_query(test_query)
        print(f"✅ Response: {response}")
        
        # Log the interaction
        logger._run(
            query=test_query,
            response=response,
            query_type="direct_test"
        )
        
        print("✅ Test completed successfully - NO CrewAI tasks used!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_approach()