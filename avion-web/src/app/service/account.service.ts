import { Injectable } from '@angular/core';
import { AccountParams } from './accountparams';

@Injectable({
  providedIn: 'root'
})
export class AccountService {

  constructor() { }

  register(user: AccountParams): void {
    window.alert(`Thank you ${user.firstname}!`);
  }
}
