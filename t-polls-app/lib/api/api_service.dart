import "package:http/http.dart" as http;
import "package:t_polls_app/types/exceptions.dart";
import "dart:convert";
import "package:t_polls_app/types/poll.dart";
import "package:telegram_web_app/telegram_web_app.dart";

class ApiService {
  String serverURL = "https://api.penki.tech/";
  static final ApiService service = ApiService();

  Future<Map<String, bool>> getSettings() async {
    http.Response baseInfoResponse = await http.get(Uri.parse(
        "$serverURL/api/user/settings?user_id=${TelegramWebApp.instance.initData.user.id}"));
    Map<String, bool> baseInfoJson = jsonDecode(baseInfoResponse.body);
    return baseInfoJson;
  }

  Future<List<Poll>> getPolls() async {
    print("AAAA");
    http.Response baseInfoResponse = await http.get(Uri.parse(
        "$serverURL/api/user/polls?user_id=${TelegramWebApp.instance.initData.user.id}"));
    List baseInfoJson = jsonDecode(baseInfoResponse.body);
    return List.generate(
        baseInfoJson.length, (index) => Poll.fromJson(baseInfoJson[index]));
    return a;
  }

  Future<Poll?> getPoll(int id) async {
    http.Response baseInfoResponse = await http
        .get(Uri.parse("$serverURL/api/user/poll?id=$id"))
        .timeout(const Duration(seconds: 3), onTimeout: () {
      throw APIError("Превышено время ожидания ответа сервера");
    });
    print(baseInfoResponse.request!.url);
    Map baseInfoJson = jsonDecode(baseInfoResponse.body);
    if (baseInfoResponse.statusCode != 200) {
      throw APIError(baseInfoJson["message"]);
    }
    print(baseInfoJson);
    var a = Poll.fromJson(baseInfoJson);
    print(a);
    return a;
  }

  Future<Map?> getHistory(int id) async {
    http.Response baseInfoResponse = await http
        .get(Uri.parse(
            "$serverURL/api/user/history?poll_id=$id&user_id=${TelegramWebApp.instance.initData.user.id}"))
        .timeout(const Duration(seconds: 3), onTimeout: () {
      throw APIError("Превышено время ожидания ответа сервера");
    });
    print(baseInfoResponse.request!.url);
    Map baseInfoJson = jsonDecode(baseInfoResponse.body);
    if (baseInfoResponse.statusCode != 200) {
      throw APIError(baseInfoJson["message"]);
    }
    print(baseInfoJson);
    return baseInfoJson;
  }

  Future<Poll?> getRandomPoll(int previousId) async {
    http.Response baseInfoResponse = await http
        .get(Uri.parse(
            "$serverURL/api/user/swipe?poll_id=$previousId&user_id=${TelegramWebApp.instance.initData.user.id}"))
        .timeout(const Duration(seconds: 3), onTimeout: () {
      throw APIError("Превышено время ожидания ответа сервера");
    });
    print(baseInfoResponse.request!.url);
    Map baseInfoJson = jsonDecode(baseInfoResponse.body);
    if (baseInfoResponse.statusCode != 200) {
      throw APIError(baseInfoJson["message"]);
    }
    print(baseInfoJson);
    var a = Poll.fromJson(baseInfoJson);
    print(a);
    return a;
  }

  Future<bool> loadResult(
      int pollId, Map<String, int?> questions, bool finalQuestion) async {
    List<String> keys = questions.keys.toList();
    Map body = {
      "user_id": TelegramWebApp.instance.initData.user.id.toString(),
      "poll_id": poll_id,
    };

    http.Response baseInfoResponse = await http.post(
      Uri.parse("$serverURL/api/user/poll"),
      body: body,
    );
    return baseInfoResponse.statusCode == 200;
  }
}
