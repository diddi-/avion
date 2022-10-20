import { Component, OnInit } from '@angular/core';
import {FormlyFieldConfig} from "@ngx-formly/core";
import {UntypedFormGroup} from "@angular/forms";
import {CreateAccountParams} from "@app/services/auth/create-account-params";
import {AuthService} from "@app/services/auth/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})

export class RegisterComponent implements OnInit {
  form = new UntypedFormGroup({});
  model: any = {};
  fields: FormlyFieldConfig[] = [
    {
      key: 'firstname',
      type: 'input',
      focus: true,
      templateOptions: {
        label: 'First name',
        required: true
      }
    },
    {
      key: 'lastname',
      type: 'input',
      templateOptions: {
        label: 'Last name',
        required: true
      }
    },
    {
      key: 'email',
      type: 'input',
      templateOptions: {
        label: 'Email',
        required: true
      }
    },
    {
      key: 'password',
      type: 'input',
      templateOptions: {
        label: 'Password',
        required: true,
        type: 'password'
      }
    },
    {
      key: 'confirmPassword',
      type: 'input',
      templateOptions: {
        label: 'Confirm password',
        required: true,
        type: 'password'
      },
      validators: {
        fieldMatch: {
          expression: (control: any) => control.value === this.model.password,
          message: 'Passwords must be same',
        }
      },
    },
  ]
  errorMsg: string | undefined = undefined;
  loading: boolean = false;

  onRegistrationError(err: Error): void {
    this.errorMsg = err.toString();
    this.loading = false;
  }

  onRegistrationSuccess(): void {
    this.loading = false;
    this.router.navigate(['login']).then(() => location.reload());
  }

  constructor(public authService: AuthService, public router: Router) { }

  ngOnInit(): void {
  }

  public onSubmit() {
    this.loading = true;
    this.authService.registerAccount(
      <CreateAccountParams>this.model,
      () => this.onRegistrationSuccess(),
      (err) => this.onRegistrationError(err));
  }
}
