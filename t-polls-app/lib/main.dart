import 'package:flutter/material.dart';
import 'package:t_polls_app/api/api_service.dart';
import 'package:t_polls_app/pages/main_page.dart';
import 'package:t_polls_app/themes/dark_theme.dart';
import 'package:t_polls_app/themes/light_theme.dart';
import 'package:telegram_web_app/telegram_web_app.dart';
// import 'package:t_polls_app/pages/main_page.dart';

void main() {
  try {
    if (TelegramWebApp.instance.isSupported) {
      TelegramWebApp.instance.ready();
      Future.delayed(
          const Duration(seconds: 1), TelegramWebApp.instance.expand);
    }
  } catch (e) {
    print("Error happened in Flutter while loading Telegram $e");
    return;
  }

  FlutterError.onError = (details) {
    print("Flutter error happened: $details");
  };
  MainApp.fetchSettings();
  runApp(const MainApp());
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  static void fetchSettings() {
    ApiService.service.getSettings().then((value) {
      if (value == null) return;
      bool? theme = value["light_theme"];
      if (theme != null) {
        MainApp.notifier.value = theme ? ThemeMode.light : ThemeMode.dark;
      }
      MainApp.swipeMode.value = value["swipe_mode"] ?? MainApp.swipeMode.value;
    });
  }

  static final ValueNotifier<ThemeMode> notifier =
      ValueNotifier(ThemeMode.dark);

  static final ValueNotifier<bool> swipeMode = ValueNotifier(false);

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<ThemeMode>(
        valueListenable: notifier,
        builder: (_, mode, __) {
          return MaterialApp(
            theme: DarkTheme().themeData,
            darkTheme: LightTheme().themeData,
            themeMode: mode,
            home: const MainPage(),
          );
        });
  }
}
