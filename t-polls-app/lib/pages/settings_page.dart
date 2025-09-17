import 'package:flutter/material.dart';
import 'package:t_polls_app/api/api_service.dart';
import 'package:t_polls_app/main.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key, required this.refreshParent});

  final Function refreshParent;

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Настройки"),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Card(
              child: Padding(
                padding:
                    const EdgeInsets.symmetric(vertical: 15, horizontal: 10),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      "Светлая тема",
                      style: TextStyle(
                        fontSize: 24,
                      ),
                    ),
                    Switch(
                        value: MainApp.notifier.value == ThemeMode.dark,
                        onChanged: (val) {
                          MainApp.notifier.value =
                              val ? ThemeMode.dark : ThemeMode.light;
                          setState(() {});
                        }),
                  ],
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Card(
              child: Padding(
                padding:
                    const EdgeInsets.symmetric(vertical: 15, horizontal: 10),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      "Свайп-режим",
                      style: TextStyle(
                        fontSize: 24,
                      ),
                    ),
                    Switch(
                        value: MainApp.swipeMode.value,
                        onChanged: (val) {
                          MainApp.swipeMode.value = val;
                          setState(() {});
                          widget.refreshParent();
                        }),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    ApiService.service.setSettings(MainApp.notifier.value == ThemeMode.light, MainApp.swipeMode.value);
    super.dispose();
  }
}
