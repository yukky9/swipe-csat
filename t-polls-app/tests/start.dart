import 'history_tests.dart';
import 'load_tests.dart';
import 'polls_tests.dart';

void main() {
  List<bool> res = [
    pollsTest(),
    historiesTest(),
    loadTest(),
  ];

  for (bool a in res) {
    print(a);
  }
}
