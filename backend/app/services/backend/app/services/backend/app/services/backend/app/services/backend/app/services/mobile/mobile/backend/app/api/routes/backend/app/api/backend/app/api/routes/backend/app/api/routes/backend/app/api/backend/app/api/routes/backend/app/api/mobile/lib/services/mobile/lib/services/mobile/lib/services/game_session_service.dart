
import 'api_service.dart';

class GameSessionService {
  // Create a new game session.
  static Future<Map<String, dynamic>> createSession({
    required String userId,
    required String gameId,
  }) async {
    final query = Uri(
      queryParameters: {
        'user_id': userId,
        'game_id': gameId,
      },
    ).query;

    return await ApiService.post(
      '/game-sessions/?$query',
    );
  }

  // Get session details.
  static Future<Map<String, dynamic>> getSession(
    String sessionId,
  ) async {
    return await ApiService.get(
      '/game-sessions/$sessionId',
    );
  }

  // Complete a session.
  static Future<Map<String, dynamic>> completeSession(
    String sessionId,
  ) async {
    return await ApiService.post(
      '/game-sessions/$sessionId/complete',
    );
  }

  // Cancel a session.
  static Future<Map<String, dynamic>> cancelSession(
    String sessionId,
  ) async {
    return await ApiService.post(
      '/game-sessions/$sessionId/cancel',
    );
  }

  // Get all sessions of a user.
  static Future<Map<String, dynamic>> getUserSessions(
    String userId,
  ) async {
    return await ApiService.get(
      '/game-sessions/user/$userId',
    );
  }
}
