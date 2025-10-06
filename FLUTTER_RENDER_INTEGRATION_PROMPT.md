# Flutter App Integration with Render Deployment - Detailed Instructions

## 🎯 Objective
Modify the existing Flutter FAQ chatbot application to connect exclusively to the deployed SLM (Small Language Model) API hosted on Render at `https://slmchatcore.onrender.com`.

## 📋 Critical Requirements

### 1. Base URL Configuration
**REQUIRED CHANGES:**
- Set the base URL to: `https://slmchatcore.onrender.com`
- **DO NOT** include port numbers (no `:8000` or any port)
- **DO NOT** include trailing slashes
- **DO NOT** use `localhost` or `127.0.0.1` anywhere
- **DO NOT** use `http://` - only use `https://`

### 2. File to Modify: `api_service.dart`

**Location:** `lib/services/api_service.dart` or `flutter_integration/api_service.dart`

**Exact Changes Required:**

```dart
class ApiService {
  // ✅ CORRECT - Use this exact URL
  static const String baseUrl = 'https://slmchatcore.onrender.com';
  
  // ❌ WRONG - Do NOT use any of these:
  // static const String baseUrl = 'http://localhost:8000';
  // static const String baseUrl = 'http://127.0.0.1:8000';
  // static const String baseUrl = 'http://10.0.2.2:8000';
  // static const String baseUrl = 'https://slmchatcore.onrender.com:8000';
  // static const String baseUrl = 'https://slmchatcore.onrender.com/';
  
  // Rest of the class remains unchanged
}
```

### 3. API Endpoints to Use

The deployed API provides these endpoints:

| Endpoint | Method | Purpose | Full URL |
|----------|--------|---------|----------|
| `/health` | GET | Check API health | `https://slmchatcore.onrender.com/health` |
| `/faq` | POST | Query the FAQ bot | `https://slmchatcore.onrender.com/faq` |
| `/api-info` | GET | Get API information | `https://slmchatcore.onrender.com/api-info` |
| `/docs` | GET | Interactive API docs | `https://slmchatcore.onrender.com/docs` |

### 4. Timeout Configuration

**CRITICAL:** Render's free tier may sleep after inactivity. First request can take 30-60 seconds.

**Required Changes in `api_service.dart`:**

```dart
static Future<QueryResponse> queryFaq(
  String question, {
  int topK = 5,
  double minScore = 0.0,
}) async {
  final uri = Uri.parse('$baseUrl/faq');
  
  try {
    final response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'question': question,
        'top_k': topK,
        'min_score': minScore,
      }),
    ).timeout(
      const Duration(seconds: 90),  // ⚠️ MUST be at least 60 seconds
      onTimeout: () {
        throw TimeoutException('Server took too long to respond. It may be starting up.');
      },
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return QueryResponse.fromJson(data);
    } else {
      throw Exception('Server returned ${response.statusCode}: ${response.body}');
    }
  } on SocketException {
    throw Exception('No internet connection. Please check your network.');
  } on TimeoutException catch (e) {
    throw Exception(e.message);
  } catch (e) {
    throw Exception('Failed to connect to server: $e');
  }
}
```

### 5. Health Check Implementation

**Add this method to `ApiService` class:**

```dart
static Future<Map<String, dynamic>> checkHealth() async {
  final uri = Uri.parse('$baseUrl/health');
  
  try {
    final response = await http.get(uri).timeout(
      const Duration(seconds: 30),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Health check failed with status ${response.statusCode}');
    }
  } catch (e) {
    throw Exception('Cannot reach server: $e');
  }
}
```

### 6. UI Loading States

**Required User Feedback:**

Add proper loading indicators that inform users about potential delays:

```dart
// In your StatefulWidget's build method or query screen

if (_isLoading) {
  return Center(
    child: Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        CircularProgressIndicator(),
        SizedBox(height: 20),
        Text(
          'Processing your question...',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
        ),
        SizedBox(height: 8),
        Text(
          'First query may take 30-60 seconds',
          style: TextStyle(fontSize: 12, color: Colors.grey[600]),
        ),
        SizedBox(height: 4),
        Text(
          '(Server is waking up)',
          style: TextStyle(fontSize: 11, color: Colors.grey[500]),
        ),
      ],
    ),
  );
}
```

