import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { retry } from "rxjs/operators";
import { CreateCompanyParams } from "@app/services/company/model/create-company-params";
import { Company } from "@app/services/company/model/company";

@Injectable({
  providedIn: 'root'
})
export class CompanyService {

  constructor(private http: HttpClient) { }

  public createCompany(params: CreateCompanyParams): void {
    this.http.post<Company>("/api/company", params)
      .pipe(retry({count: 3, delay: 1000}))
      .subscribe();
  }

}
