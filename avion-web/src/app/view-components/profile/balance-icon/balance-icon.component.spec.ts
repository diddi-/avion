import {ComponentFixture, TestBed} from '@angular/core/testing';

import {BalanceIconComponent} from './balance-icon.component';
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {MaterialModule} from "@app/material.module";
import {Subject} from "rxjs";
import {Profile} from "@app/services/profile/model/profile";
import {ProfileService} from "@app/services/profile/profile.service";

class MockProfileService {
  profileSwitched$ = new Subject<Profile>();
  currentProfile: Profile | undefined = {
    "firstname": "John",
    "lastname": "Doe",
    "balance": 0,
    "id": 1
  }
}

describe('BalanceIconComponent', () => {
  let component: BalanceIconComponent;
  let fixture: ComponentFixture<BalanceIconComponent>;
  let profileService: MockProfileService;
  let balanceComponent: BalanceIconComponent;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HttpClientTestingModule, MaterialModule],
      declarations: [BalanceIconComponent],
      providers: [
        BalanceIconComponent,
        {provide: ProfileService, useClass: MockProfileService}
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(BalanceIconComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    balanceComponent = TestBed.inject(BalanceIconComponent);
    profileService = TestBed.inject(ProfileService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("should update balance when profile data is updated", () => {
    expect(component.balance).toBe(0);
    const profile: Profile = {
      "firstname": "John",
      "lastname": "Doe",
      "balance": 1500,
      "id": 1
    };
    profileService.profileSwitched$.next(profile);
    expect(component.balance).toBe(profile.balance);
  });

  it("should read current profile balance on init", () => {
    const expected_balance = 50000;
    if(profileService.currentProfile?.balance !== undefined) // TS2779
      profileService.currentProfile.balance = expected_balance;
    expect(component.balance).toBe(0);
    component.ngOnInit();
    expect(component.balance).toBe(expected_balance);
  })
});
