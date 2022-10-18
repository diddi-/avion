import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {MaterialModule} from "./material.module";
import {FormlyModule} from "@ngx-formly/core";
import {FormlyMaterialModule} from "@ngx-formly/material";
import {ReactiveFormsModule} from "@angular/forms";
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './view-components/app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormlyMaterialExtrasModule } from './formly.material.extras.module';
import { LoginComponent } from './view-components/login/login.component';
import { AuthInterceptor } from './interceptors/auth-interceptor';
import { DrawerRailModule } from 'angular-material-rail-drawer';
import { HomeComponent } from './view-components/home/home.component';
import { CreateProfileComponent } from './view-components/profile/create-profile/create-profile.component';
import { ProfileSelectorComponent } from './view-components/profile/profile-selector/profile-selector.component';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    HomeComponent,
    CreateProfileComponent,
    ProfileSelectorComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MaterialModule,
    ReactiveFormsModule,
    FormlyModule.forRoot({
      types: [
      ],
      validators: [
      ],
      validationMessages: [
      ],
    }),
    FormlyMaterialModule,
    BrowserAnimationsModule,
    FormlyMaterialExtrasModule,
    HttpClientModule,
    DrawerRailModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
