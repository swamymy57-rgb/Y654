
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Replace this with your deployed backend URL.
  static const String baseUrl = 'http://10.0.2.2:8000/api/v1';

  static Future<Map<String, dynamic>> get(
    String endpoint,
  ) async {
    final response = await http
        .get(Uri.parse('$baseUrl$endpoint'))
        .timeout(const Duration(seconds: 15));

    return _handleResponse(response);
  }

  static Future<Map<String, dynamic>> post(
    String endpoint, {
    Map<String, dynamic>? body,
  }) async {
    final response = await http
        .post(
          Uri.parse('$baseUrl$endpoint'),
          headers: {
            'Content-Type': 'application/json',
          },
          body: jsonEncode(body ?? {}),
        )
        .timeout(const Duration(seconds: 15));

    return _handleResponse(response);
  }

  static Map<String, dynamic> _handleResponse(
    http.Response response,
  ) {
    final dynamic decoded = jsonDecode(response.body);

    if (response.statusCode >= 200 &&
        response.statusCode < 300) {
      if (decoded is Map<String, dynamic>) {
        return decoded;
      }

      return {'data': decoded};
    }

    throw Exception(
      'API Error ${response.statusCode}: ${response.body}',
    );
  }
}
