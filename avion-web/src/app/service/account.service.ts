import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AccountParams } from './accountparams';
import { AccountRegistrationResponse } from './account_registration_response';

@Injectable({
  providedIn: 'root'
})
export class AccountService {

  constructor(private http: HttpClient) { }

  register(user: AccountParams): void {
    if(user.password != user.confirmPassword) {
      throw new Error("Passwords don't match");
    }
    const response = this.http.post<AccountRegistrationResponse>("http://localhost:5000/account", {
      firstname: user.firstname,
      lastname: user.lastname,
      email: user.email,
      password: user.password
      }).subscribe((data: AccountRegistrationResponse) => window.alert(`Thank you ${user.firstname}! You are our number ${data.id} <3`));
  }
}
