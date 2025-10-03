# 🚀 Deployment Guide - Host Your FAQ API

This guide shows you multiple ways to host your Mental Health FAQ API so it's accessible from your Flutter app anywhere.

---

## 📋 Table of Contents

1. [Quick Testing with ngrok (5 minutes)](#option-1-quick-testing-with-ngrok-5-minutes)
2. [Free Hosting on Render.com (20 minutes)](#option-2-free-hosting-on-rendercom-recommended)
3. [Free Hosting on Railway.app (15 minutes)](#option-3-free-hosting-on-railwayapp)
4. [Hosting on PythonAnywhere (Free tier)](#option-4-pythonanywhere-free-tier)
5. [Self-Hosting on Your Network (Local)](#option-5-self-hosting-on-your-local-network)

---

## Option 1: Quick Testing with ngrok (5 minutes)

**Best for:** Quick testing, temporary access

### Step 1: Install ngrok

1. Go to https://ngrok.com and sign up (free)
2. Download ngrok for Windows
3. Extract `ngrok.exe` to a folder
4. Get your auth token from dashboard

### Step 2: Setup ngrok

```powershell
# Add to PATH or navigate to ngrok folder
cd C:\path\to\ngrok

# Authenticate
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### Step 3: Start Your API Server

```powershell
# Terminal 1: Start your API
cd C:\Users\sepok\SLMChatCore-1
.\.venv\Scripts\activate.ps1
uvicorn faq_api:app --host 0.0.0.0 --port 8000
```

### Step 4: Start ngrok Tunnel

```powershell
# Terminal 2: Start ngrok
ngrok http 8000
```

You'll see something like:
```
Forwarding   https://abc123.ngrok.io -> http://localhost:8000
```

### Step 5: Update Flutter App

Copy the `https://abc123.ngrok.io` URL and update your Flutter app:

```dart
// In api_service.dart
static const String baseUrl = 'https://abc123.ngrok.io';
```

**Pros:**
- ✅ Works instantly
- ✅ HTTPS included
- ✅ No configuration needed

**Cons:**
- ❌ URL changes every restart (free tier)
- ❌ API must run on your PC
- ❌ Not for production

---

## Option 2: Free Hosting on Render.com (Recommended)

**Best for:** Production, permanent hosting, free tier available

### Step 1: Prepare Your Repository

1. **Create a `Procfile`** in your project root:

```bash
web: uvicorn faq_api:app --host 0.0.0.0 --port $PORT
```

2. **Update `requirements.txt`** (add if missing):

```txt
fastapi==0.118.0
uvicorn[standard]==0.35.0
sentence-transformers==3.1.1
pandas==2.2.3
numpy==2.1.2
scikit-learn==1.5.2
torch==2.5.1
protobuf==5.28.3
```

3. **Create `render.yaml`** (optional but recommended):

```yaml
services:
  - type: web
    name: mental-health-faq-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn faq_api:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

### Step 2: Push to GitHub

```powershell
# Initialize git if not already done
git init
git add .
git commit -m "Prepare for Render deployment"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/SLMChatCore.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Render

1. Go to https://render.com and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your `SLMChatCore` repository
5. Configure:
   - **Name:** `mental-health-faq-api`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn faq_api:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free
6. Click **"Create Web Service"**

### Step 4: Wait for Deployment (10-15 minutes)

Render will:
- Install all dependencies
- Load your model
- Start the server

You'll get a URL like: `https://mental-health-faq-api.onrender.com`

### Step 5: Update Flutter App

```dart
// In api_service.dart
static const String baseUrl = 'https://mental-health-faq-api.onrender.com';
```

### Step 6: Test Your API

Visit in browser:
- `https://mental-health-faq-api.onrender.com/docs`
- `https://mental-health-faq-api.onrender.com/health`

**Pros:**
- ✅ Free tier available
- ✅ Auto-deploy from GitHub
- ✅ HTTPS included
- ✅ Permanent URL
- ✅ No PC needed

**Cons:**
- ❌ Spins down after 15 min inactivity (free tier)
- ❌ First request after sleep is slow (30s)

**Pro Tip:** Upgrade to paid tier ($7/month) for always-on service.

---

## Option 3: Free Hosting on Railway.app

**Best for:** Easy deployment, modern UI

### Step 1: Prepare Files

1. **Create `Procfile`:**

```bash
web: uvicorn faq_api:app --host 0.0.0.0 --port $PORT
```

2. **Ensure `requirements.txt` is complete** (same as Render)

### Step 2: Deploy

1. Go to https://railway.app and sign up
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway auto-detects Python
5. Add environment variables if needed
6. Deploy!

You'll get: `https://your-app.up.railway.app`

### Step 3: Update Flutter App

```dart
static const String baseUrl = 'https://your-app.up.railway.app';
```

**Pros:**
- ✅ $5 free credit/month
- ✅ Modern dashboard
- ✅ Fast deployment
- ✅ Always on (within free credit)

**Cons:**
- ❌ Free credit runs out
- ❌ Need credit card after trial

---

## Option 4: PythonAnywhere (Free Tier)

**Best for:** Python-specific hosting, learning

### Step 1: Sign Up

1. Go to https://www.pythonanywhere.com
2. Create a free "Beginner" account

### Step 2: Upload Your Code

1. Open a **Bash console**
2. Clone your repo:

```bash
git clone https://github.com/YOUR_USERNAME/SLMChatCore.git
cd SLMChatCore
```

### Step 3: Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 faqenv
pip install -r requirements.txt
```

### Step 4: Configure Web App

1. Go to **Web** tab
2. Click **"Add a new web app"**
3. Choose **Manual configuration** → Python 3.10
4. Set:
   - **Source code:** `/home/yourusername/SLMChatCore`
   - **Working directory:** `/home/yourusername/SLMChatCore`
   - **WSGI file:** Configure ASGI for FastAPI

### Step 5: Edit WSGI Configuration

Replace content with:

```python
import sys
path = '/home/yourusername/SLMChatCore'
if path not in sys.path:
    sys.path.append(path)

from faq_api import app as application
```

### Step 6: Reload and Test

URL: `https://yourusername.pythonanywhere.com`

**Pros:**
- ✅ Free tier forever
- ✅ Good for learning
- ✅ Python-focused

**Cons:**
- ❌ Limited resources on free tier
- ❌ Model might be too large
- ❌ More manual setup

---

## Option 5: Self-Hosting on Your Local Network

**Best for:** Development, LAN-only access

### Step 1: Find Your PC's IP Address

```powershell
ipconfig
```

Look for **IPv4 Address** (e.g., `192.168.1.42`)

### Step 2: Allow Through Windows Firewall

```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "FAQ API" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

Or manually:
1. Open **Windows Defender Firewall**
2. Click **Advanced settings**
3. Click **Inbound Rules** → **New Rule**
4. Port: TCP 8000
5. Allow the connection

### Step 3: Start API Server

```powershell
cd C:\Users\sepok\SLMChatCore-1
.\.venv\Scripts\activate.ps1
uvicorn faq_api:app --host 0.0.0.0 --port 8000
```

### Step 4: Update Flutter App

```dart
// Use your PC's actual IP
static const String baseUrl = 'http://192.168.1.42:8000';
```

### Step 5: Test

From another device on same WiFi:
- Visit: `http://192.168.1.42:8000/docs`

**Pros:**
- ✅ Free
- ✅ Fast
- ✅ Full control

**Cons:**
- ❌ Only works on same WiFi
- ❌ PC must be on
- ❌ IP might change
- ❌ No HTTPS

---

## 🎯 Recommendation

| Use Case | Recommended Option | Cost |
|----------|-------------------|------|
| **Quick Testing** | ngrok | Free |
| **Development** | Local Network | Free |
| **Production (Hobby)** | Render.com Free Tier | Free |
| **Production (Serious)** | Render.com Paid | $7/mo |
| **Production (Scale)** | Railway/AWS/GCP | Variable |

---

## 📱 After Deployment: Update Your Flutter App

### 1. Update `api_service.dart`

```dart
class ApiService {
  // Replace with your deployed URL
  static const String baseUrl = 'https://your-app.onrender.com';
  
  // Or use environment variables:
  // static const String baseUrl = String.fromEnvironment(
  //   'API_URL',
  //   defaultValue: 'http://10.0.2.2:8000',
  // );
  
  // ... rest of code
}
```

### 2. Test Connection

```dart
// Add this test in your app
void testConnection() async {
  try {
    final health = await ApiService.checkHealth();
    print('✅ Connected: ${health['status']}');
  } catch (e) {
    print('❌ Connection failed: $e');
  }
}
```

### 3. Handle Errors Gracefully

```dart
try {
  final response = await ApiService.queryFaq(question);
  // Use response
} on SocketException {
  // Show: "Cannot connect to server"
} on TimeoutException {
  // Show: "Server is taking too long"
} catch (e) {
  // Show: "An error occurred"
}
```

---

## 🔧 Troubleshooting

### API Returns 503 "Bot not initialized"

**Cause:** Model files not loaded on server

**Fix:**
1. Ensure `faq_model/` directory is in your repo
2. Check server logs for errors
3. Verify all model files are present

### Render Deployment Fails

**Common Issues:**
1. **Out of memory:** Model too large for free tier
   - Solution: Upgrade to paid tier or use smaller model
2. **Build timeout:** Dependencies take too long
   - Solution: Remove unnecessary packages from `requirements.txt`

### Railway Free Credit Runs Out

**Solution:**
- Add credit card for $5/month credit
- Or switch to Render free tier

### ngrok URL Changes Every Time

**Solution:**
- Upgrade to ngrok paid plan for static domain ($8/mo)
- Or use Render for permanent URL

---

## 🎉 Next Steps

1. Choose your hosting option
2. Deploy your API
3. Update Flutter app with new URL
4. Test thoroughly
5. Monitor logs for errors

**Need help?** Check the server logs:
- **Render:** Dashboard → Logs
- **Railway:** Dashboard → Deployments → Logs
- **Local:** Terminal output

---

**You're ready to deploy! Choose the option that best fits your needs and follow the steps above.** 🚀
