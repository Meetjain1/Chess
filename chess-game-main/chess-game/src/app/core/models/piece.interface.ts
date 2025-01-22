import { Move } from 'src/app/core/models/moves.interface';

export interface Piece { 
    type: string,
    isWhite: boolean,
    //position: string,
    isDead: boolean,
    moves: Move[]
    unmoved?: boolean;
}
