import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { retry } from 'rxjs/operators';
import { CreateProfileParams } from './model/create-profile-params';
import { Profile } from './model/profile';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  public currentProfile: Profile | null = null;

  constructor(private http: HttpClient) { }

  public createProfile(params: CreateProfileParams): void {
    this.http.post<Profile>("/api/profile", params)
    .pipe(retry({count: 3, delay: 1000}))
    .subscribe({
      next: (profile: Profile) => this.switchProfile(profile)
    });
  }

  public switchProfile(profile: Profile): void {
    this.currentProfile = profile;
    localStorage.setItem("currentProfileId", profile.id.toString());
    console.log(`Switched to profile: ${profile.firstname} ${profile.lastname}`)
  }

}
