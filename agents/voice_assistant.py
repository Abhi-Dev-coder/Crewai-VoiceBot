from crewai import Agent
from groq import Groq
from config import Config

class DirectGroqClient:
    """Direct Groq client that bypasses CrewAI's LLM system"""
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
    
    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a friendly voice assistant. Give concise, conversational responses under 100 words."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"

class VoiceAssistantAgent:
    def __init__(self, groq_api_key: str):
        self.groq_client = DirectGroqClient(groq_api_key)
        
        # Create agent WITHOUT LLM to avoid litellm
        self.agent = Agent(
            role='Voice Assistant',
            goal='Provide helpful responses to user voice queries',
            backstory='You are a friendly voice assistant.',
            verbose=True,
            allow_delegation=False
            # NO LLM parameter!
        )
    
    def process_query(self, query: str, history: list | None = None) -> str:
        """Process query directly, optionally using short conversation history for context"""
        if history:
            # Build a compact context prefix from recent exchanges
            recent_pairs = history[-5:]  # limit context size
            context_lines = []
            for item in recent_pairs:
                user = item.get("query")
                assistant = item.get("response")
                if user:
                    context_lines.append(f"User: {user}")
                if assistant:
                    context_lines.append(f"Assistant: {assistant}")
            context = "\n".join(context_lines)
            prompt = f"Context from previous conversation (most recent first):\n{context}\n\nCurrent user message: {query}\n\nPlease answer concisely while respecting the context."
        else:
            prompt = query
        return self.groq_client.generate_response(prompt)

class LoggerAgent:
    def __init__(self, groq_api_key: str):
        self.groq_client = DirectGroqClient(groq_api_key)
        self.agent = Agent(
            role='Query Logger',
            goal='Log interactions',
            backstory='You log conversations.',
            verbose=True,
            allow_delegation=False
        )