### 7. Connection Status Indicator

**Implement a status checker:**

```dart
class ConnectionStatus extends StatefulWidget {
  @override
  _ConnectionStatusState createState() => _ConnectionStatusState();
}

class _ConnectionStatusState extends State<ConnectionStatus> {
  bool _isConnected = false;
  bool _isChecking = true;

  @override
  void initState() {
    super.initState();
    _checkConnection();
  }

  Future<void> _checkConnection() async {
    setState(() => _isChecking = true);
    
    try {
      final health = await ApiService.checkHealth();
      setState(() {
        _isConnected = health['status'] == 'healthy';
        _isChecking = false;
      });
    } catch (e) {
      setState(() {
        _isConnected = false;
        _isChecking = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isChecking) {
      return Icon(Icons.cloud_queue, color: Colors.orange);
    }
    
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(
          _isConnected ? Icons.cloud_done : Icons.cloud_off,
          color: _isConnected ? Colors.green : Colors.red,
          size: 20,
        ),
        SizedBox(width: 4),
        Text(
          _isConnected ? 'Connected' : 'Offline',
          style: TextStyle(
            fontSize: 12,
            color: _isConnected ? Colors.green : Colors.red,
          ),
        ),
      ],
    );
  }
}
```

### 8. Error Handling

**Required error messages for users:**

```dart
void _handleError(dynamic error) {
  String userMessage;
  
  if (error.toString().contains('No internet')) {
    userMessage = 'No internet connection. Please check your network and try again.';
  } else if (error.toString().contains('timeout') || error.toString().contains('starting up')) {
    userMessage = 'Server is starting up. Please wait a moment and try again.';
  } else if (error.toString().contains('SocketException')) {
    userMessage = 'Cannot reach server. Please check your internet connection.';
  } else {
    userMessage = 'An error occurred: ${error.toString()}';
  }
  
  setState(() {
    _error = userMessage;
    _isLoading = false;
  });
  
  // Show snackbar
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: Text(userMessage),
      backgroundColor: Colors.red[700],
      duration: Duration(seconds: 5),
      action: SnackBarAction(
        label: 'RETRY',
        textColor: Colors.white,
        onPressed: () => _retryQuery(),
      ),
    ),
  );
}
```

## 🔧 Testing Checklist

Before submitting the modified app, verify:

### ✅ Pre-Flight Checks

1. **URL Verification**
   ```dart
   print(ApiService.baseUrl); // Should print: https://slmchatcore.onrender.com
   ```

2. **Browser Test**
   - Open: https://slmchatcore.onrender.com/health
   - Expected response: `{"status":"healthy","message":"FAQ Bot is ready","model_loaded":true}`

3. **API Documentation**
   - Visit: https://slmchatcore.onrender.com/docs
   - Test the `/faq` endpoint with a sample question

### ✅ Flutter App Tests

1. **Health Check Test**
   ```dart
   void testHealthCheck() async {
     try {
       final health = await ApiService.checkHealth();
       print('Health check passed: $health');
     } catch (e) {
       print('Health check failed: $e');
     }
   }
   ```

2. **Query Test**
   ```dart
   void testQuery() async {
     try {
       final response = await ApiService.queryFaq('What is depression?');
       print('Query succeeded with ${response.results.length} results');
     } catch (e) {
       print('Query failed: $e');
     }
   }
   ```

3. **Timeout Test**
   - First query after 15+ minutes of inactivity should still work (but take longer)
   - Verify loading indicator shows appropriate message

4. **Network Error Test**
   - Turn off internet
   - Verify appropriate error message appears

5. **Visual Tests**
   - Connection status indicator shows green/connected
   - Loading states display correctly
   - Error messages are user-friendly
   - Retry functionality works

## 📱 Platform-Specific Notes

