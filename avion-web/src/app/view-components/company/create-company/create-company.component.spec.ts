import {ComponentFixture, TestBed} from '@angular/core/testing';

import {CreateCompanyComponent} from './create-company.component';
import {HttpClientTestingModule} from "@angular/common/http/testing";
import {AppModule} from "@app/app.module";

describe('CreateCompanyComponent', () => {
  let component: CreateCompanyComponent;
  let fixture: ComponentFixture<CreateCompanyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreateCompanyComponent ],
      imports: [HttpClientTestingModule, AppModule]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateCompanyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
