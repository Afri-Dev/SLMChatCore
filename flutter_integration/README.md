# Flutter Integration Guide

This directory contains Flutter/Dart files to integrate with the Mental Health FAQ API.

## Files

- **`api_service.dart`**: API service with models and HTTP methods
- **`faq_screen.dart`**: Complete Flutter UI screen with search and results display

## Setup Instructions

### 1. Add HTTP Package to Flutter Project

In your Flutter project's `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0  # Add this line
```

Then run:
```bash
flutter pub get
```

### 2. Copy Files to Your Flutter Project

Copy these files to your Flutter project:
- `api_service.dart` → `lib/services/api_service.dart`
- `faq_screen.dart` → `lib/screens/faq_screen.dart`

### 3. Update Base URL in `api_service.dart`

Change the `baseUrl` based on your environment:

```dart
// For Android Emulator
static const String baseUrl = 'http://10.0.2.2:8000';

// For iOS Simulator
static const String baseUrl = 'http://localhost:8000';

// For Real Device (replace with your PC's IP)
static const String baseUrl = 'http://192.168.1.42:8000';

// For Production
static const String baseUrl = 'https://your-domain.com';
```

### 4. Add the Screen to Your App

In your `main.dart`:

```dart
import 'package:flutter/material.dart';
import 'screens/faq_screen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mental Health FAQ',
      theme: ThemeData(
        primarySwatch: Colors.teal,
      ),
      home: FaqScreen(),
    );
  }
}
```

### 5. Start the Python API Server

In your SLMChatCore-1 directory:

```bash
# Activate virtual environment (Windows)
.\.venv\Scripts\activate.ps1

# Start the server
uvicorn faq_api:app --reload --host 0.0.0.0 --port 8000
```

### 6. Test the Connection

The app will show a cloud icon in the app bar:
- ✅ **Green cloud**: Server connected
- ❌ **Red cloud**: Server disconnected

## Features

### API Service Features
- ✅ Query FAQ with customizable `top_k` and `min_score`
- ✅ Health check endpoint
- ✅ Stats endpoint
- ✅ Proper error handling with timeouts
- ✅ Structured models (QueryResponse, FAQResult)

### UI Features
- ✅ Real-time health status indicator
- ✅ Search with question input
- ✅ Color-coded confidence scores (green/orange/red)
- ✅ Expandable result cards
- ✅ Category badges
- ✅ Error and warning messages
- ✅ Empty state guidance
- ✅ Refresh button
- ✅ Beautiful Material Design UI

## API Response Format

The API returns structured JSON:

```json
{
  "success": true,
  "query": "What is anxiety?",
  "total_results": 3,
  "message": null,
  "results": [
    {
      "question": "What is anxiety?",
      "answer": "Anxiety is a normal emotion...",
      "score": 0.9234,
      "category": "General"
    }
  ]
}
```

## Troubleshooting

### Cannot Connect to Server

1. **Check if server is running**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **For Android Emulator**: Use `10.0.2.2` instead of `localhost`

3. **For Real Device**: 
   - Find your PC's IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
   - Allow port 8000 through Windows Firewall
   - Use `http://YOUR_PC_IP:8000`

4. **Use ngrok for quick testing**:
   ```bash
   ngrok http 8000
   ```
   Then use the ngrok URL in `api_service.dart`

### Model Not Loading

Check the server logs for errors. Ensure:
- `faq_model` directory exists
- All model files are present
- Dependencies are installed: `pip install -r requirements.txt`

### CORS Errors

The API already has CORS enabled with `allow_origins=["*"]`. For production, restrict this to your domain.

## Production Deployment

### Deploy Python API

**Option 1: Render.com (Free)**
1. Push code to GitHub
2. Create new Web Service on Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn faq_api:app --host 0.0.0.0 --port $PORT`

**Option 2: Railway.app**
1. Connect GitHub repo
2. Railway auto-detects Python
3. Set start command in `Procfile`

**Option 3: Google Cloud Run / AWS Lambda**
For serverless deployment with auto-scaling

### Update Flutter App
Change `baseUrl` to your production URL and rebuild:
```bash
flutter build apk  # Android
flutter build ios  # iOS
```

## Next Steps

- Add Firebase Authentication for user login
- Store query history in Firestore
- Add favorite/bookmark functionality
- Implement caching for offline support
- Add analytics to track popular questions
- Implement rate limiting on API
