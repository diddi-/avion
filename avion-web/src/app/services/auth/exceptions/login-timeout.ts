export class LoginTimeoutException extends Error {
  constructor() {
    super("Login failed due to timeout");
  }
}
