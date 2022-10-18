import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { retry } from 'rxjs/operators';
import { Observable, Subject } from 'rxjs';
import { CreateProfileParams } from './model/create-profile-params';
import { Profile } from './model/profile';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {
  public profileSwitched$ = new Subject<Profile>();


  public currentProfile: Profile | undefined;
  public profilesList: Profile[] = [];

  constructor(private http: HttpClient) {
  }

  private onProfilesListUpdate(): void {
    const profileId = this.getCurrentProfileId();
    if(!profileId)
      return;

    this.profilesList.forEach(p => {
      if(p.id === profileId)
        this.switchProfile(p);
    })
  }

  public createProfile(params: CreateProfileParams): void {
    this.http.post<Profile>("/api/profiles", params)
      .pipe(retry({count: 3, delay: 1000}))
      .subscribe((p) => this.switchProfile(p));
  }

  public getCurrentProfileId(): number {
    const profileId = localStorage.getItem("currentProfileId");
    if(!profileId)
      throw new Error("No current profile selected");

    return parseInt(profileId);
  }

  public updateProfilesList(): void {
    this.http.get<Profile[]>("/api/profiles")
      .subscribe(plist => {
        this.profilesList = plist;
        this.onProfilesListUpdate();
      });
  }

  public switchProfile(profile: Profile): void {
    localStorage.setItem("currentProfileId", profile.id.toString());
    this.currentProfile = profile;
    this.profileSwitched$.next(profile);
  }

  public getDetailedProfile(): Observable<Profile> {
    return this.http.get<Profile>("/api/profile");
  }
}
