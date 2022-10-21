import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DetailedProfileViewComponent } from './detailed-profile-view.component';
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {Profile} from "@app/services/profile/model/profile";
import {Subject} from "rxjs";
import {ProfileService} from "@app/services/profile/profile.service";

class MockProfileService {
  profileSwitched$ = new Subject<Profile>();
  currentProfile: Profile | undefined =  {
    "firstname": "John",
    "lastname": "Doe",
    "balance": 50000,
    "id": 1
  }
}

describe('DetailedProfileViewComponent', () => {
  let component: DetailedProfileViewComponent;
  let fixture: ComponentFixture<DetailedProfileViewComponent>;
  let profileService: MockProfileService;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DetailedProfileViewComponent ],
      imports: [HttpClientTestingModule],
      providers: [
        {provider: ProfileService, useClass: MockProfileService}
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DetailedProfileViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    profileService = TestBed.inject(ProfileService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("should display readonly field with firstname of the current profile", () => {
    const html = fixture.nativeElement;

  });
});
