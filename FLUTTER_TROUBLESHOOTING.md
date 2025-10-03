# 🔧 Flutter App API Connection Troubleshooting Guide

## Problem: Flutter app cannot connect to the Python API server

This guide will help you fix connectivity issues between your Flutter app and the FAQ API.

---

## ✅ STEP 1: Verify API Server is Running

**In your Python project terminal (`C:\Users\sepok\SLMChatCore-1`):**

```powershell
# 1. Activate virtual environment
.\.venv\Scripts\activate.ps1

# 2. Start the API server with correct host binding
uvicorn faq_api:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**Test the server is accessible:**
```powershell
# Open a new terminal and test
curl http://localhost:8000/health
```

---

## ✅ STEP 2: Find Your PC's IP Address

**Windows PowerShell:**
```powershell
ipconfig
```

**Look for:**
```
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.1.42    <-- THIS IS YOUR IP
```

**macOS/Linux:**
```bash
ifconfig | grep "inet "
```

**Write down your IP address:** `___________________`

---

## ✅ STEP 3: Update Flutter App Configuration

### For Android Emulator:

**File:** `lib/services/api_service.dart`

```dart
class ApiService {
  // Use 10.0.2.2 for Android Emulator (maps to localhost on host machine)
  static const String baseUrl = 'http://10.0.2.2:8000';
  
  // ... rest of code
}
```

### For iOS Simulator:

**File:** `lib/services/api_service.dart`

```dart
class ApiService {
  // Use localhost for iOS Simulator
  static const String baseUrl = 'http://localhost:8000';
  
  // ... rest of code
}
```

### For Real Device (Phone/Tablet):

**File:** `lib/services/api_service.dart`

```dart
class ApiService {
  // Replace with YOUR actual PC IP from Step 2
  static const String baseUrl = 'http://192.168.1.42:8000';  // <-- CHANGE THIS
  
  // ... rest of code
}
```

---

## ✅ STEP 4: Configure Windows Firewall (for Real Device)

If using a **real device**, you must allow port 8000 through Windows Firewall:

**Option A: Temporary (Quick Test):**
```powershell
# Run as Administrator in PowerShell
New-NetFirewallRule -DisplayName "FAQ API Server" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

**Option B: Windows Firewall GUI:**
1. Open **Windows Defender Firewall** → **Advanced Settings**
2. Click **Inbound Rules** → **New Rule**
3. Select **Port** → Next
4. Select **TCP** → Specific local ports: **8000** → Next
5. Select **Allow the connection** → Next
6. Check all profiles → Next
7. Name it "FAQ API Port 8000" → Finish

---

## ✅ STEP 5: Verify Device and PC are on Same Network

**Both your PC and device MUST be on the same WiFi network.**

- PC WiFi: `___________________`
- Device WiFi: `___________________`

**They must match!**

---

## ✅ STEP 6: Test Connection from Flutter App

Add this test button to your Flutter app temporarily:

**File:** `lib/screens/faq_screen.dart`

Add in the AppBar actions:

```dart
appBar: AppBar(
  title: const Text('Mental Health FAQ'),
  actions: [
    // Health indicator
    IconButton(
      icon: Icon(
        _serverHealthy ? Icons.cloud_done : Icons.cloud_off,
        color: _serverHealthy ? Colors.white : Colors.red,
      ),
      onPressed: _checkHealth,
      tooltip: _serverHealthy ? 'Server Connected' : 'Server Disconnected',
    ),
    // TEST CONNECTION BUTTON - Add this
    IconButton(
      icon: const Icon(Icons.network_check),
      onPressed: () async {
        try {
          final health = await ApiService.checkHealth();
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('✅ Connected! Status: ${health['status']}'),
              backgroundColor: Colors.green,
            ),
          );
        } catch (e) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('❌ Error: $e'),
              backgroundColor: Colors.red,
              duration: const Duration(seconds: 5),
            ),
          );
        }
      },
      tooltip: 'Test Connection',
    ),
  ],
),
```

---

## ✅ STEP 7: Enable Internet Permission (Android)

**File:** `android/app/src/main/AndroidManifest.xml`

Add this line BEFORE `<application>`:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <!-- Add this line -->
    <uses-permission android:name="android.permission.INTERNET" />
    
    <application
        ...
```

---

## ✅ STEP 8: Allow Clear Text Traffic (Android Development Only)

**File:** `android/app/src/main/AndroidManifest.xml`

Update the `<application>` tag:

```xml
<application
    android:label="your_app_name"
    android:usesCleartextTraffic="true"
    android:icon="@mipmap/ic_launcher">
