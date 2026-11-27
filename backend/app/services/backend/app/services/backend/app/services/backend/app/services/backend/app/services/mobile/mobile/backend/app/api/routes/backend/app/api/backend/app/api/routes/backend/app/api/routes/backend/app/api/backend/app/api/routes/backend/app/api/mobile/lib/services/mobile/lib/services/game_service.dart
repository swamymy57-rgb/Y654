
import 'api_service.dart';

class GameService {
  // Get complete game lobby information.
  static Future<Map<String, dynamic>> getLobby() async {
    return await ApiService.get('/games/lobby');
  }

  // Get all game categories.
  static Future<Map<String, dynamic>> getCategories() async {
    return await ApiService.get('/games/categories');
  }

  // Get games by category.
  static Future<Map<String, dynamic>> getGames({
    String category = 'ALL',
    String? search,
  }) async {
    final query = <String, String>{
      'category': category,
    };

    if (search != null && search.trim().isNotEmpty) {
      query['search'] = search.trim();
    }

    final queryString = Uri(queryParameters: query).query;

    return await ApiService.get(
      '/games/?$queryString',
    );
  }

  // Get details of one game.
  static Future<Map<String, dynamic>> getGame(
    String gameId,
  ) async {
    return await ApiService.get('/games/$gameId');
  }
}
