import "package:flutter/material.dart";
import 'package:appinio_swiper/appinio_swiper.dart';
import "package:t_polls_app/api/api_service.dart";
import "package:t_polls_app/types/exceptions.dart";
import "package:t_polls_app/widgets/custom_appbar.dart";
import "package:t_polls_app/widgets/exception_dialog.dart";
import "../types/poll.dart";
import "main_page.dart";

class SwipePage extends StatefulWidget {
  const SwipePage({super.key, required this.poll});

  final Poll poll;

  @override
  State<SwipePage> createState() => _SwipePageState();
}

class _SwipePageState extends State<SwipePage> {
  List<int> marks = [];

  // @override
  // void initState() {
  //   refresh();
  //   super.initState();
  // }

  @override
  Widget build(BuildContext context) {
    List<String> keys = [];
    for (var a in widget.poll.questions!.keys) {
      keys.add(a);
    }

    return Scaffold(
      appBar: MyAppBar(text: widget.poll.name),
      body: Padding(
        padding: const EdgeInsets.all(10),
        child: Center(
          child: Column(
            children: [
              Expanded(
                child: buildSwiper(widget.poll, keys),
              ),
              const Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Icon(
                    Icons.close,
                    color: Colors.red,
                    size: 40,
                  ),
                  Icon(
                    Icons.arrow_back,
                    size: 30,
                  ),
                  Text(
                    "Свайпай!",
                    style: TextStyle(
                      fontSize: 22,
                    ),
                  ),
                  Icon(
                    Icons.arrow_forward,
                    size: 30,
                  ),
                  Icon(
                    Icons.done,
                    color: Colors.green,
                    size: 40,
                  ),
                ],
              ),
              const SizedBox(
                height: 8,
              )
            ],
          ),
        ),
      ),
    );
  }

  AppinioSwiper buildSwiper(Poll p, List<String> keys, [args]) {
    return AppinioSwiper(
        cardCount: keys.length + 1,
        backgroundCardCount: 0,
        backgroundCardScale: 0.1,
        maxAngle: 0,
        threshold: 20,
        swipeOptions: const SwipeOptions.symmetric(horizontal: true),
        onSwipeEnd:
            (int previousIndex, int targetIndex, SwiperActivity activity) {
          // print(targetIndex);
          if (previousIndex == targetIndex) return;
          if (activity.direction == AxisDirection.left) {
            marks.add(1);
          }
          if (activity.direction == AxisDirection.right) {
            marks.add(5);
          }
          if (targetIndex == keys.length + 1) {
            ApiService.service
                .loadResult(
                    widget.poll.id,
                    Map.fromIterables(
                        keys, List.generate(3, (index) => marks[index])),
                    marks.last == 5)
                .then((bool value) {
              showDialog(
                barrierDismissible: false,
                context: context,
                builder: (context) => AlertDialog(
                  title: Text(value
                      ? "Спасибо за прохождение опроса!"
                      : "Не удалось загрузить ответ на сервер. Пожалуйста, попробуйте позже"),
                  actions: [
                    TextButton(
                        onPressed: () {
                          Navigator.of(context).pushAndRemoveUntil(
                              MaterialPageRoute(
                                  builder: (context) => const MainPage()),
                              (r) => false);
                          // initState();
                        },
                        child: const Text("ОК"))
                  ],
                ),
              );
            }).onError((APIError e, _) {
              showDialog(
                  context: context,
                  builder: (context) => ExceptionDialog(
                        e: e,
                        doublePop: true,
                      ));
            });
          }
        },
        cardBuilder: (BuildContext context, int index) {
          // print("-----: $index");
          return SwipeQuestionCard(
            index: index,
            poll: p,
            keys: keys,
          );
        });
  }
}

class SwipeQuestionCard extends StatefulWidget {
  const SwipeQuestionCard(
      {super.key, required this.index, required this.poll, required this.keys});

  final int index;
  final Poll poll;
  final List<String> keys;

  @override
  State<SwipeQuestionCard> createState() => _SwipeQuestionCardState();
}

class _SwipeQuestionCardState extends State<SwipeQuestionCard> {
  @override
  Widget build(BuildContext context) {
    var i = widget.index;
    // print("++++: $i");
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(20),
        color: Theme.of(context).cardColor,
      ),
      alignment: Alignment.center,
      child: Text(
        widget.index == 3 ? widget.poll.finalQuestion! : widget.keys[i],
        style: const TextStyle(fontSize: 40),
        textAlign: TextAlign.center,
      ),
    );
  }
}
