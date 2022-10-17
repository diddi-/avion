import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginComponent } from './login.component';
import {RouterTestingModule} from "@angular/router/testing";
import {MatCard, MatCardContent, MatCardSubtitle, MatCardTitle} from '@angular/material/card';
import {MessageSnackbarService} from "../../services/message-snackbar/message-snackbar.service";
import {
  MockMessageSnackbarService
} from "../../model/test-models/mock-message-snackbar-service.model";


describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule],
      providers: [ {
        provide: MessageSnackbarService,
        useClass: MockMessageSnackbarService
      }],
      declarations: [ LoginComponent, MatCard, MatCardTitle, MatCardSubtitle, MatCardContent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
