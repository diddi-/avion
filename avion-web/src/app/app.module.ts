import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {MaterialModule} from "./material.module";
import {FormlyModule} from "@ngx-formly/core";
import {FormlyMaterialModule} from "@ngx-formly/material";
import {ReactiveFormsModule} from "@angular/forms";
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './view-components/app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormlyMaterialExtrasModule } from './formly.material.extras.module';
import { LoginComponent } from './view-components/login/login.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
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
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
