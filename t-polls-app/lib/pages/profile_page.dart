import 'package:flutter/material.dart';
import 'package:t_polls_app/pages/history_page.dart';
import 'package:t_polls_app/pages/settings_page.dart';
import 'package:t_polls_app/widgets/custom_card.dart';
import 'package:t_polls_app/widgets/profile_button.dart';
import 'package:telegram_web_app/telegram_web_app.dart';

import '../api/api_service.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key, required this.refreshParent});

  final Function refreshParent;

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  Future? count;

  void fetch() {
    count = ApiService.service.getCompletedCount();
  }

  @override
  Widget build(BuildContext context) {
    fetch();
    return Scaffold(
      appBar: AppBar(
        title: const Text("Профиль"),
      ),
      body: Column(
        children: [
          Row(
            children: [
              Expanded(
                child: CustomCard(
                  title: ClipOval(
                    child: CircleAvatar(
                      radius: 60,
                      backgroundColor: Theme.of(context).canvasColor,
                      child: const Icon(
                        Icons.account_circle_outlined,
                        size: 120,
                      ),
                    ),
                  ),
                  content: Text(
                    TelegramWebApp.instance.initData.user.firstname ?? "User",
                    textScaler: const TextScaler.linear(2),
                  ),
                ),
              ),
              Expanded(
                child: CustomCard(
                  title: const Text(
                    "Опросов пройдено:",
                    style: TextStyle(
                      fontSize: 24,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  content: Padding(
                    padding: EdgeInsets.only(top: 10),
                    child: FutureBuilder(
                        future: count,
                        builder: (context, snapshot) {
                          return Text(
                            snapshot.hasData ? snapshot.data.toString() : "-",
                            style: const TextStyle(
                              fontSize: 24,
                            ),
                          );
                        }),
                  ),
                  height: 160,
                ),
              )
            ],
          ),
          Expanded(
            child: ProfileButtonWidget(
              title: const Text(
                "История",
                style: TextStyle(
                  fontSize: 24,
                ),
              ),
              icon: Icons.history,
              onTap: () {
                Navigator.of(context).push(MaterialPageRoute(
                    builder: (context) => const HistoryPage()));
              },
            ),
          ),
          Expanded(
            child: ProfileButtonWidget(
              title: const Text(
                "Настройки",
                style: TextStyle(
                  fontSize: 24,
                ),
              ),
              icon: Icons.settings,
              onTap: () {
                Navigator.of(context).push(MaterialPageRoute(
                    builder: (context) => SettingsPage(
                          refreshParent: widget.refreshParent,
                        )));
              },
            ),
          ),
          Expanded(
            child: ProfileButtonWidget(
              title: const Text(
                "Тех. поддержка",
                style: TextStyle(
                  fontSize: 24,
                ),
              ),
              icon: Icons.support,
              onTap: () {},
            ),
          )
        ],
      ),
    );
  }
}
