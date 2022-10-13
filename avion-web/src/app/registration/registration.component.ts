import { Component, OnInit } from '@angular/core';
import { NonNullableFormBuilder } from '@angular/forms';
import { AccountService } from '../service/account.service';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})
export class RegistrationComponent implements OnInit {

  registrationForm = this.formBuilder.group({
    firstname: '',
    lastname: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  submitDisabled = true;

  onPasswordInput(): void {
      if(this.registrationForm.get("password")?.value === this.registrationForm.get("confirmPassword")?.value) {
        this.submitDisabled = false;
      }
      else {
        this.submitDisabled = true;
      }
  }

  constructor(private formBuilder: NonNullableFormBuilder,
              private accountService: AccountService) { }

  ngOnInit(): void {
  }

  onSubmit(): void {
    console.log(this.registrationForm.value);
    this.accountService.register(this.registrationForm.getRawValue());
    //this.registrationForm.reset();
  }
}
