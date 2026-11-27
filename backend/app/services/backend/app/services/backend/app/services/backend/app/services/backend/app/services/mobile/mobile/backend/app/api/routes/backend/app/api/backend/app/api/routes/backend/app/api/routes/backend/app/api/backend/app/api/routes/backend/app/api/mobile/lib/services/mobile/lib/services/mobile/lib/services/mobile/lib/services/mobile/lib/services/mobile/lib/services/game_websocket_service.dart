
import 'dart:async';
import 'dart:convert';

import 'package:web_socket_channel/web_socket_channel.dart';

class GameWebSocketService {
  WebSocketChannel? _channel;

  final StreamController<Map<String, dynamic>>
      _messageController =
      StreamController<Map<String, dynamic>>.broadcast();

  Stream<Map<String, dynamic>> get messages =>
      _messageController.stream;

  bool get isConnected => _channel != null;

  Future<void> connect({
    required String baseUrl,
    required String userId,
  }) async {
    if (_channel != null) {
      return;
    }

    final uri = Uri.parse(
      '$baseUrl/ws/games/$userId',
    );

    _channel = WebSocketChannel.connect(uri);

    _channel!.stream.listen(
      (message) {
        try {
          final decoded = jsonDecode(message);

          if (decoded is Map<String, dynamic>) {
            _messageController.add(decoded);
          }
        } catch (error) {
          _messageController.add({
            'type': 'error',
            'message': 'Invalid server message',
          });
        }
      },
      onError: (error) {
        _messageController.add({
          'type': 'error',
          'message': 'WebSocket connection failed',
        });
      },
      onDone: () {
        _channel = null;
      },
    );

    await _channel!.ready;
  }

  void sendMessage(Map<String, dynamic> message) {
    if (_channel == null) {
      throw StateError('WebSocket is not connected.');
    }

    _channel!.sink.add(jsonEncode(message));
  }

  Future<void> disconnect() async {
    final channel = _channel;
    _channel = null;

    await channel?.sink.close();
  }

  Future<void> dispose() async {
    await disconnect();
    await _messageController.close();
  }
}
