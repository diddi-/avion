import {Component, ContentChild, ElementRef, Input, OnInit, TemplateRef, ViewChild} from '@angular/core';

@Component({
  selector: 'app-menu-item',
  templateUrl: './menu-item.component.html',
  styleUrls: ['./menu-item.component.scss']
})
export class MenuItemComponent implements OnInit {
  @Input() link: string = "";
  @Input() icon: string = "label";
  @Input() text: string = "";


  constructor() { }

  ngOnInit(): void {
  }

}
