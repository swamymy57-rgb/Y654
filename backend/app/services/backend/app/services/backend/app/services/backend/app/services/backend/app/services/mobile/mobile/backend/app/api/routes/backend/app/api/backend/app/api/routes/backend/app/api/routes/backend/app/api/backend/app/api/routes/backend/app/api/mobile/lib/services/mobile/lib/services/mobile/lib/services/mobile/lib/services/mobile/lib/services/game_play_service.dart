
import 'api_service.dart';

class GamePlayService {
  // Play the virtual dice game.
  static Future<Map<String, dynamic>> playDice({
    required int betPoints,
  }) async {
    if (betPoints <= 0 || betPoints > 1000) {
      throw ArgumentError(
        'Bet points must be between 1 and 1000.',
      );
    }

    return await ApiService.post(
      '/game-play/dice',
      body: {
        'bet_points': betPoints,
      },
    );
  }

  // Get available games from the game engine.
  static Future<Map<String, dynamic>> getAvailableGames() async {
    return await ApiService.get(
      '/game-play/available-games',
    );
  }
}
