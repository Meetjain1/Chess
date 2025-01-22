import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BoardComponent } from './components/board/board.component';
import { GameComponent } from './components/game/game.component';
import { CoreService } from './core.service';
import { MovesComponent } from './components/moves/moves.component';

@NgModule({
  declarations: [
    BoardComponent,
    GameComponent,
    MovesComponent
  ],
  imports: [
    CommonModule
  ],
  providers: [CoreService],
  exports: [BoardComponent, GameComponent]
})
export class CoreModule { }
