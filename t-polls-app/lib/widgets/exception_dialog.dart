import 'package:flutter/material.dart';
import 'package:t_polls_app/types/exceptions.dart';

class ExceptionDialog extends StatelessWidget {
  const ExceptionDialog({super.key, required this.e, this.doublePop = false});

  final APIError e;
  final bool doublePop;

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text("Упс!"),
      content: Text(e.e),

      actions: [
        TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              if (doublePop) {
                Navigator.of(context).pop();
              }
            },
            child: const Text("OK"))
      ],
    );
  }
}
