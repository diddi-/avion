import { Component, OnInit } from '@angular/core';
import { ProfileService } from '@app/services/profile/profile.service';
import { Profile } from '@app/services/profile/model/profile';

@Component({
  selector: 'app-profile-selector',
  templateUrl: './profile-selector.component.html',
  styleUrls: ['./profile-selector.component.scss']
})
export class ProfileSelectorComponent implements OnInit {

  constructor(private profileService: ProfileService) { }

  ngOnInit(): void {
  }

  public hasProfileSelected(): boolean {
    if(this.profileService.currentProfile !== undefined)
      return true;
    return false;
  }

  public getCurrentProfileName(): string | undefined {
    if(!this.hasProfileSelected())
      throw new Error("FAIL");

    const profile = this.profileService.currentProfile;
    return `${profile?.firstname} ${profile?.lastname}`;
  }

}
