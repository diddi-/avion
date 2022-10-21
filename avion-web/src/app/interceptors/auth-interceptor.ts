import { Injectable } from '@angular/core';
import {
  HttpEvent, HttpInterceptor, HttpHandler, HttpRequest
} from '@angular/common/http';

import { Observable } from 'rxjs';
import { AuthService } from '../services/auth/auth.service';
import { TokenStorageService } from '../services/token/token-storage.service';
import { TokenNotFoundException } from '../services/token/exceptions/token-not-found-exception';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService,
              private tokenStorage: TokenStorageService) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler):
    Observable<HttpEvent<any>> {
    if(this.authService.isLoggedIn()) {
      try {
        const authToken = this.tokenStorage.getAccessToken();
        const authReq = req.clone({
              headers: req.headers.set('Authorization', "Bearer " + authToken)
            });
        return next.handle(authReq);
      }
      catch(e) {
        if (!(e instanceof TokenNotFoundException)) // Ignore this exception
          throw e;
      }
    }

    // Default do nothing
    return next.handle(req);
  }
}
