from flask import Flask, render_template, request, jsonify, session
import asyncio
import json
import uuid
from datetime import datetime
import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import VoiceBot
from config import Config

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Global VoiceBot instance
voicebot = None

def init_voicebot():
    global voicebot
    if voicebot is None:
        try:
            print("Initializing VoiceBot...")
            # Import here to ensure Config class is properly loaded
            from main import VoiceBot
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
        
        # Process the text query (simulating voice input)
        try:
            # Generate response using CrewAI
            from tasks.voice_tasks import create_voice_response_task
            
            response_task = create_voice_response_task(
                bot.voice_assistant.agent,
                [bot.json_logger],
                user_text
            )
            
            # Update crew with the task and execute
            bot.crew.tasks = [response_task]
            crew_result = bot.crew.kickoff()
            assistant_response = str(crew_result)
            
            # Log the interaction
            bot.json_logger._run(
                query=user_text,
                response=assistant_response,
                query_type="web_voice_interaction"
            )
            
            return jsonify({
                'success': True,
                'user_query': user_text,
                'assistant_response': assistant_response,
                'timestamp': datetime.now().isoformat(),
                'session_id': session['session_id']
            })
            
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            return jsonify({'error': error_msg}), 500
            
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
    # Check configuration
    if not Config.GROQ_API_KEY:
        print("Error: GROQ_API_KEY environment variable not set!")
        exit(1)
    
    print("Starting VoiceBot Web Application...")
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)