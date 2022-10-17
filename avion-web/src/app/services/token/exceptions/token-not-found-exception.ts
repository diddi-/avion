
export class TokenNotFoundException extends Error {
  constructor() {
    super("Token not found");
  }
}
