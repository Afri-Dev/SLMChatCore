import 'dart:convert';
import 'package:http/http.dart' as http;

// Models
class FAQResult {
  final String question;
  final String answer;
  final double score;
  final String category;

  FAQResult({
    required this.question,
    required this.answer,
    required this.score,
    this.category = 'General',
  });

  factory FAQResult.fromJson(Map<String, dynamic> json) {
    return FAQResult(
      question: json['question'] ?? '',
      answer: json['answer'] ?? '',
      score: (json['score'] ?? 0.0).toDouble(),
      category: json['category'] ?? 'General',
    );
  }
}

class QueryResponse {
  final bool success;
  final String query;
  final List<FAQResult> results;
  final int totalResults;
  final String? message;

  QueryResponse({
    required this.success,
    required this.query,
    required this.results,
    required this.totalResults,
    this.message,
  });

  factory QueryResponse.fromJson(Map<String, dynamic> json) {
    return QueryResponse(
      success: json['success'] ?? false,
      query: json['query'] ?? '',
      results: (json['results'] as List)
          .map((item) => FAQResult.fromJson(item))
          .toList(),
      totalResults: json['total_results'] ?? 0,
      message: json['message'],
    );
  }
}

// API Service
class ApiService {
  // Change this based on your environment:
  // - Android Emulator: http://10.0.2.2:8000
  // - iOS Simulator: http://localhost:8000
  // - Real Device: http://YOUR_PC_IP:8000 (e.g., http://192.168.1.42:8000)
  // - Production: your hosted URL
  static const String baseUrl = 'http://10.0.2.2:8000';

  /// Query the FAQ bot with a question
  static Future<QueryResponse> queryFaq(
    String question, {
    int topK = 5,
    double minScore = 0.0,
  }) async {
    final uri = Uri.parse('$baseUrl/faq');
    final response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'question': question,
        'top_k': topK,
        'min_score': minScore,
      }),
    ).timeout(const Duration(seconds: 15));

    if (response.statusCode != 200) {
      throw Exception('API Error: ${response.statusCode} - ${response.body}');
    }

    return QueryResponse.fromJson(jsonDecode(response.body));
  }

  /// Check API health status
  static Future<Map<String, dynamic>> checkHealth() async {
    final uri = Uri.parse('$baseUrl/health');
    final response = await http.get(uri).timeout(const Duration(seconds: 5));

    if (response.statusCode != 200) {
      throw Exception('Health check failed');
    }

    return jsonDecode(response.body);
  }

  /// Get API statistics
  static Future<Map<String, dynamic>> getStats() async {
    final uri = Uri.parse('$baseUrl/stats');
    final response = await http.get(uri).timeout(const Duration(seconds: 5));

    if (response.statusCode != 200) {
      throw Exception('Stats request failed');
    }

    return jsonDecode(response.body);
  }
}
