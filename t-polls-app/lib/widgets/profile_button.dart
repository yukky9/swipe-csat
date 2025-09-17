import 'package:flutter/material.dart';

class ProfileButtonWidget extends StatelessWidget {
  const ProfileButtonWidget({
    super.key,
    required this.title,
    this.subtitle,
    this.icon,
    this.height,
    this.onTap,
  });

  final Widget? title, subtitle;
  final IconData? icon;
  final double? height;
  final void Function()? onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: SizedBox(
        height: height,
        child: Card(
          shadowColor: Colors.transparent,
          child: Center(
            child: ListTile(
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(15.0),
              ),
              title: title,
              subtitle: subtitle,
              trailing: icon != null
                  ? CircleAvatar(
                      radius: 15,
                      backgroundColor: Theme.of(context).colorScheme.secondary,
                      child: Icon(
                        size: 20,
                        icon,
                        color: Theme.of(context).primaryColor,
                      ),
                    )
                  : null,
            ),
          ),
        ),
      ),
    );
  }
}
