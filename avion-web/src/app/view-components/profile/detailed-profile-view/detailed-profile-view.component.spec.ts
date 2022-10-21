import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DetailedProfileViewComponent } from './detailed-profile-view.component';
import {HttpClientTestingModule} from "@angular/common/http/testing";

describe('DetailedProfileViewComponent', () => {
  let component: DetailedProfileViewComponent;
  let fixture: ComponentFixture<DetailedProfileViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DetailedProfileViewComponent ],
      imports: [HttpClientTestingModule]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DetailedProfileViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
