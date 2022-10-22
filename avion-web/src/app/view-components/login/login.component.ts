import {Component, OnInit} from '@angular/core';
import {AuthService} from "@app/services/auth/auth.service";
import {ActivatedRoute, Router} from "@angular/router";
import {UntypedFormGroup} from "@angular/forms";
import {FormlyFieldConfig} from "@ngx-formly/core";
import {LoginCredentials} from "@app/services/auth/login-credentials";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loading = false;
  returnUrl: string | undefined = undefined;
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
        required: true,
        type: "password",
      }
    },
  ];

  errorMsg: string | null = null;

  constructor(public authService: AuthService, public router: Router,
              private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['home']).then()
    }

    this.route.queryParams.subscribe(params => {
      if ("returnUrl" in params)
        this.returnUrl = params["returnUrl"];
    });
  }

  onLoginError(err: Error): void {
    this.errorMsg = err.toString();
    this.loading = false;
  }

  onLoginSuccess(): void {
    this.loading = false;
    const returnUrl = this.returnUrl ? this.returnUrl : "home";
    this.router.navigate([returnUrl]).then(() => location.reload());
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
