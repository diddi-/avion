import {Component, OnInit} from '@angular/core';
import {FormlyFieldConfig} from "@ngx-formly/core";
import {UntypedFormGroup} from "@angular/forms";
import {CompanyService} from "@app/services/company/company.service";
import {CreateCompanyParams} from "@app/services/company/model/create-company-params";
import {Router} from '@angular/router';

@Component({
  selector: 'app-create-company',
  templateUrl: './create-company.component.html',
  styleUrls: ['./create-company.component.scss']
})
export class CreateCompanyComponent implements OnInit {
  form = new UntypedFormGroup({});
  model = {};
  fields: FormlyFieldConfig[] = [
    {
      key: 'name',
      type: 'input',
      focus: true,
      templateOptions: {
        label: 'Company name',
        required: true
      }
    },
  ]

  constructor(private companyService: CompanyService,
              private router: Router) {
  }

  ngOnInit(): void {
  }

  public onSubmit() {
    this.companyService.createCompany(<CreateCompanyParams>this.model);
    this.router.navigate(["home"]).then();
  }
}
