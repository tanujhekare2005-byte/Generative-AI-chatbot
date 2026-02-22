"""
Database Module - MongoDB Integration
Handles chat history storage and retrieval
"""

import os
from typing import List, Dict, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

class ChatDatabase:
    """
    MongoDB database handler for chat history
    """
    
    def __init__(self):
        """Initialize MongoDB connection"""
        self.mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.db_name = os.getenv("DB_NAME", "studybot")
        self.collection_name = "chat_history"
        
        try:
            # Connect to MongoDB
            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            
            # Create index on user_id for faster queries
            self.collection.create_index("user_id")
            self.collection.create_index("timestamp")
            
            print(f"✓ Connected to MongoDB: {self.db_name}")
            
        except ConnectionFailure as e:
            print(f"✗ Failed to connect to MongoDB: {str(e)}")
            raise
    
    def check_connection(self) -> bool:
        """Check if database connection is alive"""
        try:
            self.client.admin.command('ping')
            return True
        except Exception:
            return False
    
    def store_message(self, user_id: str, user_message: str, bot_response: str) -> dict:
        """
        Store a conversation exchange in the database
        
        Args:
            user_id: User identifier
            user_message: User's message
            bot_response: Bot's response
            
        Returns:
            Inserted document
        """
        try:
            document = {
                "user_id": user_id,
                "user_message": user_message,
                "bot_response": bot_response,
                "timestamp": datetime.utcnow()
            }
            
            result = self.collection.insert_one(document)
            document["_id"] = str(result.inserted_id)
            
            return document
            
        except PyMongoError as e:
            print(f"Error storing message: {str(e)}")
            raise
    
    def get_chat_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """
        Retrieve chat history for a user
        
        Args:
            user_id: User identifier
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of chat messages
        """
        try:
            cursor = self.collection.find(
                {"user_id": user_id}
            ).sort("timestamp", 1).limit(limit)
            
            history = []
            for doc in cursor:
                history.append({
                    "user_message": doc.get("user_message"),
                    "bot_response": doc.get("bot_response"),
                    "timestamp": doc.get("timestamp").isoformat() if doc.get("timestamp") else None
                })
            
            return history
            
        except PyMongoError as e:
            print(f"Error retrieving history: {str(e)}")
            return []
    
    def clear_history(self, user_id: str) -> int:
        """
        Clear all chat history for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            Number of deleted documents
        """
        try:
            result = self.collection.delete_many({"user_id": user_id})
            return result.deleted_count
            
        except PyMongoError as e:
            print(f"Error clearing history: {str(e)}")
            raise
    
    def get_statistics(self) -> Dict:
        """
        Get database statistics
        
        Returns:
            Dictionary with statistics
        """
        try:
            total_conversations = self.collection.count_documents({})
            total_users = len(self.collection.distinct("user_id"))
            
            return {
                "total_conversations": total_conversations,
                "total_users": total_users
            }
            
        except PyMongoError as e:
            print(f"Error getting statistics: {str(e)}")
            return {
                "total_conversations": 0,
                "total_users": 0
            }
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("✓ MongoDB connection closed")