### Android
- No special configuration needed
- HTTPS works by default
- If using HTTP (DON'T!), you'd need network security config

### iOS
- HTTPS works by default
- No App Transport Security changes needed
- Ensure proper internet permissions in Info.plist

### Web
- CORS is already configured on the server
- Should work without additional changes

## 🚫 Common Mistakes to Avoid

1. **Don't hardcode localhost**
   ```dart
   // ❌ WRONG
   final url = 'http://localhost:8000/faq';
   ```

2. **Don't add port numbers to Render URL**
   ```dart
   // ❌ WRONG
   static const String baseUrl = 'https://slmchatcore.onrender.com:8000';
   ```

3. **Don't use HTTP instead of HTTPS**
   ```dart
   // ❌ WRONG
   static const String baseUrl = 'http://slmchatcore.onrender.com';
   ```

4. **Don't set too short timeouts**
   ```dart
   // ❌ WRONG - Render needs more time
   .timeout(const Duration(seconds: 10))
   ```

5. **Don't forget to handle errors**
   ```dart
   // ❌ WRONG - Silent failure
   try {
     await ApiService.queryFaq(question);
   } catch (e) {
     // Empty catch - user sees nothing!
   }
   ```

## 📦 Required Dependencies

Ensure these are in `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0  # For API calls
  connectivity_plus: ^5.0.0  # For checking internet connection (optional but recommended)

dev_dependencies:
  flutter_test:
    sdk: flutter
```

Run after adding dependencies:
```bash
flutter pub get
```

## 🎯 Final Validation

Before considering the task complete:

1. ✅ Base URL is set to `https://slmchatcore.onrender.com` (no port, no trailing slash)
2. ✅ All API calls use the correct base URL
3. ✅ Timeout is set to at least 60 seconds
4. ✅ Loading indicators inform users about potential delays
5. ✅ Error handling provides clear, actionable messages
6. ✅ Connection status indicator is visible
7. ✅ Health check endpoint is implemented
8. ✅ All tests pass (health check, query, error handling)
9. ✅ App works on both WiFi and mobile data
10. ✅ First query after server sleep completes successfully (even if slow)

## 📞 API Response Examples

### Successful Health Check
```json
{
  "status": "healthy",
  "message": "FAQ Bot is ready",
  "model_loaded": true
}
```

### Successful FAQ Query
```json
{
  "question": "What is depression?",
  "top_results": [
    {
      "question": "What is depression?",
      "answer": "Depression is a mood disorder...",
      "score": 0.95,
      "question_id": "q_001"
    }
  ],
  "num_results": 1
}
```

### Error Response
```json
{
  "detail": "Error message here"
}
```

## 🔍 Debugging Tips

If connection fails:

1. **Check Render Status**
   - Visit: https://slmchatcore.onrender.com/health in browser
   - If this fails, the server is down (not an app issue)

2. **Check Flutter Logs**
   ```bash
   flutter run -v
   ```

3. **Test with curl**
   ```bash
   curl -X POST https://slmchatcore.onrender.com/faq \
     -H "Content-Type: application/json" \
     -d '{"question":"What is anxiety?","top_k":3,"min_score":0.0}'
   ```

4. **Enable Debug Logging**
   ```dart
   void debugApiCall(String endpoint, dynamic data) {
     if (kDebugMode) {
       print('API Call: $endpoint');
       print('Data: $data');
     }
   }
   ```

## 📝 Summary

**Single Most Important Change:**
```dart
// In api_service.dart
static const String baseUrl = 'https://slmchatcore.onrender.com';
```

That's it! Everything else is about making the user experience smooth when dealing with Render's cold start delays.

---

## ✨ Expected Behavior After Implementation

- ✅ App connects to remote server successfully
- ✅ First query may take 30-60 seconds (with appropriate loading message)
- ✅ Subsequent queries are fast (< 2 seconds)
- ✅ Connection status shows green indicator
- ✅ Errors are handled gracefully with user-friendly messages
- ✅ Works on all platforms (Android, iOS, Web)
- ✅ No localhost or port numbers in code

**Target URL: `https://slmchatcore.onrender.com`**
**Protocol: HTTPS only**
**Timeout: Minimum 60 seconds**
**Port: None (handled by Render)**

Good luck with the integration! 🚀
