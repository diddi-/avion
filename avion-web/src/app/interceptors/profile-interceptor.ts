import { Injectable } from '@angular/core';
import {
  HttpEvent, HttpInterceptor, HttpHandler, HttpRequest
} from '@angular/common/http';

import { Observable } from 'rxjs';
import { ProfileService } from '@app/services/profile/profile.service';

@Injectable()
export class ProfileInterceptor implements HttpInterceptor {

  constructor(private profileService: ProfileService) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler):
    Observable<HttpEvent<any>> {
    try {
      const profileId = this.profileService.getCurrentProfileId();
      const profileReq = req.clone({
        headers: req.headers.set('X-PROFILE-ID', profileId.toString())
      });
        return next.handle(profileReq);
    }
    catch(e) {
      // Ignore for now.
    }

    // Default do nothing
    return next.handle(req);
  }
}
