import {ComponentFixture, TestBed} from '@angular/core/testing';

import {CreateProfileComponent} from './create-profile.component';
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {AppModule} from "@app/app.module";

describe('CreateProfileComponent', () => {
  let component: CreateProfileComponent;
  let fixture: ComponentFixture<CreateProfileComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreateProfileComponent ],
      imports: [HttpClientTestingModule, AppModule]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
