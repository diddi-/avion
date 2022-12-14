import {Component, OnInit} from '@angular/core';
import {FormlyFieldConfig} from "@ngx-formly/core";
import {UntypedFormGroup} from "@angular/forms";
import {ProfileService} from '@app/services/profile/profile.service';
import {CreateProfileParams} from '@app/services/profile/model/create-profile-params';
import {Router} from "@angular/router";

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

  constructor(private profileService: ProfileService,
              private router: Router) {
  }

  ngOnInit(): void {
  }

  public onSubmit() {
    this.profileService.createProfile(<CreateProfileParams>this.model);
    this.router.navigate(["home"]).then();
  }
}
