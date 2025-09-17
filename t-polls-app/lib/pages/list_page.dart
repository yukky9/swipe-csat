import "package:flutter/material.dart";
import "package:t_polls_app/api/api_service.dart";
import "package:t_polls_app/types/exceptions.dart";
import "package:t_polls_app/widgets/exception_dialog.dart";
import "../types/poll.dart";
import "../widgets/poll_card.dart";

class ListPage extends StatefulWidget {
  const ListPage({super.key});

  @override
  State<ListPage> createState() => _ListPageState();
}

class _ListPageState extends State<ListPage> {
  Future? polls;

  void fetch() async {
    polls = ApiService.service.getPolls();
  }

  // @override
  // void initState() {
  //   super.initState();
  //   fetch();
  // }

  @override
  Widget build(BuildContext context) {
    fetch();
    print("AAAA");
    return FutureBuilder(
      future: polls,
      builder: (context, snapshot) {
        print(snapshot);
        if (snapshot.hasData) {
          List<Poll> pollsList = snapshot.data;
          return SingleChildScrollView(
            child: GridView.builder(
              physics: const NeverScrollableScrollPhysics(),
              shrinkWrap: true,
              itemBuilder: (context, index) => PollCardWidget(
                poll: pollsList[index],
              ),
              itemCount: pollsList.length,
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2),
            ),
          );
        }
        if (snapshot.error.runtimeType == NotAuthorizedException) {
          return Padding(
            padding: const EdgeInsets.all(10),
            child: Center(
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(20),
                  color: Theme.of(context).cardColor,
                ),
                alignment: Alignment.center,
                child: const Text(
                  "Для того, чтобы пользоваться приложением, пожалуйста, отправьте боту команду /start",
                  style: TextStyle(fontSize: 36),
                  textAlign: TextAlign.center,
                ),
              ),
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
                    IconButton(
                        onPressed: () {
                          setState(() {
                            fetch();
                          });
                        },
                        icon: Icon(Icons.refresh)),
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
    );
  }
}
