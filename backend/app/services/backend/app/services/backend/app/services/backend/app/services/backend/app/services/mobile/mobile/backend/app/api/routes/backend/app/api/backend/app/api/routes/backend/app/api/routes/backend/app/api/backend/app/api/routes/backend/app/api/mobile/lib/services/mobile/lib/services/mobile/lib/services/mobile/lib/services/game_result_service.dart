
import 'api_service.dart';

class GameResultService {
  // Submit a game result.
  static Future<Map<String, dynamic>> submitResult({
    required String userId,
    required String gameId,
    required String sessionId,
    int score = 0,
    int pointsEarned = 0,
  }) async {
    final query = Uri(
      queryParameters: {
        'user_id': userId,
        'game_id': gameId,
        'session_id': sessionId,
        'score': score.toString(),
        'points_earned': pointsEarned.toString(),
      },
    ).query;

    return await ApiService.post(
      '/game-results/?$query',
    );
  }

  // Get one game result.
  static Future<Map<String, dynamic>> getResult(
    String resultId,
  ) async {
    return await ApiService.get(
      '/game-results/$resultId',
    );
  }

  // Get all results of a user.
  static Future<Map<String, dynamic>> getUserResults(
    String userId,
  ) async {
    return await ApiService.get(
      '/game-results/user/$userId',
    );
  }
}