```

**⚠️ Security Note:** Remove `usesCleartextTraffic="true"` in production. Use HTTPS instead.

---

## ✅ STEP 9: iOS Configuration (if using iOS)

**File:** `ios/Runner/Info.plist`

Add this configuration to allow HTTP (development only):

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
    <key>NSAllowsLocalNetworking</key>
    <true/>
</dict>
```

---

## ✅ STEP 10: Alternative - Use ngrok (Quick Solution)

If firewall configuration is too complex, use **ngrok** to expose your API:

**Terminal 1 (Start API):**
```powershell
uvicorn faq_api:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 (Start ngrok):**
```powershell
# Download ngrok from https://ngrok.com/download
ngrok http 8000
```

**You'll get a public URL like:**
```
Forwarding: https://abc123.ngrok.io -> http://localhost:8000
```

**Update Flutter:**
```dart
class ApiService {
  static const String baseUrl = 'https://abc123.ngrok.io';  // Use ngrok URL
}
```

---

## 🐛 Common Error Messages & Solutions

### Error: "Failed to establish a new connection"
- ✅ Check API server is running
- ✅ Verify you're using correct IP address
- ✅ Ensure device and PC are on same WiFi

### Error: "Connection refused"
- ✅ API server not running or crashed
- ✅ Wrong port number (should be 8000)
- ✅ Check API server logs for errors

### Error: "Network is unreachable"
- ✅ Device not on same WiFi as PC
- ✅ Firewall blocking port 8000
- ✅ VPN or proxy interfering

### Error: "Connection timeout"
- ✅ Firewall blocking connection
- ✅ Wrong IP address
- ✅ PC hibernated/sleeping

### Error: "SSL certificate verify failed"
- ✅ Using https:// instead of http://
- ✅ Change to http:// for local development

---

## 📋 Quick Checklist

Copy this checklist and mark items as completed:

```
[ ] API server is running on PC (uvicorn command)
[ ] Server responds to http://localhost:8000/health on PC
[ ] Found PC's IP address (ipconfig)
[ ] Updated api_service.dart with correct baseUrl
[ ] Device and PC on same WiFi network
[ ] Windows Firewall allows port 8000 (for real device)
[ ] Android INTERNET permission added to AndroidManifest.xml
[ ] Android usesCleartextTraffic="true" enabled (development)
[ ] Flutter app restarted after changes (flutter run)
[ ] Tested connection button shows success
```

---

## 🧪 Test Commands

**On PC (where API runs):**
```powershell
# Test API locally
curl http://localhost:8000/health

# Test API from network (replace with your IP)
curl http://192.168.1.42:8000/health
```

**From another device on same network:**
```bash
# Replace with your PC's IP
curl http://192.168.1.42:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "message": "FAQ Bot is ready",
  "model_loaded": true
}
```

---

## 📱 Summary of baseUrl by Platform

| Platform | baseUrl to use |
|----------|----------------|
| Android Emulator | `http://10.0.2.2:8000` |
| iOS Simulator | `http://localhost:8000` |
| Real Device (WiFi) | `http://YOUR_PC_IP:8000` |
| Production | `https://your-domain.com` |

---

## 🚀 After Fixing - Hot Restart Flutter

```bash
# In Flutter project directory
flutter clean
flutter pub get
flutter run
```

Or press **R** in the terminal where Flutter is running to hot restart.

---

## 💡 Pro Tips

1. **Use ngrok for quick testing** - avoids firewall issues
2. **Check API logs** - The uvicorn terminal shows all requests
3. **Test on PC first** - Visit http://localhost:8000/docs
4. **One change at a time** - Don't change multiple things simultaneously
5. **Restart Flutter app** - After changing baseUrl, always hot restart

---

## 📞 Still Not Working?

If you've completed all steps and it's still not working, provide these details:

```
1. Platform: [ ] Android Emulator [ ] iOS Simulator [ ] Real Device
2. PC IP Address: ___________________
3. baseUrl in api_service.dart: ___________________
4. Can you access http://localhost:8000/health on PC? [ ] Yes [ ] No
5. Firewall rule added? [ ] Yes [ ] No [ ] Not applicable
6. Error message from Flutter app: 
   ___________________________________________________

7. API server logs (last 10 lines):
   ___________________________________________________
```

---

**Good luck! 🎉 Once connected, you'll see the green cloud icon in your Flutter app.**
