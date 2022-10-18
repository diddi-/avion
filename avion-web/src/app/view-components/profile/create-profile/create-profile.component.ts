import { Component, OnInit } from '@angular/core';
import {FormlyFieldConfig} from "@ngx-formly/core";
import {UntypedFormGroup} from "@angular/forms";

@Component({
  selector: 'app-create-profile',
  templateUrl: './create-profile.component.html',
  styleUrls: ['./create-profile.component.scss']
})
export class CreateProfileComponent implements OnInit {
  form = new UntypedFormGroup({});
  model = {};
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
  ]
  constructor() { }

  ngOnInit(): void {
  }

  public onSubmit() {
    console.log("Submitting profile..");
  }
}
