import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfileSelectorComponent } from './profile-selector.component';
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {MaterialModule} from "@app/material.module";

describe('ProfileSelectorComponent', () => {
  let component: ProfileSelectorComponent;
  let fixture: ComponentFixture<ProfileSelectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfileSelectorComponent ],
      imports: [HttpClientTestingModule, MaterialModule]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProfileSelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
