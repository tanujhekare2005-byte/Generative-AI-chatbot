# Study Bot - AI-Powered Study Assistant 🤖📚

An intelligent chatbot designed to help students with their studies by answering questions, explaining concepts, and maintaining conversation context through MongoDB storage.

## 🌟 Features

- **AI-Powered Responses**: Uses Groq's LLM (Llama 3.1) for intelligent study assistance
- **Conversation Memory**: Stores and retrieves chat history using MongoDB
- **Context-Aware**: Maintains conversation context for better responses
- **RESTful API**: Easy-to-use FastAPI endpoints
- **Multi-User Support**: Handles multiple users with separate conversation histories
- **Study-Focused**: Specialized prompts for educational content

## 🏗️ Architecture

```
study-bot-project/
├── main.py              # FastAPI application and endpoints
├── chatbot.py           # LLM integration and response generation
├── database.py          # MongoDB connection and operations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── test_api.py          # API testing script
└── README.md           # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- MongoDB (local or Atlas)
- Groq API key ([Get one here](https://console.groq.com))

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd study-bot-project
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
cp .env.example .env
```

Edit `.env` with your credentials:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=studybot
GROQ_API_KEY=your_groq_api_key_here
PORT=8000
```

### Running Locally

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### Root
```http
GET /
```
Returns API information and available endpoints.

### Health Check
```http
GET /health
```
Checks API and database connectivity.

### Chat
```http
POST /chat
Content-Type: application/json

{
  "user_id": "user123",
  "message": "What is photosynthesis?"
}
```

Response:
```json
{
  "user_id": "user123",
  "user_message": "What is photosynthesis?",
  "bot_response": "Photosynthesis is...",
  "timestamp": "2024-02-21T10:30:00"
}
```

### Get History
```http
GET /history/{user_id}?limit=50
```
Retrieves conversation history for a user.

### Clear History
```http
DELETE /clear-history/{user_id}
```
Clears all conversation history for a user.

### Statistics
```http
GET /stats
```
Returns system statistics (total users, conversations).

## 🧪 Testing

Run the test script:
```bash
python test_api.py
```

This will test all API endpoints and display results.

## 🌐 Deployment on Render

### Step 1: Prepare for Deployment

1. **Create a GitHub repository**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Set up MongoDB Atlas

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user
4. Whitelist all IP addresses (0.0.0.0/0) for Render
5. Get your connection string

### Step 3: Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: study-bot-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `MONGODB_URI`: Your MongoDB Atlas connection string
   - `DB_NAME`: studybot
   - `GROQ_API_KEY`: Your Groq API key
6. Click "Create Web Service"

### Step 4: Test Deployment

Once deployed, update the `BASE_URL` in `test_api.py` to your Render URL:
```python
BASE_URL = "https://your-app-name.onrender.com"
```

Run tests:
```bash
python test_api.py
```

## 💡 Usage Examples

### Example 1: Basic Question
```python
import requests

response = requests.post(
    "https://your-app.onrender.com/chat",
    json={
        "user_id": "student_1",
        "message": "Explain the Pythagorean theorem"
    }
)
print(response.json()["bot_response"])
```

### Example 2: Follow-up Question (with context)
```python
# First question
response1 = requests.post(
    "https://your-app.onrender.com/chat",
    json={
        "user_id": "student_1",
        "message": "What is calculus?"
    }
)

# Follow-up (bot remembers context)
response2 = requests.post(
    "https://your-app.onrender.com/chat",
    json={
        "user_id": "student_1",
        "message": "Can you give me an example?"
    }
)
```

## 🔧 Configuration

### LLM Model
Change the model in `chatbot.py`:
```python
self.llm = ChatGroq(
    groq_api_key=self.api_key,
    model_name="llama-3.1-70b-versatile",  # Change this
    temperature=0.7,
    max_tokens=1024
)
```

Available models:
- `llama-3.1-70b-versatile`
- `llama-3.1-8b-instant`
- `mixtral-8x7b-32768`

### System Prompt
Customize the bot's behavior in `chatbot.py` by modifying `self.system_prompt`.

## 📊 Memory Implementation

The Study Bot implements conversation memory using MongoDB:

1. **Storage**: Each conversation exchange is stored with user_id, messages, and timestamp
2. **Retrieval**: When a user sends a message, the last 10 exchanges are retrieved
3. **Context**: Previous messages are sent to the LLM to maintain context
4. **Efficiency**: Indexes on user_id and timestamp ensure fast queries

## 🛠️ Troubleshooting

### MongoDB Connection Error
- Check your connection string
- Ensure IP whitelist includes 0.0.0.0/0
- Verify database user credentials

### Groq API Error
- Verify your API key is correct
- Check rate limits
- Ensure the model name is valid

### Deployment Issues
- Check Render logs: Dashboard → Your Service → Logs
- Verify all environment variables are set
- Ensure requirements.txt includes all dependencies

## 📝 Project Requirements Met

✅ FastAPI application with API endpoints  
✅ LLM integration (Groq/Langchain)  
✅ MongoDB database for chat history  
✅ Context-aware responses using memory  
✅ Study-focused system prompt  
✅ Deployed on Render  
✅ Comprehensive documentation  
✅ Test suite included  

## 🤝 Contributing

This is a student project. Feel free to fork and modify for your learning!

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Created as part of the DevTown Study Bot Project

---

**Need Help?**
- Check the [Render Documentation](https://render.com/docs)
- Review [FastAPI Documentation](https://fastapi.tiangolo.com)
- See [Groq Documentation](https://console.groq.com/docs)
