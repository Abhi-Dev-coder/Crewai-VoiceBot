# test_groq.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    print("❌ GROQ_API_KEY not found!")
else:
    print(f"✅ GROQ_API_KEY found: {api_key[:10]}...")
    
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=50
        )
        print(f"✅ Groq working: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ Groq error: {e}")