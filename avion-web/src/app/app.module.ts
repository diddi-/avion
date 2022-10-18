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
import { DrawerRailModule } from 'angular-material-rail-drawer';
import { HomeComponent } from './view-components/home/home.component';
import { CreateProfileComponent } from './view-components/profile/create-profile/create-profile.component';
import { ProfileSelectorComponent } from './view-components/profile/profile-selector/profile-selector.component';
import { CreateCompanyComponent } from './view-components/company/create-company/create-company.component';
import { httpInterceptorProviders } from "@app/interceptors";
import { DetailedProfileViewComponent } from './view-components/profile/detailed-profile-view/detailed-profile-view.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    HomeComponent,
    CreateProfileComponent,
    ProfileSelectorComponent,
    CreateCompanyComponent,
    DetailedProfileViewComponent,
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
  providers: [httpInterceptorProviders],
  bootstrap: [AppComponent]
})
export class AppModule { }
