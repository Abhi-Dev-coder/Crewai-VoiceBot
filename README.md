---
title: VoiceBot CrewAI Assistant
emoji: 🎤
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
---

# 🎤 VoiceBot CrewAI Assistant

A conversational AI assistant built with CrewAI architecture and powered by Groq LLM.

## Features

- 💬 **Real-time Chat**: Interactive conversation interface
- 🎤 **Voice Input**: Support for voice-to-text (browser-based)
- 🧠 **Smart Responses**: Powered by Groq's fast LLM
- 📝 **Conversation Logs**: Track and analyze interactions
- 🎨 **Modern UI**: Clean, responsive Gradio interface

## How to Use

1. **Text Chat**: Type your message and press Enter or click Send
2. **Voice Input**: Click the microphone button to record voice (requires microphone permission)
3. **Examples**: Try the example queries to get started

## Technology Stack

- **Frontend**: Gradio
- **LLM**: Groq (Llama 3.1 8B Instant)
- **Architecture**: CrewAI-inspired design
- **Hosting**: Hugging Face Spaces

## Setup

To run locally:

1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Set environment variable: `GROQ_API_KEY=your_api_key`
4. Run: `python app.py`

## Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)

## License

MIT License