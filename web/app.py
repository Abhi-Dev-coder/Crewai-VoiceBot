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
        
        # Process the text query using direct method with session memory
        result = bot.process_text_query(user_text, session_id=session['session_id'])
        
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
        
        # If session exists, prefer session-scoped logs; else fall back to recent logs
        if 'session_id' in session:
            recent_logs = bot.json_logger.get_session_logs(session['session_id'], limit=20)
        else:
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

@app.route('/api/get-history')
def get_history():
    try:
        bot = init_voicebot()
        if bot is None:
            return jsonify({'error': 'VoiceBot not initialized'}), 500
        if 'session_id' not in session:
            return jsonify({'success': True, 'history': []})
        history = bot._get_history(session['session_id'])
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'error': f'Error retrieving history: {str(e)}'}), 500

if __name__ == '__main__':
    if not Config.GROQ_API_KEY:
        print("Error: GROQ_API_KEY environment variable not set!")
        exit(1)
    
    print("Starting VoiceBot Web Application...")
    app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)