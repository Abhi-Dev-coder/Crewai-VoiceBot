# 🚀 VoiceBot Deployment Guide

This guide provides multiple options to deploy your VoiceBot project online so others can access it via a public URL.

## 📋 Prerequisites

1. **Groq API Key**: Get your free API key from [Groq Console](https://console.groq.com/)
2. **GitHub Account**: For version control and deployment
3. **Deployment Platform Account**: Choose one of the platforms below

## 🎯 Quick Deployment Options

### Option 1: Railway (Recommended - Easiest)

Railway offers the simplest deployment with automatic builds and free tier.

#### Steps:
1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/voicebot-project.git
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Go to [Railway.app](https://railway.app/)
   - Sign up/login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variable: `GROQ_API_KEY=your_api_key_here`
   - Railway will automatically detect the Dockerfile and deploy

3. **Access your app**: Railway will provide a public URL like `https://your-app-name.railway.app`

### Option 2: Render (Free Tier Available)

Render provides reliable hosting with a generous free tier.

#### Steps:
1. **Push to GitHub** (same as Railway)

2. **Deploy on Render**:
   - Go to [Render.com](https://render.com/)
   - Sign up/login with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 web.app:app`
     - **Environment**: Python 3
   - Add environment variable: `GROQ_API_KEY=your_api_key_here`
   - Click "Create Web Service"

3. **Access your app**: Render will provide a URL like `https://your-app-name.onrender.com`

### Option 3: Vercel (Serverless)

Vercel offers serverless deployment with excellent performance.

#### Steps:
1. **Push to GitHub** (same as above)

2. **Deploy on Vercel**:
   - Go to [Vercel.com](https://vercel.com/)
   - Sign up/login with GitHub
   - Click "New Project"
   - Import your GitHub repository
   - Add environment variable: `GROQ_API_KEY=your_api_key_here`
   - Click "Deploy"

3. **Access your app**: Vercel will provide a URL like `https://your-app-name.vercel.app`

### Option 4: Heroku (Paid)

Heroku requires a paid plan but offers excellent reliability.

#### Steps:
1. **Install Heroku CLI** and login
2. **Create Heroku app**:
   ```bash
   heroku create your-voicebot-app
   ```
3. **Set environment variable**:
   ```bash
   heroku config:set GROQ_API_KEY=your_api_key_here
   ```
4. **Deploy**:
   ```bash
   git push heroku main
   ```

## 🔧 Environment Variables

All platforms require the `GROQ_API_KEY` environment variable:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

Optional environment variables:
```bash
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5000
```

## 🐳 Docker Deployment (Advanced)

If you want to deploy using Docker:

1. **Build the image**:
   ```bash
   docker build -t voicebot-app .
   ```

2. **Run locally**:
   ```bash
   docker run -p 5000:5000 -e GROQ_API_KEY=your_key voicebot-app
   ```

3. **Deploy to cloud**:
   - Push to Docker Hub
   - Use any cloud provider that supports Docker containers

## 🔍 Testing Your Deployment

After deployment, test your app:

1. **Health Check**: Visit `https://your-app-url/api/health`
2. **Main Interface**: Visit `https://your-app-url/`
3. **Test Voice Input**: Try the microphone feature
4. **Test Text Input**: Type a message and send

## 🚨 Troubleshooting

### Common Issues:

1. **"GROQ_API_KEY not set"**:
   - Ensure environment variable is set in your deployment platform
   - Check the variable name is exactly `GROQ_API_KEY`

2. **App not starting**:
   - Check logs in your deployment platform
   - Ensure all dependencies are in `requirements.txt`
   - Verify the start command is correct

3. **Voice features not working**:
   - Voice input requires HTTPS in production
   - Some browsers may block microphone access on HTTP

4. **Slow responses**:
   - This is normal for free tiers
   - Consider upgrading to paid plans for better performance

## 📊 Monitoring

- **Railway**: Built-in metrics and logs
- **Render**: Dashboard with logs and metrics
- **Vercel**: Analytics and function logs
- **Heroku**: Logs via CLI: `heroku logs --tail`

## 🔄 Updates

To update your deployed app:

1. Make changes to your code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```
3. Most platforms auto-deploy on git push

## 💡 Tips

1. **Start with Railway** - it's the easiest for beginners
2. **Use environment variables** for sensitive data
3. **Test locally first** before deploying
4. **Monitor your usage** to avoid hitting API limits
5. **Keep your Groq API key secure** - never commit it to git

## 🆘 Need Help?

- Check the platform's documentation
- Look at the logs for error messages
- Test the health endpoint first
- Ensure your Groq API key is valid and has credits

---

**Ready to deploy?** Choose Railway for the easiest experience, or Render for a reliable free option!
