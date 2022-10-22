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

  constructor(public profileService: ProfileService) { }

  ngOnInit(): void {
    this.profileService.profileSwitched$.subscribe(p => this.currentProfile = p);
    this.profileService.updateProfilesList();
  }

  public hasProfileSelected(): boolean {
    return this.profileService.currentProfile !== undefined;

  }

  public getCurrentProfileName(): string {
    return `${this.currentProfile?.firstname} ${this.currentProfile?.lastname}`;
  }

  public getProfileSelectionList(): Profile[] {
    return this.profileService.profilesList.filter((p) => p !== this.currentProfile);
  }
}
