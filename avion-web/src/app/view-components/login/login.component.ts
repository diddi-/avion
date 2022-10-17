import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../services/auth/auth.service";
import {Router} from "@angular/router";
import {UntypedFormGroup} from "@angular/forms";
import {FormlyFieldConfig} from "@ngx-formly/core";
import {LoginResponse} from "../../services/auth/login-response";
import {LoginCredentials} from "../../services/auth/login-credentials";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit{
  loading = false;

  form = new UntypedFormGroup({});
  model = {};
  fields: FormlyFieldConfig[] = [
    {
      key: 'username',
      type: 'input',
      templateOptions: {
        label: 'Username',
        required: true
      }
    },
    {
      key: 'password',
      type: 'input',
      templateOptions: {
        label: 'Password',
        required: true
      }
    },
  ];

  errorMsg: string | null = null;

  constructor(public authService: AuthService, public router: Router) {
  }

  ngOnInit(): void {
    if (this.authService.isLoggedIn) {
      this.router.navigate(['home']).then()
    }
  }

  onLoginError(err: Error): void {
    this.errorMsg = err.toString();
    console.log(err);
    this.loading = false;
  }

  onLoginSuccess(): void {
    this.loading = false;
    this.router.navigate(['home']).then(() => location.reload());
  }

  login() {
    this.loading = true;
    this.authService.login(
      <LoginCredentials>this.model,
      {
        onSuccess: () => this.onLoginSuccess(),
        onError: (err) => this.onLoginError(err)
      });
  }
}
