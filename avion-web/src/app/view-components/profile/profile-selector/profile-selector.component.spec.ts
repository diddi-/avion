import {ComponentFixture, TestBed} from '@angular/core/testing';

import {ProfileSelectorComponent} from './profile-selector.component';
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {AppModule} from "@app/app.module";
import {Subject} from "rxjs";
import {Profile} from "@app/services/profile/model/profile";
import {ProfileService} from "@app/services/profile/profile.service";


export const spyGetter = <T, K extends keyof T>(target: jasmine.SpyObj<T>, key: K): jasmine.Spy => {
  return Object.getOwnPropertyDescriptor(target, key)?.get as jasmine.Spy;
};

export const spySetter = <T, K extends keyof T>(target: jasmine.SpyObj<T>, key: K): jasmine.Spy => {
  return Object.getOwnPropertyDescriptor(target, key)?.set as jasmine.Spy;
};

describe('ProfileSelectorComponent', () => {
  let component: ProfileSelectorComponent;
  let fixture: ComponentFixture<ProfileSelectorComponent>;
  let profileService: jasmine.SpyObj<ProfileService>;

  beforeEach(async () => {
    const spy = jasmine.createSpyObj<ProfileService>("ProfileService",
      ["updateProfilesList"], ["currentProfile", "profileSwitched$", "profilesList"]);
      spyGetter(spy, "profileSwitched$").and.returnValue(new Subject<Profile>());
      spyGetter(spy, "profilesList").and.returnValue([]);

    await TestBed.configureTestingModule({
      declarations: [ProfileSelectorComponent],
      imports: [HttpClientTestingModule, AppModule],
      providers: [
        ProfileSelectorComponent,
        {provide: ProfileService, useValue: spy}
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ProfileSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    profileService = TestBed.inject(ProfileService) as jasmine.SpyObj<ProfileService>;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

describe("ProfileSelectorComponent HTML", () => {
  let component: ProfileSelectorComponent;
  let fixture: ComponentFixture<ProfileSelectorComponent>;
  let profileService: jasmine.SpyObj<ProfileService>;

  beforeEach(async () => {
    const spy = jasmine.createSpyObj<ProfileService>("ProfileService",
      ["updateProfilesList"], ["currentProfile", "profileSwitched$", "profilesList"]);
    spyGetter(spy, "profileSwitched$").and.returnValue(new Subject<Profile>());
    spyGetter(spy, "profilesList").and.returnValue([]);
    spyGetter(spy, "currentProfile").and.returnValue({
      "firstname": "John",
      "lastname": "Doe",
      "balance": 0,
      "id": 1
    });

    await TestBed.configureTestingModule({
      declarations: [ProfileSelectorComponent],
      imports: [HttpClientTestingModule, AppModule],
      providers: [
        {provide: ProfileService, useValue: spy}
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(ProfileSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    profileService = TestBed.inject(ProfileService) as jasmine.SpyObj<ProfileService>;
  });

  it("should display selected profile", () => {
    if(profileService.currentProfile)
      profileService.profileSwitched$.next(profileService.currentProfile);
    fixture.detectChanges();
    expect(component.currentProfile).toBeDefined();
    const html: HTMLElement = fixture.nativeElement;
    const value = html.querySelector("#selected-profile");
    expect(profileService.currentProfile).toBeDefined();
    expect(value?.textContent).toContain(component.getCurrentProfileName());
  })
});
