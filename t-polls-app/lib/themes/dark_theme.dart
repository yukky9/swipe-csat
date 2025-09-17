import 'dart:ui';

import 'package:t_polls_app/themes/base_theme.dart';

class DarkTheme extends BaseTheme {
  @override
  Color get backgroundColor => const Color.fromARGB(255, 44, 56, 68);

  @override
  Color get primaryAccent => const Color.fromRGBO(255, 221, 45, 1);

  @override
  Color get secondaryColor => const Color.fromARGB(255, 71, 167, 247);

  @override
  Color get cardColor => const Color.fromARGB(255, 50, 62, 68);

  @override
  Color get primaryContent => const Color.fromRGBO(238, 238, 238, 1);

  @override
  Brightness get brightness => Brightness.dark;
}
