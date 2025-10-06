---
title: Mental Health FAQ Bot
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# 🧠 Mental Health FAQ API

A REST API for mental health FAQ retrieval using sentence transformers and semantic search.

## 🚀 Quick Start

### API Endpoints

- **Health Check:** `GET /health`
- **Query FAQ:** `POST /faq`
- **Statistics:** `GET /stats`
- **Documentation:** `/docs`

### Example Usage

```bash
curl -X POST https://YOUR-SPACE-URL.hf.space/faq \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I manage anxiety?",
    "top_k": 3,
    "min_score": 0.5
  }'
```

### Response Format

```json
{
  "success": true,
  "results": [
    {
      "question": "What are some ways to manage anxiety?",
      "answer": "Practice deep breathing, meditation, regular exercise...",
      "score": 0.8542,
      "category": "Anxiety"
    }
  ],
  "query": "How do I manage anxiety?",
  "total_results": 3
}
```

## 🔧 Technology Stack

- **Framework:** FastAPI
- **ML Model:** sentence-transformers/all-MiniLM-L6-v2
- **Similarity Search:** Cosine similarity with numpy
- **Deployment:** Docker on Hugging Face Spaces

## 📊 Features

- ✅ Semantic search for mental health questions
- ✅ CORS enabled for web/mobile apps
- ✅ Adjustable top-k results
- ✅ Minimum similarity score filtering
- ✅ Category-based organization
- ✅ RESTful API with OpenAPI docs

## 🧪 Integration

### Flutter/Dart

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<Map<String, dynamic>> queryFAQ(String question) async {
  final response = await http.post(
    Uri.parse('https://YOUR-SPACE-URL.hf.space/faq'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'question': question,
      'top_k': 3,
      'min_score': 0.5
    }),
  );
  return jsonDecode(response.body);
}
```

### Python

```python
import requests

response = requests.post(
    'https://YOUR-SPACE-URL.hf.space/faq',
    json={
        'question': 'How do I manage anxiety?',
        'top_k': 3,
        'min_score': 0.5
    }
)
print(response.json())
```

### JavaScript

```javascript
const response = await fetch('https://YOUR-SPACE-URL.hf.space/faq', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    question: 'How do I manage anxiety?',
    top_k: 3,
    min_score: 0.5
  })
});
const data = await response.json();
console.log(data);
```

## 📝 API Parameters

### POST /faq

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| question | string | required | User's question |
| top_k | integer | 3 | Number of results (1-10) |
| min_score | float | 0.0 | Minimum similarity score (0.0-1.0) |

## 🏥 Use Cases

- Mental health chatbots
- FAQ systems
- Support applications
- Educational tools
- Wellness platforms

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! This is an open-source mental health support tool.

## ⚠️ Disclaimer

This API provides general mental health information. For medical advice or emergencies, please consult qualified healthcare professionals or call emergency services.

---

Built with ❤️ using FastAPI and Hugging Face Spaces
