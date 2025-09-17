import 'package:flutter/material.dart';
import 'package:t_polls_app/types/poll.dart';
import 'package:t_polls_app/widgets/history_card.dart';

import '../api/api_service.dart';

class HistoryPage extends StatefulWidget {
  const HistoryPage({super.key});

  @override
  State<HistoryPage> createState() => _HistoryPageState();
}

class _HistoryPageState extends State<HistoryPage> {
  Future? polls;

  void fetch() async {
    polls = ApiService.service.getHistories();
  }

  @override
  Widget build(BuildContext context) {
    fetch();
    return Scaffold(
      appBar: AppBar(
        title: const Text("История"),
      ),
      body: FutureBuilder(
        future: polls,
        builder: (context, snapshot) {
          print(snapshot);
          if (snapshot.hasData) {
            List<Poll> pollsList = snapshot.data;
            return SingleChildScrollView(
              child: GridView.builder(
                physics: const NeverScrollableScrollPhysics(),
                shrinkWrap: true,
                itemBuilder: (context, index) => HistoryCard(
                  poll: pollsList[index]
                ),
                itemCount: pollsList.length,
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2),
              ),
            );
          }
          if (snapshot.hasError) {
            return Padding(
              padding: const EdgeInsets.all(10),
              child: Center(
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(20),
                    color: Theme.of(context).cardColor,
                  ),
                  alignment: Alignment.center,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        "Произошла ошибка: ${snapshot.error}",
                        style: const TextStyle(fontSize: 28),
                        textAlign: TextAlign.center,
                      ),
                      IconButton(onPressed: () {
                        setState(() {
                          fetch();
                        });
                      }, icon: Icon(Icons.refresh)),
                    ],
                  ),
                ),
              ),
            );
          }
          return const Center(
            child: CircularProgressIndicator(),
          );
        },
      ),
    );
  }
}
