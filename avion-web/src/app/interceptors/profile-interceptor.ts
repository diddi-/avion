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
    if(this.profileService.currentProfile !== undefined) {
      const profileReq = req.clone({
            headers: req.headers.set('X-PROFILE-ID', this.profileService.currentProfile.id.toString())
          });
      return next.handle(profileReq);
    }

    // Default do nothing
    return next.handle(req);
  }
}
