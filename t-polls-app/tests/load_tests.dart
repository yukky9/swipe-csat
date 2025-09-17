import "package:t_polls_app/api/api_service.dart";


bool loadTest() {
  try {
    Future<bool> poll = ApiService.service.loadResult(127272, {"aaaa": 3, "vvv": 2, "sss": 5}, true);
    poll.then((value) {
      return value;
    });
  }
  catch (e){
    return false;
  }
  return false;
}
