import { Injectable } from '@angular/core';
import { TokenNotFoundException } from './exceptions/token-not-found-exception';

@Injectable({
  providedIn: 'root'
})
// NOTE: There are some serious considerations to be made here. Storing tokens in localStorage may or may not be
// a safe thing due to XSS.
export class TokenStorageService {

  constructor() { }

  public saveAccessToken(token: string): void {
    localStorage.setItem("accessToken", token);
  }

  public getAccessToken(): string {
    const token = localStorage.getItem("accessToken");
    if(token)
      return token;

    throw new TokenNotFoundException();
  }

  public clearAllTokens(): void {
    localStorage.removeItem("accessToken");
  }
}
