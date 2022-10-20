export class RegistrationTimeoutException extends Error {
  constructor() {
    super("Registration failed due to timeout");
  }
}
