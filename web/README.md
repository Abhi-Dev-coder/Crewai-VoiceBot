# VoiceBot Web Deployment

This is the web version of the VoiceBot, optimized for serverless deployment on Vercel.

## Key Changes for Web Deployment

1. **No Audio Dependencies**: Removed `speechrecognition` and `pyttsx3` dependencies that cause build issues on Vercel
2. **Text-Only Interface**: The web version processes text input only, no voice input/output
3. **Session Management**: Maintains conversation history per user session
4. **API Endpoints**: RESTful API for processing queries and retrieving logs

## Environment Variables

Set these in your Vercel dashboard:

- `GROQ_API_KEY`: Your Groq API key
- `FLASK_HOST`: `0.0.0.0` (default)
- `FLASK_PORT`: `5000` (default)
- `FLASK_DEBUG`: `false` (for production)

## API Endpoints

- `POST /api/process-voice`: Process text queries
- `GET /api/get-logs`: Retrieve conversation logs
- `GET /api/health`: Health check
- `GET /api/get-history`: Get conversation history

## Deployment

1. Connect your repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy - Vercel will use the `vercel.json` configuration

## Local Development

```bash
cd web
pip install -r requirements.txt
python app.py
```

The web version will work without audio dependencies and is ready for serverless deployment.
