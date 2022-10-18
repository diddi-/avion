import { Injectable } from '@angular/core';
import {Router} from "@angular/router";
import {LoginCredentials} from "./login-credentials";
import {LoginResponse} from "./login-response";
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError, TimeoutError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { LoginTimeoutException } from './exceptions/login-timeout';
import { InvalidCredentialsException } from './exceptions/invalid-credentials-exception';
import { authLoginOptions } from './auth-login-options';
import { TokenStorageService } from '../token/token-storage.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  public isLoggedIn: boolean = false;
  public username: string | undefined = 'admin';
  public token: string | null = null;
  redirectUrl: string | null = null;

  constructor(private router: Router, private http: HttpClient,
              private tokenStorage: TokenStorageService) {
  }

  private handleError(error: HttpErrorResponse) {
    if (error.status === 504) {
      return throwError(() => new LoginTimeoutException());
    }
    else if (error.status === 401) {
      return throwError(() => new InvalidCredentialsException());
    }
    // Return an observable with a user-facing error message.
    return throwError(() => new Error('Something bad happened; please try again later.'));
  }

  private handleLogin(data: LoginResponse, onSuccessCb: () => void): void {
    this.tokenStorage.saveAccessToken(data.token);
    this.isLoggedIn = true;
    if (onSuccessCb)
      onSuccessCb();
  }

  public login(credentials: LoginCredentials, opts: authLoginOptions) {
    return this.http.post<LoginResponse>("/api/login", credentials)
      .pipe(retry({count: 3, delay: 1000}), catchError(this.handleError))
      .subscribe({
          next: (data: LoginResponse) => this.handleLogin(data, opts.onSuccess),
          error: err => {
            if (opts.onError)
              opts.onError(err);
          }
        });
  }

  public logout(): void {
    this.isLoggedIn = false;
    this.username = undefined;
    this.tokenStorage.clearAllTokens();
    this.router.navigate(['login']).then();
  }
}
