import { Component, OnInit } from '@angular/core';
import { ProfileService } from '@app/services/profile/profile.service';
import { Profile } from '@app/services/profile/model/profile';

@Component({
  selector: 'app-profile-selector',
  templateUrl: './profile-selector.component.html',
  styleUrls: ['./profile-selector.component.scss']
})
export class ProfileSelectorComponent implements OnInit {
  public currentProfile: Profile | undefined;

  constructor(private profileService: ProfileService) { }

  ngOnInit(): void {
    this.profileService.profileSwitched$.subscribe(p => this.currentProfile = p);
  }

  public hasProfileSelected(): boolean {
    if(this.currentProfile !== undefined)
      return true;
    return false;
  }

  public getCurrentProfileName(): string {
    if(!this.hasProfileSelected())
      throw new Error("FAIL");

    return `${this.currentProfile?.firstname} ${this.currentProfile?.lastname}`;
  }

}
