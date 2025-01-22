import { Move } from 'src/app/core/models/moves.interface';
import { Piece } from 'src/app/core/models/piece.interface';

export interface Board { 
    '1': BoardRow,
    '2': BoardRow,
    '3': BoardRow,
    '4': BoardRow,
    '5': BoardRow,
    '6': BoardRow,
    '7': BoardRow,
    '8': BoardRow,
}

export interface BoardColor { 
    '1': BoardColorRow,
    '2': BoardColorRow,
    '3': BoardColorRow,
    '4': BoardColorRow,
    '5': BoardColorRow,
    '6': BoardColorRow,
    '7': BoardColorRow,
    '8': BoardColorRow,
}

export interface BoardCircle { 
    '1': BoardCircleRow,
    '2': BoardCircleRow,
    '3': BoardCircleRow,
    '4': BoardCircleRow,
    '5': BoardCircleRow,
    '6': BoardCircleRow,
    '7': BoardCircleRow,
    '8': BoardCircleRow,
}

export interface Stats { 
    death: Piece[] | null,
    isBlackCheck: boolean,
    isBlackCheckMate: boolean,
    isWhiteCheck: boolean,
    isWhiteCheckMate: boolean
}

export interface BoardRow { 
    a: Piece | null,
    b: Piece | null,
    c: Piece | null,
    d: Piece | null,
    e: Piece | null,
    f: Piece | null,
    g: Piece | null,
    h: Piece | null,
}

export interface BoardColorRow { 
    a: string | null,
    b: string | null,
    c: string | null,
    d: string | null,
    e: string | null,
    f: string | null,
    g: string | null,
    h: string | null,
}

export interface BoardCircleRow { 
    a: boolean | null,
    b: boolean | null,
    c: boolean | null,
    d: boolean | null,
    e: boolean | null,
    f: boolean | null,
    g: boolean | null,
    h: boolean | null,
}