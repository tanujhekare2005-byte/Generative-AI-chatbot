"""
Study Bot - Chatbot Logic
Integrates with LLM (Groq) for generating responses
"""

import os
from typing import List, Dict
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage, SystemMessage

class StudyBot:
    """
    Study Bot class that handles AI responses using Groq LLM
    """
    
    def __init__(self):
        """Initialize the Study Bot with Groq LLM"""
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Initialize Groq LLM
        self.llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name="llama-3.1-70b-versatile",  # You can change to other models
            temperature=0.7,
            max_tokens=1024
        )
        
        # System prompt for the Study Bot
        self.system_prompt = """You are a helpful and knowledgeable Study Bot assistant. 
Your purpose is to help students with their studies by:

1. Answering questions about various academic subjects (math, science, history, literature, etc.)
2. Explaining complex concepts in simple terms
3. Providing study tips and learning strategies
4. Helping with homework and assignments (guiding, not just giving answers)
5. Offering memory techniques and study methodologies
6. Recommending resources and study materials

Guidelines:
- Be patient, encouraging, and supportive
- Break down complex topics into manageable parts
- Ask clarifying questions when needed
- Provide examples to illustrate concepts
- Remember previous conversations to provide contextual help
- Focus on helping students understand, not just memorize
- If you don't know something, admit it and suggest how to find the answer

Maintain a friendly, educational tone and always prioritize the student's learning journey."""

    def get_response(self, user_message: str, chat_history: List[Dict] = None) -> str:
        """
        Generate a response to the user's message
        
        Args:
            user_message: The user's input message
            chat_history: Previous conversation history
            
        Returns:
            Bot's response as a string
        """
        try:
            # Build message chain
            messages = [SystemMessage(content=self.system_prompt)]
            
            # Add chat history if available (limited to last 10 exchanges)
            if chat_history:
                recent_history = chat_history[-10:]  # Last 10 messages
                for entry in recent_history:
                    messages.append(HumanMessage(content=entry.get("user_message", "")))
                    messages.append(AIMessage(content=entry.get("bot_response", "")))
            
            # Add current user message
            messages.append(HumanMessage(content=user_message))
            
            # Get response from LLM
            response = self.llm.invoke(messages)
            
            return response.content
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error processing your request. Please try again."
    
    def get_simple_response(self, user_message: str) -> str:
        """
        Generate a simple response without history (for testing)
        
        Args:
            user_message: The user's input message
            
        Returns:
            Bot's response as a string
        """
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error. Please try again."
