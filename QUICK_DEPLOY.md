# 🚀 Quick Start - Deploy in 5 Minutes

Choose your deployment method:

## ⚡ Fastest: ngrok (Temporary Testing)

```powershell
# Terminal 1: Start API
cd C:\Users\sepok\SLMChatCore-1
.\.venv\Scripts\activate.ps1
uvicorn faq_api:app --host 0.0.0.0 --port 8000

# Terminal 2: Start ngrok
ngrok http 8000
# Copy the https URL (e.g., https://abc123.ngrok.io)
```

**Update Flutter:**
```dart
static const String baseUrl = 'https://abc123.ngrok.io';
```

---

## 🌐 Best: Render.com (Free & Permanent)

### 1. Push to GitHub

```powershell
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Deploy on Render

1. Go to https://render.com
2. Sign up (free)
3. Click **New +** → **Web Service**
4. Connect GitHub → Select `SLMChatCore`
5. Settings:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn faq_api:app --host 0.0.0.0 --port $PORT`
6. Click **Create**

### 3. Wait 10-15 min for deployment

You'll get: `https://your-app-name.onrender.com`

**Update Flutter:**
```dart
static const String baseUrl = 'https://your-app-name.onrender.com';
```

---

## 🏠 Local Network (Same WiFi Only)

### 1. Find Your IP

```powershell
ipconfig
# Look for IPv4 (e.g., 192.168.1.42)
```

### 2. Allow Firewall (Run as Admin)

```powershell
New-NetFirewallRule -DisplayName "FAQ API" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

### 3. Start Server

```powershell
cd C:\Users\sepok\SLMChatCore-1
.\.venv\Scripts\activate.ps1
uvicorn faq_api:app --host 0.0.0.0 --port 8000
```

**Update Flutter:**
```dart
static const String baseUrl = 'http://192.168.1.42:8000';  // Your IP
```

---

## 🧪 Test Your Deployment

Visit in browser:
- `/docs` - Interactive API docs
- `/health` - Quick health check

Or run:
```powershell
python test_api_complete.py
```

---

**For detailed instructions, see [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md)**
