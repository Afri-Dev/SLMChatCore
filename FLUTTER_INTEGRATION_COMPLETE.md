# 📱 Flutter Integration - Complete Guide

## For the Flutter Developer

This guide helps you integrate the Mental Health FAQ API into your Flutter app.

---

## 📋 Prerequisites

- ✅ API is deployed and accessible (see [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md))
- ✅ You have the API URL (e.g., `https://your-app.onrender.com` or `http://192.168.1.42:8000`)
- ✅ Flutter SDK installed

---

## 🚀 Quick Setup (5 Steps)

### Step 1: Add HTTP Package

In your Flutter project's `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0  # Add this line
```

Run:
```bash
flutter pub get
```

### Step 2: Copy Service Files

Copy these files from `flutter_integration/` to your Flutter project:

```
SLMChatCore-1/flutter_integration/api_service.dart
    → YOUR_FLUTTER_PROJECT/lib/services/api_service.dart

SLMChatCore-1/flutter_integration/faq_screen.dart
    → YOUR_FLUTTER_PROJECT/lib/screens/faq_screen.dart
```

### Step 3: Update API URL

Edit `lib/services/api_service.dart`:

```dart
class ApiService {
  // REPLACE THIS with your actual API URL
  static const String baseUrl = 'https://your-app.onrender.com';
  
  // Examples:
  // Render: 'https://mental-health-faq.onrender.com'
  // Railway: 'https://your-app.up.railway.app'
  // ngrok: 'https://abc123.ngrok.io'
  // Local Network: 'http://192.168.1.42:8000'
  // Android Emulator + Local: 'http://10.0.2.2:8000'
  
  // ... rest stays the same
}
```

### Step 4: Add Screen to Your App

Edit `lib/main.dart`:

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
      home: FaqScreen(),  // Use the FAQ screen
    );
  }
}
```

### Step 5: Run Your App

```bash
flutter run
```

**That's it!** Your app should now connect to the API.

---

## 🔧 Configuration Options

### Environment-Based URLs

Create different configurations for dev/prod:

```dart
class ApiService {
  static const String baseUrl = bool.fromEnvironment('PRODUCTION')
      ? 'https://your-app.onrender.com'  // Production
      : 'http://10.0.2.2:8000';           // Development
}
```

Run with:
```bash
# Development
flutter run

# Production
flutter run --dart-define=PRODUCTION=true
```

### Or use a config file:

**`lib/config/api_config.dart`:**
```dart
class ApiConfig {
  static const bool isProduction = bool.fromEnvironment('PRODUCTION');
  
  static const String productionUrl = 'https://your-app.onrender.com';
  static const String developmentUrl = 'http://10.0.2.2:8000';
  
  static String get baseUrl => isProduction ? productionUrl : developmentUrl;
}
```

**Update `api_service.dart`:**
```dart
import '../config/api_config.dart';

class ApiService {
  static String get baseUrl => ApiConfig.baseUrl;
  // ... rest of code
}
```

---

## 🐛 Troubleshooting

### "SocketException: Failed to connect"

**Cause:** Can't reach the API server

**Solutions:**

1. **Check API is running:**
   - Visit API URL in browser: `https://your-app.onrender.com/health`
   - Should return: `{"status": "healthy", "model_loaded": true}`

2. **Check URL in api_service.dart:**
   ```dart
   // WRONG ❌
   static const String baseUrl = 'http://10.0.2.2:8000';  // Only works for Android emulator
   
   // CORRECT ✅ (for deployed API)
   static const String baseUrl = 'https://your-app.onrender.com';
   ```

3. **For Android Emulator + Local API:**
   - Use `http://10.0.2.2:8000` (NOT `localhost`)
   - Ensure API runs with `--host 0.0.0.0`

4. **For iOS Simulator + Local API:**
   - Use `http://localhost:8000`

5. **For Real Device + Local API:**
   - Use your PC's IP: `http://192.168.1.42:8000`
   - Both devices on same WiFi
   - Firewall allows port 8000

### "TimeoutException: Connection timeout"

**Cause:** Server is slow or sleeping (Render free tier)

**Solutions:**

1. **Increase timeout:**
   ```dart
   final response = await http.post(
     uri,
     headers: {'Content-Type': 'application/json'},
     body: jsonEncode({'question': question}),
   ).timeout(const Duration(seconds: 30));  // Increase from 15 to 30
   ```

2. **Show loading indicator:**
   ```dart
   if (_loading) {
     return Center(
       child: Column(
         mainAxisAlignment: MainAxisAlignment.center,
         children: [
           CircularProgressIndicator(),
           SizedBox(height: 16),
           Text('Waking up server... This may take 30 seconds'),
         ],
       ),
     );
   }
   ```

3. **Upgrade Render to paid tier** ($7/month) for always-on service

### "FormatException: Unexpected character"

**Cause:** API returned non-JSON (likely an error page)

**Solution:**

Add better error handling:

```dart
static Future<QueryResponse> queryFaq(String question) async {
  try {
    final response = await http.post(/* ... */);
    
    if (response.statusCode != 200) {
      throw Exception('API returned ${response.statusCode}: ${response.body}');
    }
    
    // Try to parse JSON
    final json = jsonDecode(response.body);
    return QueryResponse.fromJson(json);
    
  } on FormatException catch (e) {
    throw Exception('Invalid response from server: $e');
  } on SocketException catch (e) {
    throw Exception('Cannot connect to server: $e');
  } on TimeoutException catch (e) {
    throw Exception('Connection timeout: $e');
  }
}
```

