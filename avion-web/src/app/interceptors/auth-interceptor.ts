import { Injectable } from '@angular/core';
import {
  HttpEvent, HttpInterceptor, HttpHandler, HttpRequest
} from '@angular/common/http';

import { Observable } from 'rxjs';
import { AuthService } from '../services/auth/auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler):
    Observable<HttpEvent<any>> {
    if(this.authService.isLoggedIn) {
      const authToken = localStorage.getItem("token");
      const authReq = req.clone({
            headers: req.headers.set('Authorization', "Bearer " + authToken)
          });
      return next.handle(authReq);
    }

    // Default do nothing
    return next.handle(req);
  }
}