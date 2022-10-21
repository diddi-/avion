import { InvalidTokenException } from "./exceptions/invalid-token";

export class JwtTokenPayload {
  sub: string | undefined;
  iss: string | undefined;
  exp: number;

  constructor(exp: number) {
    this.exp = exp;
  }

  static fromDict(data: any): JwtTokenPayload {
    if("exp" in data === false)
      throw new InvalidTokenException();

    const payload = new JwtTokenPayload(parseInt(data["exp"]));

    if("sub" in data)
      payload.sub = data["sub"];

    return payload;
  }
}
