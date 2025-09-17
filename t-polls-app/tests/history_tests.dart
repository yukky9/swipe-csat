import "package:t_polls_app/api/api_service.dart";
import "package:t_polls_app/types/exceptions.dart";
import "package:t_polls_app/types/poll.dart";

bool historiesTest() {
  try {
    Future<List?> polls = ApiService.service.getHistories();
    polls.then((value) {
      if (value.runtimeType == List) {
        for (var p in value!) {
          if (!(p.runtimeType == Poll)) {
            return false;
          }
        }
        return true;
      }
    });
  }
  on APIError catch (_){
    return false;
  }
  catch (e){
    return false;
  }
  return false;
}