import 'package:flutter/material.dart';
import 'package:t_polls_app/api/api_service.dart';
import 'package:t_polls_app/pages/poll_page.dart';
import 'package:t_polls_app/types/exceptions.dart';
import 'package:t_polls_app/types/poll.dart';
import 'package:t_polls_app/widgets/exception_dialog.dart';

class HistoryCard extends StatelessWidget {
  const HistoryCard({super.key, required this.poll});

  final Poll poll;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () {
        ApiService.service.getHistory(poll.id).then((value) {
          if (value == null) return;
          Poll newPoll = poll.copyWith(value);
          Navigator.of(context).push(
            MaterialPageRoute(
              builder: (context) => PollPage(
                poll: newPoll,
                lock: true,
                finalQuestion: value["answer"],
              ),
            ),
          );
        }).onError((APIError e, _) {
          showDialog(
              context: context, builder: (context) => ExceptionDialog(e: e));
        });
      },
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            children: [
              Row(
                children: [
                  const Spacer(),
                  InkWell(
                    onTap: () {
                      showDialog(
                          context: context,
                          builder: (context) {
                            return AlertDialog(
                              title: const Text("Описание"),
                              content: Text(poll.desc),
                              actions: [
                                TextButton(
                                    onPressed: () {
                                      Navigator.of(context).pop();
                                    },
                                    child: Text("Закрыть"))
                              ],
                            );
                          });
                    },
                    child: CircleAvatar(
                      radius: 10,
                      backgroundColor: Theme.of(context).colorScheme.secondary,
                      child: Icon(
                        size: 15,
                        Icons.info,
                        color: Theme.of(context).primaryColor,
                      ),
                    ),
                  )
                ],
              ),
              const Spacer(),
              Center(
                child: Text(
                  poll.name,
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.titleMedium,
                  overflow: TextOverflow.ellipsis,
                  maxLines: 4,
                ),
              ),
              const Spacer(
                flex: 2,
              )
            ],
          ),
        ),
      ),
    );
  }
}
