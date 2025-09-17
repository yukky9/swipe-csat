import 'package:flutter/material.dart';
import 'package:t_polls_app/api/api_service.dart';
import 'package:t_polls_app/main.dart';
import 'package:t_polls_app/pages/list_page.dart';
import 'package:t_polls_app/pages/profile_page.dart';
import 'package:t_polls_app/pages/swipe_page.dart';
import 'package:telegram_web_app/telegram_web_app.dart';

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> with TickerProviderStateMixin {
  void refresh() {
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            IconButton(
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) => ProfilePage(
                      refreshParent: refresh,
                    ),
                  ),
                );
              },
              icon: const Icon(
                Icons.account_circle,
                size: 35,
              ),
            ),
            // Text("User"),
            InkWell(
              onTap: null,
              child: Text(
                  TelegramWebApp.instance.initData.user.firstname ?? "User"),
            ),
          ],
        ),
      ),
      body: const ListPage(),
    );
  }
}
