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
    // Nope, don't like this but will do for now.
    this.updateProfilesList(() => this.onProfilesListUpdate());
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
    this.http.post<Profile>("/api/profile", params)
      .pipe(retry({count: 3, delay: 1000}))
      .subscribe((p) => this.switchProfile(p));
  }

  public getCurrentProfileId(): number {
    const profileId = localStorage.getItem("currentProfileId");
    if(!profileId)
      throw new Error("No current profile selected");

    return parseInt(profileId);
  }

  public updateProfilesList(callback?: () => void): void {
    this.http.get<Profile[]>("/api/profile")
      .subscribe(plist => {
        this.profilesList = plist;
        if(callback)
          callback();
        });
  }

  public switchProfile(profile: Profile): void {
    this.profileSwitched$.next(profile);
  }

}
