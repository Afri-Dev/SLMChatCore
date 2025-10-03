# 🚀 START HERE - Choose Your Path

## I want to...

### 🧪 Test the API locally first
👉 **Start here:**
1. Open terminal in `SLMChatCore-1`
2. Run: `.\.venv\Scripts\activate.ps1`
3. Run: `uvicorn faq_api:app --host 0.0.0.0 --port 8000`
4. Visit: http://localhost:8000/docs
5. Test queries in Swagger UI

📖 **Read:** None needed - just test!

---

### ⚡ Deploy quickly for testing (5 min)
👉 **Start here:**
1. Keep API running (see above)
2. Open new terminal
3. Run: `ngrok http 8000`
4. Copy the `https://` URL
5. Update Flutter app with URL

📖 **Read:** [`QUICK_DEPLOY.md`](QUICK_DEPLOY.md) section "ngrok"

---

### 🌐 Deploy to production (20 min)
👉 **Start here:**
1. Push code to GitHub
2. Go to https://render.com
3. Create Web Service from GitHub
4. Wait for deployment
5. Get your permanent URL

📖 **Read:** [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) → "Option 2: Render.com"

---

### 📱 Connect my Flutter app
👉 **Start here:**
1. Copy files from `flutter_integration/` to your Flutter project
2. Add `http: ^1.1.0` to pubspec.yaml
3. Update API URL in `api_service.dart`
4. Run `flutter pub get`
5. Run `flutter run`

📖 **Read:** [`FLUTTER_INTEGRATION_COMPLETE.md`](FLUTTER_INTEGRATION_COMPLETE.md)

---

### 🏠 Host on my local network (WiFi only)
👉 **Start here:**
1. Run: `ipconfig` to find your IP
2. Allow firewall port 8000
3. Start API with `--host 0.0.0.0`
4. Update Flutter with `http://YOUR_IP:8000`

📖 **Read:** [`QUICK_DEPLOY.md`](QUICK_DEPLOY.md) section "Local Network"

---

### 📚 Understand everything first
👉 **Start here:**

Read in this order:
1. [`README_COMPLETE.md`](README_COMPLETE.md) - Complete overview
2. [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) - Hosting options
3. [`FLUTTER_INTEGRATION_COMPLETE.md`](FLUTTER_INTEGRATION_COMPLETE.md) - Flutter setup

---

## 🆘 I have a problem

### API won't start
- Check: Virtual environment activated?
- Run: `pip install -r requirements.txt`
- Check: Protobuf version (run `pip install protobuf==5.28.3 --force-reinstall`)

### Flutter can't connect
- Check: API is running? Visit `http://localhost:8000/health`
- Check: Correct URL in `api_service.dart`?
  - Android emulator: `http://10.0.2.2:8000`
  - Real device: `http://YOUR_PC_IP:8000`
  - Deployed: `https://your-app.onrender.com`

### Deployment failed
- Check: All files pushed to GitHub?
- Check: `requirements.txt` complete?
- Check: Build logs on Render/Railway for errors

---

## 📊 Architecture Overview

```
┌─────────────────┐
│  Flutter App    │
│  (Mobile/Web)   │
└────────┬────────┘
         │ HTTP/HTTPS
         │
    ┌────▼──────────────┐
    │   FastAPI Server  │
    │   (faq_api.py)    │
    └────┬──────────────┘
         │
    ┌────▼──────────────┐
    │    FAQ Bot        │
    │   (faq_bot.py)    │
    └────┬──────────────┘
         │
    ┌────▼──────────────┐
    │  ML Model         │
    │  (faq_model/)     │
    └───────────────────┘
```

---

## ✅ Quick Checklist

Before you start:
- [ ] Python 3.11 installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API tested locally (`http://localhost:8000/docs`)

For Flutter:
- [ ] Flutter SDK installed
- [ ] API is accessible (deployed or local)
- [ ] Have API URL ready

For deployment:
- [ ] Code pushed to GitHub
- [ ] Signed up on Render/Railway (free)
- [ ] Or ngrok installed for quick test

---

## 🎯 Recommended Quick Start

**If you just want to see it working:**

```powershell
# 1. Start API (Terminal 1)
cd C:\Users\sepok\SLMChatCore-1
.\.venv\Scripts\activate.ps1
uvicorn faq_api:app --reload

# 2. Open browser
# Visit: http://localhost:8000/docs
# Try a question in the Swagger UI

# 3. If you want Flutter to connect:
# Terminal 2: ngrok http 8000
# Copy URL → Update Flutter → Run app
```

**That's it! 🎉**

---

## 📖 All Documentation

| File | Purpose |
|------|---------|
| [`README_COMPLETE.md`](README_COMPLETE.md) | Complete overview of everything |
| [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) | Detailed hosting instructions |
| [`FLUTTER_INTEGRATION_COMPLETE.md`](FLUTTER_INTEGRATION_COMPLETE.md) | Complete Flutter setup |
| [`QUICK_DEPLOY.md`](QUICK_DEPLOY.md) | Quick deployment steps |
| [`QUICK_START_FLUTTER.md`](QUICK_START_FLUTTER.md) | Flutter quick start |
| [`CHANGES.md`](CHANGES.md) | What was changed in this update |

---

**Pick your path above and get started! 🚀**
