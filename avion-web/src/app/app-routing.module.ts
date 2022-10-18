import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './view-components/login/login.component';
import { HomeComponent } from './view-components/home/home.component';
import { CreateProfileComponent } from './view-components/profile/create-profile/create-profile.component';

const routes: Routes = [
  {
    path: '',
    children: [
      {path: '', redirectTo: 'home', pathMatch: 'full'},
      {path: 'home', component: HomeComponent},
      {
        path: 'profile',
        children: [
          {path: 'new', component: CreateProfileComponent}
        ]
      }
    ]
  },
  {path: 'login', component: LoginComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
