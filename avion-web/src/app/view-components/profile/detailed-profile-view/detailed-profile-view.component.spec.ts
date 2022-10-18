import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DetailedProfileViewComponent } from './detailed-profile-view.component';

describe('DetailedViewComponent', () => {
  let component: DetailedProfileViewComponent;
  let fixture: ComponentFixture<DetailedProfileViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DetailedProfileViewComponent ]
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
