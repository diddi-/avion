import {Component, OnInit} from '@angular/core';
import {ProfileService} from "@app/services/profile/profile.service";

@Component({
  selector: 'app-balance-icon',
  templateUrl: './balance-icon.component.html',
  styleUrls: ['./balance-icon.component.scss']
})
export class BalanceIconComponent implements OnInit {
  public balance: number = 0;

  constructor(private profileService: ProfileService) { }

  ngOnInit(): void {
    this.profileService.profileSwitched$.subscribe(p => this.balance = p.balance);
    this.balance = this.profileService.currentProfile?.balance ? this.profileService.currentProfile?.balance : 0;
  }

}
