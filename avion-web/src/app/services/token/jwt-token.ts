import { JwtTokenPayload } from "./jwt-token-payload";

export class JwtToken {

  public payload: JwtTokenPayload;
  public encodedString: string;

  constructor(encodedString: string, payload: JwtTokenPayload) {
    this.encodedString = encodedString;
    this.payload = payload;
  }

  public isExpired(): boolean {
    return this.payload.exp < new Date().getTime();
  }

  public getUsername(): string | undefined {
    return this.payload.sub;
  }

  static fromString(tokenString: string): JwtToken {
    const parts = tokenString.split(".");
    const payload = JwtTokenPayload.fromDict(JSON.parse(atob(parts[1])));
    return new JwtToken(tokenString, payload);
  }
}
