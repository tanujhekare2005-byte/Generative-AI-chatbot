# API Testing Screenshots Guide

This document provides examples of what to test and screenshot for your project submission.

## Test 1: Health Check

### Request
```
GET https://your-app-name.onrender.com/health
```

### Expected Response
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-02-21T10:30:00.123456"
}
```

### Screenshot Should Show
- URL in browser or API client
- Response showing status: "healthy"
- Database: "connected"

---

## Test 2: Basic Chat

### Request
```
POST https://your-app-name.onrender.com/chat
Content-Type: application/json

{
  "user_id": "demo_student",
  "message": "What is photosynthesis?"
}
```

### Expected Response
```json
{
  "user_id": "demo_student",
  "user_message": "What is photosynthesis?",
  "bot_response": "Photosynthesis is the process by which plants, algae, and some bacteria convert light energy (usually from the sun) into chemical energy stored in glucose. This process takes place primarily in the chloroplasts of plant cells...",
  "timestamp": "2024-02-21T10:31:00.123456"
}
```

### Screenshot Should Show
- Request with user_id and message
- Bot's intelligent response about photosynthesis
- Timestamp

---

## Test 3: Context-Aware Follow-up

### First Request
```json
{
  "user_id": "demo_student",
  "message": "What is photosynthesis?"
}
```

### Second Request (Follow-up)
```json
{
  "user_id": "demo_student",
  "message": "Can you explain it in simpler terms?"
}
```

### Expected Behavior
Bot should understand "it" refers to photosynthesis from previous message and provide a simpler explanation.

### Screenshot Should Show
- Both requests in sequence
- Bot maintaining context (explaining photosynthesis without being told what "it" is)

---

## Test 4: Get Chat History

### Request
```
GET https://your-app-name.onrender.com/history/demo_student
```

### Expected Response
```json
{
  "user_id": "demo_student",
  "messages": [
    {
      "user_message": "What is photosynthesis?",
      "bot_response": "Photosynthesis is the process...",
      "timestamp": "2024-02-21T10:31:00.123456"
    },
    {
      "user_message": "Can you explain it in simpler terms?",
      "bot_response": "Sure! Think of photosynthesis as...",
      "timestamp": "2024-02-21T10:32:00.123456"
    }
  ]
}
```

### Screenshot Should Show
- All previous messages stored
- Timestamps in chronological order

---

## Test 5: Multiple Users (Isolation)

### User 1
```json
{
  "user_id": "student_alice",
  "message": "What is calculus?"
}
```

### User 2
```json
{
  "user_id": "student_bob",
  "message": "What is biology?"
}
```

### Get History
```
GET /history/student_alice  → Should only show calculus conversation
GET /history/student_bob    → Should only show biology conversation
```

### Screenshot Should Show
- Different users have separate, isolated conversations

---

## Test 6: Various Study Topics

Test with different subjects to show versatility:

```json
// Math
{"user_id": "test", "message": "Explain the Pythagorean theorem"}

// Science
{"user_id": "test", "message": "What causes earthquakes?"}

// History
{"user_id": "test", "message": "What was the French Revolution?"}

// Study Tips
{"user_id": "test", "message": "How can I improve my memory?"}
```

### Screenshot Should Show
- Bot handles multiple subjects effectively
- Provides educational, helpful responses

---

## Test 7: Statistics

### Request
```
GET https://your-app-name.onrender.com/stats
```

### Expected Response
```json
{
  "total_users": 5,
  "total_conversations": 23,
  "database_status": "connected"
}
```

---

## Using cURL (Command Line)

```bash
# Health Check
curl https://your-app-name.onrender.com/health

# Chat
curl -X POST https://your-app-name.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "What is photosynthesis?"}'

# Get History
curl https://your-app-name.onrender.com/history/test

# Stats
curl https://your-app-name.onrender.com/stats
```

---

## Using Python test_api.py

```bash
# Update BASE_URL in test_api.py
BASE_URL = "https://your-app-name.onrender.com"

# Run tests
python test_api.py
```

This will test all endpoints and show results.

---

## Using Postman

1. Import collection or create requests manually
2. Set base URL: `https://your-app-name.onrender.com`
3. Add headers: `Content-Type: application/json`
4. Send requests and capture screenshots

---

## Recommended Screenshots for Submission

1. **Render Dashboard**
   - Show your service is "Live"
   - Display the service URL

2. **MongoDB Atlas**
   - Show your cluster is active
   - Display the database name

3. **Health Check Response**
   - Successful connection to database

4. **Chat Conversation**
   - At least 3 messages showing context awareness

5. **Chat History**
   - Retrieved messages from database

6. **Test Script Output**
   - Results from test_api.py showing all tests passed

7. **GitHub Repository**
   - Code structure and files
   - README.md rendered

---

## Tips for Good Screenshots

✓ Include the URL in the screenshot  
✓ Show timestamps to prove real-time functionality  
✓ Capture full request and response  
✓ Use syntax highlighting when possible  
✓ Show multiple tests to demonstrate reliability  
✓ Include a timestamp or date in screenshot  

---

## Example Test Sequence (Recommended for Demo)

```
1. GET /health                    → Verify system is working
2. POST /chat (Question 1)        → Ask about a topic
3. POST /chat (Follow-up)         → Show context memory
4. GET /history                   → Verify storage
5. POST /chat (Different user)    → Show multi-user support
6. GET /stats                     → Show system metrics
```

This sequence demonstrates all key features of your Study Bot!
