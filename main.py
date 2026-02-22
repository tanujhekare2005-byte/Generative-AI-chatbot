"""
Study Bot - AI-Powered Study Assistant
Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
import uvicorn

# Import custom modules
from chatbot import StudyBot
from database import ChatDatabase

# Initialize FastAPI app
app = FastAPI(
    title="Study Bot API",
    description="AI-powered study assistant with conversation memory",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize bot and database
study_bot = StudyBot()
db = ChatDatabase()

# Request/Response Models
class ChatRequest(BaseModel):
    user_id: str
    message: str
    
class ChatResponse(BaseModel):
    user_id: str
    user_message: str
    bot_response: str
    timestamp: str

class HistoryResponse(BaseModel):
    user_id: str
    messages: List[dict]

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to Study Bot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "history": "/history/{user_id}",
            "clear_history": "/clear-history/{user_id}",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_status = db.check_connection()
        return {
            "status": "healthy",
            "database": "connected" if db_status else "disconnected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the Study Bot
    
    Args:
        request: ChatRequest with user_id and message
        
    Returns:
        ChatResponse with bot's reply
    """
    try:
        # Retrieve conversation history
        history = db.get_chat_history(request.user_id)
        
        # Get bot response
        bot_response = study_bot.get_response(
            user_message=request.message,
            chat_history=history
        )
        
        # Store conversation in database
        db.store_message(
            user_id=request.user_id,
            user_message=request.message,
            bot_response=bot_response
        )
        
        return ChatResponse(
            user_id=request.user_id,
            user_message=request.message,
            bot_response=bot_response,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/history/{user_id}", response_model=HistoryResponse)
async def get_history(user_id: str, limit: Optional[int] = 50):
    """
    Retrieve chat history for a user
    
    Args:
        user_id: User identifier
        limit: Maximum number of messages to retrieve
        
    Returns:
        HistoryResponse with conversation history
    """
    try:
        history = db.get_chat_history(user_id, limit=limit)
        return HistoryResponse(
            user_id=user_id,
            messages=history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@app.delete("/clear-history/{user_id}")
async def clear_history(user_id: str):
    """
    Clear chat history for a user
    
    Args:
        user_id: User identifier
        
    Returns:
        Confirmation message
    """
    try:
        result = db.clear_history(user_id)
        return {
            "message": f"Chat history cleared for user: {user_id}",
            "deleted_count": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing history: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        stats = db.get_statistics()
        return {
            "total_users": stats.get("total_users", 0),
            "total_conversations": stats.get("total_conversations", 0),
            "database_status": "connected"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

# Run the application
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