### CORS Error (Web)

**Cause:** Browser blocking cross-origin requests

**Solution:**

API already has CORS enabled. If still having issues, check:

1. **Ensure CORS middleware is active** (already done in `faq_api.py`)
2. **Use HTTPS in production** (HTTP → HTTPS causes CORS issues)
3. **Check browser console** for specific CORS error

### "Bot not initialized" Error

**Cause:** Model failed to load on server

**Solutions:**

1. **Check server logs:**
   - Render: Dashboard → Logs
   - Railway: Dashboard → Deployments → Logs

2. **Common causes:**
   - Missing `faq_model/` directory → Ensure it's in git
   - Out of memory → Upgrade to paid tier
   - Missing dependencies → Check `requirements.txt`

3. **Test health endpoint:**
   ```
   GET https://your-app.onrender.com/health
   
   Response:
   {
     "status": "healthy",
     "model_loaded": true  ← Should be true
   }
   ```

---

## 🎨 Customization

### Change Theme Colors

In `faq_screen.dart`:

```dart
// Change from teal to your color
AppBar(
  backgroundColor: Colors.purple,  // Your color
  // ...
)

// Change accent color
CircleAvatar(
  backgroundColor: Colors.purple,  // Your color
  // ...
)
```

### Modify Result Display

```dart
// Show more/less results
final response = await ApiService.queryFaq(
  question,
  topK: 10,        // Default is 5
  minScore: 0.5,   // Only show 50%+ matches
);
```

### Add Custom Fields

If you modify the API to return custom fields:

**API (`faq_api.py`):**
```python
class FAQResult(BaseModel):
    question: str
    answer: str
    score: float
    category: Optional[str] = "General"
    tags: Optional[List[str]] = []  # New field
```

**Flutter (`api_service.dart`):**
```dart
class FAQResult {
  final String question;
  final String answer;
  final double score;
  final String category;
  final List<String> tags;  // New field

  FAQResult({
    required this.question,
    required this.answer,
    required this.score,
    this.category = 'General',
    this.tags = const [],  // New field
  });

  factory FAQResult.fromJson(Map<String, dynamic> json) {
    return FAQResult(
      question: json['question'] ?? '',
      answer: json['answer'] ?? '',
      score: (json['score'] ?? 0.0).toDouble(),
      category: json['category'] ?? 'General',
      tags: (json['tags'] as List?)?.cast<String>() ?? [],  // New field
    );
  }
}
```

---

## 📊 Monitoring & Analytics

### Add Request Logging

```dart
static Future<QueryResponse> queryFaq(String question) async {
  print('🔍 Querying: $question');
  final startTime = DateTime.now();
  
  try {
    final response = await http.post(/* ... */);
    final duration = DateTime.now().difference(startTime);
    print('✅ Response in ${duration.inMilliseconds}ms');
    
    return QueryResponse.fromJson(jsonDecode(response.body));
  } catch (e) {
    print('❌ Error: $e');
    rethrow;
  }
}
```

### Add Firebase Analytics (Optional)

```yaml
# pubspec.yaml
dependencies:
  firebase_analytics: ^10.7.0
```

```dart
// Track queries
FirebaseAnalytics.instance.logEvent(
  name: 'faq_query',
  parameters: {
    'question': question,
    'result_count': response.totalResults,
    'top_score': response.results.first.score,
  },
);
```

---

## 🔒 Security Best Practices

### 1. Don't Hardcode Sensitive URLs

Use environment variables or secure storage:

```dart
// Use flutter_dotenv package
import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiService {
  static String get baseUrl => dotenv.env['API_URL'] ?? 'http://10.0.2.2:8000';
}
```

### 2. Validate Responses

```dart
if (response.results.isEmpty) {
  // Handle no results
}

if (response.results.first.score < 0.3) {
  // Warn about low confidence
}
```

### 3. Rate Limiting (If needed)

```dart
class ApiService {
  static DateTime? _lastRequest;
  static const _minDelay = Duration(seconds: 1);
  
  static Future<QueryResponse> queryFaq(String question) async {
    // Prevent spamming
    if (_lastRequest != null) {
      final elapsed = DateTime.now().difference(_lastRequest!);
      if (elapsed < _minDelay) {
        await Future.delayed(_minDelay - elapsed);
      }
    }
    
    _lastRequest = DateTime.now();
    // ... rest of request
  }
}
```

---

## 📚 API Reference

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Check API health |
| `/stats` | GET | Get FAQ database stats |
| `/faq` | POST | Query FAQ |

### Request Format

```dart
POST /faq
Content-Type: application/json

{
  "question": "What is anxiety?",
  "top_k": 5,
  "min_score": 0.0
}
```

### Response Format

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

---

## ✅ Checklist

Before releasing your app:

- [ ] API is deployed and accessible
- [ ] Base URL is updated in `api_service.dart`
- [ ] Health check works: `/health` returns `model_loaded: true`
- [ ] Test with real questions
- [ ] Error handling works (no internet, timeout, etc.)
- [ ] Loading states are clear to users
- [ ] Empty states guide users
- [ ] HTTPS in production (not HTTP)
- [ ] Analytics/logging added (optional)
- [ ] Tested on real device, not just emulator

---

## 🎉 You're Ready!

Your Flutter app is now connected to the Mental Health FAQ API.

**Questions?** Check:
- [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) - API hosting
- [`flutter_integration/README.md`](flutter_integration/README.md) - More Flutter details
- API Docs: `https://your-api.com/docs`

**Happy coding!** 🚀
