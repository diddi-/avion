/*
 * This module imports and re-exports all extra Formly Material types for convenience,
 * so only 1 module import is needed in app.module.
 *
 * To optimize your production builds, you should only import the components used in your app.
 */
import { NgModule } from '@angular/core';
import {FormlyMatDatepickerModule} from "@ngx-formly/material/datepicker";
import {FormlyMatToggleModule} from "@ngx-formly/material/toggle";
import {FormlyMatSliderModule} from "@ngx-formly/material/slider";
@NgModule({
  exports: [
    FormlyMatDatepickerModule,  // 'datepicker'
    FormlyMatSliderModule,  // 'slider'
    FormlyMatToggleModule,  // 'toggle'
  ]
})
export class FormlyMaterialExtrasModule {}
