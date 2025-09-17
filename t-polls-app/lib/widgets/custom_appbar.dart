import 'package:flutter/material.dart';
import 'package:running_text/running_text.dart';

class MyAppBar extends StatelessWidget implements PreferredSizeWidget {
  const MyAppBar({super.key, required this.text});

  final String text;

  @override
  Widget build(BuildContext context) {
    return AppBar(
      title: text.length > 20
          ? RunningTextView(
              data: RunningTextModel(
                [text],
                softWrap: false,
                velocity: 50,
                direction: RunningTextDirection.rightToLeft,
                fadeSide: RunningTextFadeSide.both,
                textStyle: const TextStyle(
                    fontSize: 18, overflow: TextOverflow.visible),
              ),
            )
          : Text(text),
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}
