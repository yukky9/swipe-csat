class Poll {
  final int id;
  final String name;
  final String desc;
  final int type; // 0 - product
  final Map<String, int?>? questions;
  final String? finalQuestion;

  Poll({
    required this.id,
    required this.name,
    required this.desc,
    this.type = 0,
    this.questions,
    this.finalQuestion,
  });

  factory Poll.fromJson(Map json) {
    Map<String, int?> q = {};
    for (Map a in json["criteria"] ?? []) {
      q[a["name"]] = null;
    }

    if (q.isNotEmpty) {
      return Poll(
          id: json["id"],
          name: json["name"],
          desc: json["description"],
          finalQuestion: json["question"],
          questions: q);
    }
    return Poll(id: json["id"], name: json["name"], desc: json["description"]);
  }

  Poll copyWith(Map data) {
    return Poll(
        id: id,
        name: name,
        desc: desc,
        type: type,
        questions: {
          data["criterion_name_1"]: data["criterion_rating_1"],
          data["criterion_name_2"]: data["criterion_rating_2"],
          data["criterion_name_3"]: data["criterion_rating_3"],
        },
        finalQuestion: data["question"]);
  }
}
