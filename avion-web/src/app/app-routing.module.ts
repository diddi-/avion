import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './view-components/login/login.component';
import { HomeComponent } from './view-components/home/home.component';
import { CreateProfileComponent } from './view-components/profile/create-profile/create-profile.component';
import { CreateCompanyComponent } from '@app/view-components/company/create-company/create-company.component';
import { DetailedProfileViewComponent } from "@app/view-components/profile/detailed-profile-view/detailed-profile-view.component";
import { RegisterComponent } from "@app/view-components/register/register.component";

const routes: Routes = [
  {
    path: '',
    children: [
      {path: '', redirectTo: 'home', pathMatch: 'full'},
      {path: 'home', component: HomeComponent},
      {
        path: 'profile',
        children: [
          {path: '', component: DetailedProfileViewComponent},
          {path: 'new', component: CreateProfileComponent}
        ]
      },
      {
        path: 'company',
        children: [
          {path: 'new', component: CreateCompanyComponent}
        ]
      },
    ]
  },
  {path: 'login', component: LoginComponent},
  {path: 'register', component: RegisterComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
