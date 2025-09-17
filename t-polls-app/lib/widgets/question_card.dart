import 'package:flutter/material.dart';
import 'package:telegram_web_app/telegram_web_app.dart';

class QuestionCardWidget extends StatefulWidget {
  const QuestionCardWidget(
      {super.key, required this.controller, required this.question, this.lock});

  final QuestionController controller;
  final String question;
  final bool? lock;

  @override
  State<QuestionCardWidget> createState() => _QuestionCardWidgetState();
}

class _QuestionCardWidgetState extends State<QuestionCardWidget> {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(5.0),
          child: Text(
            widget.question,
            style: Theme.of(context).textTheme.displayLarge,
          ),
        ),
        Center(
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: List.generate(
              5,
              (index) {
                return StarWidget(
                    checked:
                        (widget.controller.questions[widget.question] != null
                                ? widget.controller.questions[widget.question]!
                                : 0) >
                            index,
                    onPressed: widget.lock != true
                        ? () {
                            setState(() {
                              widget.controller
                                  .setMark(widget.question, index + 1);
                            });
                          }
                        : null);
              },
            ),
          ),
        )
      ],
    );
  }
}

class StarWidget extends StatelessWidget {
  const StarWidget({super.key, required this.checked, this.onPressed});

  final bool checked;
  final GestureTapCallback? onPressed;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onPressed,
      child: Icon(
        checked ? Icons.star : Icons.star_outline,
        size: 50,
        color: Theme.of(context).colorScheme.primary,
      ),
    );
  }
}

class QuestionController {
  final Map<String, int?> questions;
  bool? finalQuestion;
  bool answered = false;

  QuestionController({required this.questions});

  void setMark(String question, int mark) {
    questions[question] = mark;
    answered = _check();
  }

  bool _check() {
    bool a = true;

    for (int? i in questions.values) {
      if (i == null) {
        a = false;
        break;
      }
    }
    final bool res = a == true && finalQuestion != null;

    res ? TelegramWebApp.instance.mainButton.enable() : TelegramWebApp.instance.mainButton.disable();
    return res;
  }

  void setFinalQuestion(bool val) {
    finalQuestion = val;
    answered = _check();
  }
}
