import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { BoardComponent } from './components/board/board.component';
import { GameComponent  } from './components/game/game.component';

const routes: Routes = [
    // {path: 'board', component: BoardComponent },
    {path: 'game', component: GameComponent },
    {path: '**', component: GameComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CoreRoutingModule { }
