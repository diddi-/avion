import { Injectable } from '@angular/core';
import {Router} from "@angular/router";
import {LoginCredentials} from "./login-credentials";
import {LoginResponse} from "./login-response";
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError, TimeoutError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { LoginTimeoutException } from './exceptions/login-timeout';
import { PasswordMismatchException } from './exceptions/password-mismatch-exception';
import { RegistrationTimeoutException } from './exceptions/registration-timeout';
import { InvalidCredentialsException } from './exceptions/invalid-credentials-exception';
import { authLoginOptions } from './auth-login-options';
import { TokenStorageService } from '../token/token-storage.service';
import { CreateAccountParams } from "@app/services/auth/create-account-params";
import { RegistrationResponse } from "@app/services/auth/registration-response";
import { JwtToken } from "@app/services/token/jwt-token";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  public username: string | undefined = 'admin';
  redirectUrl: string | null = null;

  private token: JwtToken | undefined = undefined;

  constructor(private router: Router, private http: HttpClient,
              private tokenStorage: TokenStorageService) {

    if(this.tokenStorage.hasAccessToken()) {
      this.token = JwtToken.fromString(this.tokenStorage.getAccessToken());
      this.username = this.token.getUsername();
    }
  }

  public isLoggedIn() {
    if(this.token === undefined)
      return false;
    return !this.token?.isExpired();
  }

  private handleRegistrationError(error: HttpErrorResponse) {
    if (error.status === 504) {
      return throwError(() => new RegistrationTimeoutException());
    }
    // Return an observable with a user-facing error message.
    return throwError(() => new Error('Something bad happened; please try again later.'));
  }

  public registerAccount(params: CreateAccountParams, onSuccessCb: () => void, onErrorCb: (err: Error) => void) {
    if (params.password !== params.confirmPassword)
      throw new PasswordMismatchException();

    return this.http.post<RegistrationResponse>("/api/account", {
      "firstname": params.firstname,
      "lastname": params.lastname,
      "email": params.email,
      "password": params.password
    })
      .pipe(retry({count: 3, delay: 1000}), catchError(this.handleRegistrationError))
      .subscribe({
          next: () => onSuccessCb(),
          error: err => onErrorCb(err)
        });
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
    this.token = JwtToken.fromString(data.token);
    this.username = this.token.getUsername();
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

      /* DO WE NEED TO UNSUBSCRIBE HERE ???? */
  }

  public logout(): void {
    this.username = undefined;
    this.token = undefined;
    this.tokenStorage.clearAllTokens();
    this.router.navigate(['login']).then();
  }
}
