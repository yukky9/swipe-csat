class APIError implements Exception {
  APIError(this.e);
  String e;
}


class NotAuthorizedException extends APIError {
  NotAuthorizedException(e) : super(e);
}
