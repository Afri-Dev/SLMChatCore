# 🚀 Quick Start - Connect Flutter to API

## For You (Python/API Side)

### 1. Start the API Server
```powershell
cd C:\Users\sepok\SLMChatCore-1
.\.venv\Scripts\activate.ps1
uvicorn faq_api:app --reload --host 0.0.0.0 --port 8000
```

### 2. Run Diagnostics
```powershell
# In a new terminal
cd C:\Users\sepok\SLMChatCore-1
python diagnose_connection.py
```

This will tell you:
- ✅ If API is running correctly
- ✅ Your PC's IP address
- ✅ What baseUrl to use in Flutter
- ✅ If firewall is blocking connections

---

## For Your Flutter Developer

### Quick Fix Checklist

**File to edit:** `lib/services/api_service.dart`

**Find this line:**
```dart
static const String baseUrl = 'http://10.0.2.2:8000';
```

**Change based on platform:**

| Platform | Change to |
|----------|-----------|
| Android Emulator | `'http://10.0.2.2:8000'` |
| iOS Simulator | `'http://localhost:8000'` |
| Real Device | `'http://YOUR_PC_IP:8000'` |

**Example for real device:**
```dart
static const String baseUrl = 'http://192.168.1.42:8000';  // Use IP from diagnostic
```

**Then:**
1. Save the file
2. Press `R` in Flutter terminal to hot restart
3. Click the cloud icon in app to test connection

---

## Complete Instructions

👉 **Give your Flutter developer this file:**
   - `FLUTTER_TROUBLESHOOTING.md` (has everything they need)

👉 **Run the diagnostic tool:**
   - `python diagnose_connection.py`

👉 **Share the diagnostic output** with your Flutter developer

---

## Common Issues & Quick Fixes

### ❌ "Connection refused"
**Fix:** Start the API server with the uvicorn command above

### ❌ "Network unreachable" (Real Device)
**Fix:** 
1. Run diagnostic: `python diagnose_connection.py`
2. If it says firewall is blocking, run in PowerShell as Admin:
   ```powershell
   New-NetFirewallRule -DisplayName "FAQ API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
   ```

### ❌ Android Emulator can't connect
**Fix:** Use `http://10.0.2.2:8000` (not localhost)

### ❌ iOS Simulator can't connect
**Fix:** Use `http://localhost:8000`

---

## Alternative: Use ngrok (Easiest)

If firewall is too complex:

```powershell
# Download from https://ngrok.com/download
ngrok http 8000
```

You'll get: `https://abc123.ngrok.io`

**Tell your Flutter dev to use:**
```dart
static const String baseUrl = 'https://abc123.ngrok.io';  // No port needed
```

---

## Test URLs

After starting the server, open these in browser:

- http://localhost:8000/docs - Interactive API documentation
- http://localhost:8000/health - Quick health check
- http://YOUR_IP:8000/health - Test from network

---

**That's it! Run the diagnostic and share the output.** 🎉
