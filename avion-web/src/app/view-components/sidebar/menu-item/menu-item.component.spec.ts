import {ComponentFixture, TestBed} from '@angular/core/testing';

import {MenuItemComponent} from './menu-item.component';
import {AppModule} from "@app/app.module";

describe('MenuItemComponent HTML', () => {
  let component: MenuItemComponent;
  let fixture: ComponentFixture<MenuItemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MenuItemComponent ],
      imports: [AppModule],
    })
    .compileComponents();

    fixture = TestBed.createComponent(MenuItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it("should display the material icon", () => {
    component.icon = "dashboard";
    fixture.detectChanges();
    const html: HTMLElement = fixture.nativeElement;
    expect(html.querySelector("mat-icon")?.textContent).toBe(component.icon);
  });

  it("should link to the right place", () => {
    component.link = "/my/home";
    fixture.detectChanges();
    const html: HTMLElement = fixture.nativeElement;
    const linkAttribute = html.querySelector("a")?.getAttribute("href");
    expect(linkAttribute?.toString()).toBe(component.link);
  });

  it("should display the menu item text", () => {
    component.text = "my menu item";
    fixture.detectChanges();
    const html: HTMLElement = fixture.nativeElement;
    expect(html.querySelector("p")?.textContent).toContain(component.text);
  });

  it("should display tooltip after the menu item", () => {
    component.text = "my menu item";
    fixture.detectChanges();
    const html: HTMLElement = fixture.nativeElement;
    const aLink: HTMLAnchorElement = html.querySelector("a")!;
    expect(aLink.getAttribute("ng-reflect-position")).toBe("after");
    expect(aLink.getAttribute("ng-reflect-message")).toBe(component.text);
  });
});
