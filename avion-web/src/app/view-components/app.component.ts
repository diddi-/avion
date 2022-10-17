import {Component, OnInit} from '@angular/core';
import {NavigationStart, Router} from "@angular/router";
import {filter} from "rxjs";

import { AuthService } from '../services/auth/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  title = 'Avion Web';

  public isMenuOpen: boolean = false;

  constructor(private router: Router, public authService: AuthService) {
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
  }

  ngOnInit() {
    this.router.events
      .pipe(filter(evt => evt instanceof NavigationStart))
      .subscribe(evt => this.isMenuOpen = false)
  }
}
