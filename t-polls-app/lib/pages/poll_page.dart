import 'package:flutter/material.dart';
import 'package:t_polls_app/api/api_service.dart';
import 'package:t_polls_app/pages/main_page.dart';
import 'package:t_polls_app/types/exceptions.dart';
import 'package:t_polls_app/types/poll.dart';
import 'package:t_polls_app/widgets/exception_dialog.dart';
import 'package:t_polls_app/widgets/question_card.dart';
import 'package:telegram_web_app/telegram_web_app.dart';

import '../widgets/custom_appbar.dart';

class PollPage extends StatefulWidget {
  const PollPage(
      {super.key, required this.poll, required this.lock, this.finalQuestion});

  final Poll poll;

  final bool lock;
  final bool? finalQuestion;

  @override
  State<PollPage> createState() => _PollPageState();
}

class _PollPageState extends State<PollPage> {
  late final QuestionController _questionController;

  void onButtonPress() {
    if (!_questionController.answered) return;
    Future<bool> res = ApiService.service.loadResult(
        widget.poll.id,
        _questionController.questions,
        _questionController.finalQuestion ?? false);
    TelegramWebApp.instance.mainButton.hide();

    res.then(
      (bool val) {
        return val
            ? showDialog(
                barrierDismissible: false,
                context: context,
                builder: (context) => AlertDialog(
                      title: const Text("Спасибо за прохождение опроса!"),
                      actions: [
                        TextButton(
                            onPressed: () => Navigator.of(context)
                                .pushAndRemoveUntil(
                                    MaterialPageRoute(
                                        builder: (context) => const MainPage()),
                                    (r) => false),
                            child: const Text("ОК"))
                      ],
                    ))
            : showDialog(
                barrierDismissible: false,
                context: context,
                builder: (context) => AlertDialog(
                  title: const Text("Что-то пошло не так..."),
                  content: const Text("Попробуйте снова через несколько минут"),
                  actions: [
                    TextButton(
                        onPressed: () => Navigator.of(context)
                            .pushAndRemoveUntil(
                                MaterialPageRoute(
                                    builder: (context) => const MainPage()),
                                (r) => false),
                        child: const Text("ОК"))
                  ],
                ),
              );
      },
    ).onError(
      (APIError e, _) {
        showDialog(
            context: context,
            builder: (context) => ExceptionDialog(
                  e: e,
                  doublePop: true,
                ));
      },
    );
  }

  @override
  void initState() {
    super.initState();
    _questionController = QuestionController(questions: widget.poll.questions!);
    widget.finalQuestion == null
        ? null
        : _questionController.setFinalQuestion(widget.finalQuestion!);
    if (widget.lock == true) return;
    TelegramWebApp.instance.mainButton
      ..onClick(onButtonPress)
      ..setParams(BottomButtonParams(
        text: "Ответить",
        color: const Color.fromARGB(255, 71, 167, 247).hexString,
        textColor: '',
        hasShineEffect: true,
        position: '',
      ))
      ..disable()
      ..show();
  }

  @override
  void dispose() {
    if (widget.lock == true) return;
    TelegramWebApp.instance.mainButton.hide();
    TelegramWebApp.instance.mainButton.offClick(onButtonPress);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_questionController.answered) {
      TelegramWebApp.instance.mainButton.enable();
    }
    return Scaffold(
      appBar: MyAppBar(text: widget.poll.name),
      body: Center(
        child: Column(
          children: [
            ListView.builder(
                physics: const NeverScrollableScrollPhysics(),
                shrinkWrap: true,
                itemBuilder: (context, index) => Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: QuestionCardWidget(
                          controller: _questionController,
                          question:
                              widget.poll.questions!.keys.elementAt(index),
                          lock: widget.lock,
                        ),
                      ),
                    ),
                itemCount: widget.poll.questions!.length),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Text(
                        widget.poll.finalQuestion!,
                        textAlign: TextAlign.center,
                        style: Theme.of(context).textTheme.displayLarge,
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 15.0),
                      child: Row(
                        mainAxisSize: MainAxisSize.max,
                        children: [
                          const Spacer(
                            flex: 2,
                          ),
                          OutlinedButton(
                              style: OutlinedButton.styleFrom(
                                  // backgroundColor: Colors.green,
                                  side: BorderSide(
                                      width:
                                          _questionController.finalQuestion ==
                                                  true
                                              ? 5
                                              : 2,
                                      color: Colors.green)),
                              onPressed: widget.lock
                                  ? null
                                  : () {
                                      setState(() {
                                        _questionController
                                            .setFinalQuestion(true);
                                      });
                                    },
                              child: Text(
                                "Да",
                                style: TextStyle(
                                    color: Theme.of(context).primaryColor),
                              )),
                          const Spacer(
                            flex: 1,
                          ),
                          OutlinedButton(
                              style: OutlinedButton.styleFrom(
                                  // backgroundColor: Colors.red,
                                  side: BorderSide(
                                      width:
                                          _questionController.finalQuestion ==
                                                  false
                                              ? 5
                                              : 2,
                                      color: Colors.red)),
                              onPressed: widget.lock
                                  ? null
                                  : () {
                                      setState(() {
                                        _questionController
                                            .setFinalQuestion(false);
                                      });
                                    },
                              child: Text(
                                "Нет",
                                style: TextStyle(
                                    color: Theme.of(context).primaryColor),
                              )),
                          const Spacer(
                            flex: 2,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
