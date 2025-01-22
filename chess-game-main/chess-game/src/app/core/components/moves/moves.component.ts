import { Component, Input, OnInit } from '@angular/core';
import { CoreService } from '../../core.service';

@Component({
  selector: 'app-moves',
  templateUrl: './moves.component.html',
  styleUrls: ['./moves.component.scss']
})
export class MovesComponent implements OnInit {
  @Input() moves;

  constructor(private coreService: CoreService) { }

  ngOnInit(): void {
    // console.log(this.moves)
  }

}
