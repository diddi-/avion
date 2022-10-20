export class PasswordMismatchException extends Error {
  constructor() {
    super("Could not register account. Passwords don't match.");
  }
}
