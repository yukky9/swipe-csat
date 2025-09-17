import 'dart:ui';

import 'package:t_polls_app/themes/base_theme.dart';

class LightTheme extends BaseTheme {
  @override
  Color get backgroundColor => const Color.fromRGBO(255, 255, 255, 1);

  @override
  Color get primaryAccent => const Color.fromRGBO(255, 221, 45, 1);

  @override
  Color get secondaryColor => const Color.fromARGB(255, 71, 167, 247);

  @override
  Color get cardColor => const Color.fromARGB(255, 236, 236, 236);

  @override
  Color get primaryContent => const Color.fromRGBO(0, 0, 0, 1);

  @override
  Brightness get brightness => Brightness.light;
}
