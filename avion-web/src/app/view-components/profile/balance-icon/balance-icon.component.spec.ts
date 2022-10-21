import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BalanceIconComponent } from './balance-icon.component';

describe('BalanceIconComponent', () => {
  let component: BalanceIconComponent;
  let fixture: ComponentFixture<BalanceIconComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BalanceIconComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BalanceIconComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
