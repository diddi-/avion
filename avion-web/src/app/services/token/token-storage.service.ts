import { Injectable } from '@angular/core';
import { TokenNotFoundException } from './exceptions/token-not-found-exception';

@Injectable({
  providedIn: 'root'
})
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
}
