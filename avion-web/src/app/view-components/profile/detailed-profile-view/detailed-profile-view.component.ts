import { Component, OnInit } from '@angular/core';
import { ProfileService } from "@app/services/profile/profile.service";
import {UntypedFormGroup} from "@angular/forms";
import {FormlyFieldConfig} from "@ngx-formly/core";
import { Profile } from "@app/services/profile/model/profile";
@Component({
  selector: 'app-detailed-profile-view',
  templateUrl: './detailed-profile-view.component.html',
  styleUrls: ['./detailed-profile-view.component.scss']
})
export class DetailedProfileViewComponent implements OnInit {
  public isLoading: boolean = true;
  form = new UntypedFormGroup({});
  model = {};
  fields: FormlyFieldConfig[] = [
    {
      key: 'firstname',
      type: 'input',
      focus: true,
      templateOptions: {
      readonly: true,
        label: 'First name',
      }
    },
    {
      key: 'lastname',
      type: 'input',
      templateOptions: {
      readonly: true,
        label: 'Last name',
      }
    },
    {
      key: 'balance',
      type: 'input',
      templateOptions: {
      readonly: true,
        label: 'Balance',
      }
    },
  ]
  constructor(private profileService: ProfileService) { }

  ngOnInit(): void {
    this.profileService.profileSwitched$.subscribe(p => this.getDetailedProfile());
    this.getDetailedProfile();
  }

  public getDetailedProfile(): void {
     this.profileService.getDetailedProfile()
      .subscribe((p) => {
        this.model = p;
        this.isLoading = false;
      });
  }

}
