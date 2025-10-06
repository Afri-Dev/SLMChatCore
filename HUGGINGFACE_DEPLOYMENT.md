# 🚀 Hugging Face Spaces Deployment Guide

## ✅ Files Created

Your project is now ready for Hugging Face Spaces deployment with proper error handling!

### 1. **app.py** (Root Directory)
- ✅ Fixed error handlers using `JSONResponse`
- ✅ Port set to 7860 (HF Spaces default)
- ✅ Proper exception handling to avoid "'dict' object is not callable" error

### 2. **Dockerfile** (Optimized for HF Spaces)
- ✅ Python 3.11 slim base image
- ✅ Pre-downloads model at build time
- ✅ Health check endpoint
- ✅ Port 7860 exposed

### 3. **.dockerignore** (Build Optimization)
- ✅ Excludes unnecessary files
- ✅ Reduces build time and image size

---

## 🔧 The Fix Applied

### ❌ WRONG (Causes TypeError):
```python
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return {"error": str(exc)}  # This causes 'dict' object is not callable!
```

### ✅ CORRECT (Now Applied):
```python
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )
```

---

## 🚀 Deploy to Hugging Face Spaces

### Method 1: Web UI (Easiest - 5 minutes)

1. **Go to** https://huggingface.co/spaces
2. **Click** "Create new Space"
3. **Configure:**
   - Name: `mental-health-faq`
   - License: MIT
   - SDK: **Docker**
   - Hardware: CPU Basic (Free)
4. **Upload files:**
   - `app.py`
   - `faq_bot.py`
   - `Dockerfile`
   - `requirements.txt`
   - `Mental_Health_FAQ.csv`
   - `faq_model/` folder
5. **Click** "Commit to main"

**Done!** Your API will be live at:
```
https://YOUR_USERNAME-mental-health-faq.hf.space
```

---

### Method 2: Git Push (For developers)

```powershell
# 1. Install git-lfs (for large model files)
git lfs install

# 2. Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/mental-health-faq

# 3. Push to HF Spaces
git add app.py Dockerfile .dockerignore
git commit -m "Deploy to Hugging Face Spaces with fixed error handlers"
git push hf main
```

---

## 🧪 Test Your Deployment

### 1. Health Check
```powershell
curl https://YOUR_USERNAME-mental-health-faq.hf.space/health
```

### 2. Query FAQ
```powershell
curl -X POST https://YOUR_USERNAME-mental-health-faq.hf.space/faq `
  -H "Content-Type: application/json" `
  -d '{"question": "How do I manage anxiety?", "top_k": 3}'
```

### 3. API Documentation
Visit: `https://YOUR_USERNAME-mental-health-faq.hf.space/docs`

---

## 🔄 Update Your Flutter App

In `flutter_integration/api_service.dart`:

```dart
class ApiService {
  static const String baseUrl = 'https://YOUR_USERNAME-mental-health-faq.hf.space';
  // ... rest of your code
}
```

---

## 📊 Why Hugging Face Spaces > Render

| Feature | HF Spaces | Render (Free) |
|---------|-----------|---------------|
| **RAM** | 16 GB ✅ | 512 MB ❌ |
| **CPU** | 2 vCPU ✅ | Shared ⚠️ |
| **Uptime** | Always on ✅ | Sleeps after 15 min ❌ |
| **Build Time** | 5-10 min ✅ | 10-15 min ⚠️ |
| **ML Optimized** | Yes ✅ | No ❌ |
| **Port Issues** | None ✅ | Yes (your error) ❌ |
| **Cold Start** | 10-15s ✅ | 30-60s ❌ |

---

## 🐛 Error Handler Fix Details

The error **"'dict' object is not callable"** occurs when FastAPI exception handlers return plain dictionaries instead of Response objects.

### What Was Wrong:
```python
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Not found"}  # ❌ Plain dict
```

### What's Fixed Now:
```python
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(  # ✅ Proper Response object
        status_code=404,
        content={"error": "Not found"}
    )
```

**All error handlers in your `app.py` now use `JSONResponse`!** 🎉

---

## 📝 Files Changed

```
C:\Users\sepok\SLMChatCore-1\
├── app.py                  ✅ NEW - Main API file with fixed error handlers
├── Dockerfile              ✅ UPDATED - Optimized for HF Spaces
├── .dockerignore           ✅ NEW - Build optimization
└── ReadMe\
    └── app.py              ✅ UPDATED - Fixed error handlers
```

---

## 🎯 Next Steps

1. **Test locally (optional):**
   ```powershell
   python app.py
   # Visit: http://localhost:7860/docs
   ```

2. **Deploy to HF Spaces** (see Method 1 or 2 above)

3. **Update Flutter app** with new API URL

4. **Monitor deployment:**
   - Check build logs in HF Spaces
   - Test `/health` endpoint
   - Try sample queries

---

## 💡 Tips

- **Build time:** First build takes 10-15 min (downloads model)
- **Subsequent builds:** 2-3 min (cached layers)
- **Free tier limits:** Always on, no cold starts!
- **Custom domain:** Available with HF Pro ($9/month)

---

## 🆘 Troubleshooting

### Build fails?
```powershell
# Check requirements.txt includes:
fastapi>=0.118.0
uvicorn[standard]>=0.35.0
sentence-transformers>=3.1.1
```

### Model not loading?
- Check `faq_model/` folder is uploaded
- Verify `Mental_Health_FAQ.csv` exists
- Check HF Spaces logs

### Port timeout?
- ✅ Already fixed! Port 7860 is correctly set in Dockerfile and app.py

---

**Ready to deploy? Follow Method 1 above for the easiest path!** 🚀
