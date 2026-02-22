# Deployment Guide - Study Bot

## Quick Deployment Checklist

### 1. Prerequisites Setup
- [ ] Create GitHub account (if not already)
- [ ] Create MongoDB Atlas account
- [ ] Get Groq API key
- [ ] Create Render account

### 2. MongoDB Atlas Setup

1. **Sign up/Login** to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)

2. **Create a Free Cluster**
   - Click "Build a Database"
   - Choose "FREE" (M0 Sandbox)
   - Select your preferred cloud provider and region
   - Click "Create Cluster"

3. **Create Database User**
   - Go to "Database Access" in left sidebar
   - Click "Add New Database User"
   - Choose "Password" authentication
   - Username: `studybot_user`
   - Password: Generate strong password (save it!)
   - Database User Privileges: "Read and write to any database"
   - Click "Add User"

4. **Configure Network Access**
   - Go to "Network Access" in left sidebar
   - Click "Add IP Address"
   - Click "Allow Access from Anywhere" (0.0.0.0/0)
   - Click "Confirm"

5. **Get Connection String**
   - Go to "Database" in left sidebar
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your actual password
   - Example: `mongodb+srv://studybot_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority`

### 3. Get Groq API Key

1. Visit [Groq Console](https://console.groq.com)
2. Sign up/Login (free account available)
3. Go to API Keys section
4. Click "Create API Key"
5. Copy your API key (keep it secret!)

### 4. Prepare GitHub Repository

1. **Create Repository**
   ```bash
   # In your project directory
   git init
   git add .
   git commit -m "Initial commit: Study Bot project"
   ```

2. **Create GitHub Repo**
   - Go to [GitHub](https://github.com)
   - Click "+" → "New repository"
   - Name: `study-bot-project`
   - Make it Public
   - Don't initialize with README (we already have one)
   - Click "Create repository"

3. **Push Code**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/study-bot-project.git
   git branch -M main
   git push -u origin main
   ```

### 5. Deploy on Render

1. **Sign up/Login** to [Render](https://dashboard.render.com/)

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Click "Connect to GitHub"
   - Authorize Render to access your repositories
   - Select your `study-bot-project` repository

3. **Configure Service**
   ```
   Name: study-bot-api
   Region: Choose closest to you (e.g., Oregon)
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free
   ```

4. **Add Environment Variables**
   Click "Advanced" → "Add Environment Variable"
   
   Add these three variables:
   ```
   MONGODB_URI = mongodb+srv://studybot_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   GROQ_API_KEY = your_groq_api_key_here
   DB_NAME = studybot
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Your app will be live at: `https://study-bot-api.onrender.com`

### 6. Test Your Deployment

1. **Health Check**
   ```bash
   curl https://your-app-name.onrender.com/health
   ```

2. **Test Chat**
   ```bash
   curl -X POST https://your-app-name.onrender.com/chat \
     -H "Content-Type: application/json" \
     -d '{"user_id": "test_user", "message": "What is photosynthesis?"}'
   ```

3. **Run Full Test Suite**
   Update `test_api.py` with your URL:
   ```python
   BASE_URL = "https://your-app-name.onrender.com"
   ```
   
   Then run:
   ```bash
   python test_api.py
   ```

### 7. Get Your API URL

Your deployed API will be accessible at:
```
https://study-bot-api-XXXXX.onrender.com
```

Copy this URL for your project submission!

## Common Issues and Solutions

### Issue: "Connection to MongoDB failed"
**Solution:** 
- Verify your MongoDB connection string is correct
- Check that password doesn't contain special characters that need URL encoding
- Ensure Network Access allows 0.0.0.0/0

### Issue: "GROQ_API_KEY not found"
**Solution:**
- Check environment variables are set in Render dashboard
- Redeploy after adding variables

### Issue: "Build failed"
**Solution:**
- Check that requirements.txt is in root directory
- Verify all dependencies are spelled correctly
- Check Render build logs for specific error

### Issue: "Service won't start"
**Solution:**
- Verify start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Check that main.py exists in root directory
- Review Render logs for error messages

### Issue: Render Free Tier Sleep
**Note:** Free tier services sleep after 15 minutes of inactivity
- First request after sleep takes 30-50 seconds (this is normal)
- Subsequent requests are fast
- For production, consider upgrading to paid tier

## Screenshots for Submission

Take screenshots of:
1. Render dashboard showing "Live" status
2. MongoDB Atlas showing your cluster
3. API response from /health endpoint
4. Test conversation from test_api.py
5. GitHub repository page

## Cost Breakdown

All services used are FREE:
- MongoDB Atlas: Free M0 cluster (512 MB storage)
- Groq API: Free tier (generous limits)
- Render: Free web service (750 hours/month)
- GitHub: Free public repositories

## Getting Help

If you encounter issues:
1. Check Render logs: Dashboard → Your Service → Logs
2. Check MongoDB logs: Atlas → Database → Cluster → Metrics
3. Test locally first with `python main.py`
4. Verify environment variables are set correctly

## Submission Checklist

For your project submission, include:
- [ ] GitHub repository link
- [ ] Deployed API URL (Render)
- [ ] Project report PDF
- [ ] Screenshots of working API
- [ ] Test results from test_api.py

Good luck with your deployment! 🚀
