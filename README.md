# 🎤 VoiceBot Assistant

A sophisticated AI-powered voice assistant built with Python that supports both voice and text interactions. The project features a dual-mode architecture: a desktop application with full voice capabilities and a web application optimized for serverless deployment.

## 🌟 Features

### Core Capabilities
- **Voice Recognition**: Real-time speech-to-text using Google Speech Recognition API
- **Text-to-Speech**: Natural voice responses using pyttsx3
- **AI-Powered Responses**: Powered by Groq's Llama 3.1 model for intelligent conversations
- **Session Management**: Maintains conversation history and context
- **Dual Interface**: Both desktop and web interfaces available

### Web Application Features
- **Serverless Ready**: Optimized for Vercel deployment
- **RESTful API**: Clean API endpoints for integration
- **Real-time Chat**: Modern web interface with voice and text input
- **Session Persistence**: Maintains conversation history across sessions
- **Logging System**: Comprehensive interaction logging

## 🛠️ Technologies Used

### Backend Technologies
- **Python 3.9+**: Core programming language
- **Groq API**: AI language model provider (Llama 3.1-8b-instant)
- **CrewAI**: Agent framework for AI orchestration
- **Flask**: Web framework for the web application
- **SpeechRecognition**: Google Speech Recognition API integration
- **pyttsx3**: Text-to-speech engine
- **python-dotenv**: Environment variable management

### Frontend Technologies
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript (ES6+)**: Interactive functionality
- **Web Speech API**: Browser-based speech recognition
- **Font Awesome**: Icon library
- **Responsive Design**: Mobile-friendly interface

### Development & Deployment
- **Vercel**: Serverless deployment platform
- **Git**: Version control
- **JSON**: Data logging and storage
- **RESTful APIs**: Clean API design

## 📁 Project Structure

```
voicebot_project/
├── agents/                 # AI agent implementations
│   ├── voice_assistant.py  # Main voice assistant agent
│   └── __init__.py
├── tools/                  # Utility tools and services
│   ├── speech_tools.py     # Speech recognition & TTS
│   ├── json_logger.py      # Logging system
│   └── __init__.py
├── tasks/                  # CrewAI task definitions
│   ├── voice_tasks.py      # Voice interaction tasks
│   └── __init__.py
├── web/                    # Web application
│   ├── app.py             # Flask web server
│   ├── voicebot_web.py     # Web-optimized VoiceBot
│   ├── templates/         # HTML templates
│   │   └── index.html     # Main web interface
│   ├── static/            # Static assets
│   │   ├── style.css      # Styling
│   │   └── script.js      # Frontend JavaScript
│   └── logs/              # Web application logs
├── logs/                   # Application logs
│   └── user_queries.json  # Interaction history
├── test/                   # Test files
├── config.py              # Configuration settings
├── main.py                # Desktop application entry point
├── requirements.txt       # Python dependencies
└── vercel.json           # Vercel deployment config
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Microphone (for voice features)
- Groq API key ([Get one here](https://console.groq.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd voicebot_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

### Running the Application

#### Desktop Version (Full Voice Features)
```bash
python main.py
```

#### Web Version (Text + Browser Voice)
```bash
cd web
python app.py
```
Then visit `http://localhost:5000`

## 🌐 Web Deployment (Vercel)

### Prerequisites
- Vercel account
- Groq API key

### Deployment Steps

1. **Connect Repository**
   - Import your project to Vercel
   - Select the `web` folder as the root directory

2. **Set Environment Variables**
   In Vercel dashboard, add:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   FLASK_DEBUG=false
   ```

3. **Deploy**
   - Vercel will automatically detect the Python configuration
   - The web version excludes audio dependencies for serverless compatibility

### Web API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/api/process-voice` | POST | Process text/voice queries |
| `/api/get-logs` | GET | Retrieve conversation logs |
| `/api/get-history` | GET | Get session conversation history |
| `/api/health` | GET | Health check endpoint |

## 🔧 Configuration

### Environment Variables
```bash
GROQ_API_KEY=your_groq_api_key_here    # Required: Groq API key
FLASK_HOST=0.0.0.0                     # Optional: Flask host
FLASK_PORT=5000                        # Optional: Flask port
FLASK_DEBUG=true                       # Optional: Debug mode
```

### Customization Options
- **AI Model**: Change model in `agents/voice_assistant.py`
- **Speech Settings**: Modify `tools/speech_tools.py`
- **UI Styling**: Update `web/static/style.css`
- **Logging**: Configure in `tools/json_logger.py`

## 📱 Usage Examples

### Desktop Application
```python
from main import VoiceBot

# Initialize with voice capabilities
voicebot = VoiceBot(init_audio=True)

# Process voice input
result = await voicebot.process_voice_interaction()
print(result['assistant_response'])
```

### Web API Usage
```javascript
// Send text query
fetch('/api/process-voice', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: 'Hello, how are you?' })
})
.then(response => response.json())
.then(data => console.log(data.assistant_response));
```

## 🧪 Testing

### Run Tests
```bash
cd test
python test_integration.py
```

### Test Components
- **Voice Recognition**: Test microphone input
- **AI Responses**: Verify Groq API integration
- **Web Interface**: Test all API endpoints
- **Logging**: Check interaction logging

## 🐛 Troubleshooting

### Common Issues

1. **Microphone Not Working**
   - Check microphone permissions
   - Verify audio drivers are installed
   - Test with system audio settings

2. **Groq API Errors**
   - Verify API key is correct
   - Check API quota limits
   - Ensure internet connection

3. **Web Deployment Issues**
   - Check environment variables in Vercel
   - Verify Python version compatibility
   - Review build logs for errors

4. **Audio Dependencies**
   - For web deployment, audio tools are automatically excluded
   - Desktop version requires proper audio system setup

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq**: For providing fast AI inference
- **CrewAI**: For the agent framework
- **Google**: For speech recognition services
- **Flask**: For the web framework
- **Vercel**: For serverless deployment platform

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation

---

**Made with ❤️ using Python, AI, and modern web technologies**
