from crewai import Task
from typing import Dict, Any

def create_voice_response_task(agent, tools: list, user_query: str) -> Task:
    return Task(
        description=f'''
        Process the user's voice query: "{user_query}"
        
        Steps to complete:
        1. Understand the user's intent and question
        2. Provide a helpful, accurate, and conversational response
        3. Ensure the response is appropriate for voice output (clear, concise, natural)
        4. Keep responses under 100 words for better voice delivery
        
        Guidelines:
        - Be friendly and professional
        - Provide specific information when possible
        - If you don't know something, admit it honestly
        - Use natural language suitable for speech
        ''',
        agent=agent,
        tools=tools,
        expected_output="A clear, helpful response suitable for text-to-speech conversion"
    )

def create_logging_task(agent, tools: list, query: str, response: str) -> Task:
    return Task(
        description=f'''
        Log the following interaction:
        User Query: "{query}"
        Assistant Response: "{response}"
        
        Ensure the log entry includes:
        - Timestamp
        - Complete user query
        - Full assistant response
        - Appropriate categorization
        ''',
        agent=agent,
        tools=tools,
        expected_output="Confirmation that the interaction has been logged successfully"
    )


