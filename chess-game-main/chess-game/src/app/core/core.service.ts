import { Injectable } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import  { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';

import { Board, BoardCircle, BoardColor, Stats } from "./models/board.interface";
import { Piece } from 'src/app/core/models/piece.interface';
import { SelectedPlayer } from "./enums/selected-player";

@Injectable({
    providedIn: 'root'
})
export class CoreService { 

    baseURL: string = "https://1ososgx4a0.execute-api.us-east-1.amazonaws.com";
    // baseURL: string = "http://127.0.0.1:5000/";

    board: Board;
    stats: Stats;
    selectedPlayer: SelectedPlayer;
    moves: string[] = [];

    constructor (
        private http: HttpClient, 
        private breakpointObserver: BreakpointObserver
        ) {}

    observeBreakpoints(): Observable<BreakpointState> {
        return this.breakpointObserver.observe([
            Breakpoints.Handset, Breakpoints.Tablet, Breakpoints.Web
        ])
    };
    boardColor: BoardColor = { 
        1: { a: 'white', b: 'black', c: 'white', d: 'black', e: 'white', f: 'black', g: 'white', h: 'black' },
        2: { a: 'black', b: 'white', c: 'black', d: 'white', e: 'black', f: 'white', g: 'black', h: 'white' },
        3: { a: 'white', b: 'black', c: 'white', d: 'black', e: 'white', f: 'black', g: 'white', h: 'black' },
        4: { a: 'black', b: 'white', c: 'black', d: 'white', e: 'black', f: 'white', g: 'black', h: 'white' },
        5: { a: 'white', b: 'black', c: 'white', d: 'black', e: 'white', f: 'black', g: 'white', h: 'black' },
        6: { a: 'black', b: 'white', c: 'black', d: 'white', e: 'black', f: 'white', g: 'black', h: 'white' },
        7: { a: 'white', b: 'black', c: 'white', d: 'black', e: 'white', f: 'black', g: 'white', h: 'black' },
        8: { a: 'black', b: 'white', c: 'black', d: 'white', e: 'black', f: 'white', g: 'black', h: 'white' },
    }

    boardEmptyCircle(): BoardCircle {
        return { 
            1: { a: false, b: false, c: false, d: false, e: false, f: false, g: false, h: false },
            2: { a: false, b: false, c: false, d: false, e: false, f: false, g: false, h: false },
            3: { a: false, b: false, c: false, d: false, e: false, f: false, g: false, h: false },
            4: { a: false, b: false, c: false, d: false, e: false, f: false, g: false, h: false },
            5: { a: false, b: false, c: false, d: false, e: false, f: false, g: false, h: false },
            6: { a: false, b: false, c: false, d: false, e: false, f: false, g: false, h: false },
            7: { a: false, b: false, c: false, d: false, e: false, f: false, g: false, h: false },
            8: { a: false, b: false, c: false, d: false, e: false, f: false, g: false, h: false },
        }
    } 

    piece(piece: string, color: string): Piece { 
        return { 
            type: piece+'-'+color,
            isWhite: color === 'white' ? true : false,
            isDead: false,
            unmoved: true,
            moves: []
        }
    }

    getBoard() { 
        this.board = JSON.parse(localStorage.getItem('board')) ? JSON.parse(localStorage.getItem('board')) : this.resetBoard()
        return this.board
    }

    updateBoard(board: Board) { 
        this.board = board;
        localStorage.setItem('board', JSON.stringify(this.board))
    }
    
    resetBoard() { 
        this.resetMoves()
        this.board = {
            1: { 
                a: this.piece('rook', 'black'), 
                b: this.piece('knight', 'black'), 
                c: this.piece('bishop', 'black'), 
                d: this.piece('queen', 'black'), 
                e: this.piece('king', 'black'), 
                f: this.piece('bishop', 'black'), 
                g: this.piece('knight', 'black'), 
                h: this.piece('rook', 'black') 
            },
            2: { 
                a: this.piece('pawn', 'black'), 
                b: this.piece('pawn', 'black'), 
                c: this.piece('pawn', 'black'), 
                d: this.piece('pawn', 'black'), 
                e: this.piece('pawn', 'black'), 
                f: this.piece('pawn', 'black'), 
                g: this.piece('pawn', 'black'), 
                h: this.piece('pawn', 'black') 
            },
            3: { a: null, b: null, c: null, d: null, e: null, f: null, g: null, h: null },
            4: { a: null, b: null, c: null, d: null, e: null, f: null, g: null, h: null },
            5: { a: null, b: null, c: null, d: null, e: null, f: null, g: null, h: null },
            6: { a: null, b: null, c: null, d: null, e: null, f: null, g: null, h: null },
            7: { 
                a: this.piece('pawn', 'white'), 
                b: this.piece('pawn', 'white'), 
                c: this.piece('pawn', 'white'), 
                d: this.piece('pawn', 'white'), 
                e: this.piece('pawn', 'white'), 
                f: this.piece('pawn', 'white'), 
                g: this.piece('pawn', 'white'), 
                h: this.piece('pawn', 'white') 
            },
            8: { 
                a: this.piece('rook', 'white'), 
                b: this.piece('knight', 'white'), 
                c: this.piece('bishop', 'white'), 
                d: this.piece('queen', 'white'), 
                e: this.piece('king', 'white'), 
                f: this.piece('bishop', 'white'), 
                g: this.piece('knight', 'white'), 
                h: this.piece('rook', 'white')
            },
        };
        Object.keys(this.board['2']).map((key, val) => {
            // if (this.board['2'][key]) { 
            //     this.board['2'][key].moves = [
            //         {
            //             isKill: false,
            //             newPosition: ['3', key]
            //         },
            //         {
            //             isKill: false,
            //             newPosition: ['4', key]
            //         }
            //     ]
            // }
            if (this.board['7'][key]) { 
                this.board['7'][key].moves = [
                    {
                        isKill: false,
                        newPosition: ['6', key]
                    },
                    {
                        isKill: false,
                        newPosition: ['5', key]
                    }
                ]
            }
        })
        localStorage.setItem('board', JSON.stringify(this.board))
        return this.board
    }

    getSelectedPlayer() { 
        if (this.selectedPlayer) { 
            return this.selectedPlayer
        } else {
            if (localStorage.getItem('selectedPlayer')) {
                if (localStorage.getItem('selectedPlayer') === 'WHITE') {
                    return SelectedPlayer.WHITE
                } else {
                    return SelectedPlayer.BLACK
                }
            } else {    
                return SelectedPlayer.WHITE
            }
        }
    }

    updateSelectedPlayer(selectedPlayer: SelectedPlayer) { 
        localStorage.setItem('selectedPlayer', selectedPlayer)
        this.selectedPlayer = selectedPlayer;
        console.log('Current Player')
        console.log( this.selectedPlayer, localStorage.getItem('selectedPlayer'))
    }

    resetSelectedPlayer() { 
        this.selectedPlayer = SelectedPlayer.WHITE;
        localStorage.setItem('selectedPlayer', this.selectedPlayer)
        return this.selectedPlayer
    }

    findMoves(board: Board): Observable<any> | any { 
        console.log(this.selectedPlayer)
        if (this.selectedPlayer) { 
            const body = JSON.stringify({"board": board, "selectedPlayer": localStorage.getItem('selectedPlayer')}) 
            return this.http.post<any>(this.baseURL + '/findmoves', body)
        } else {
            return of({board: this.getBoard(), selectedPlayer: localStorage.getItem('selectedPlayer')})
        }
    }

    addMoves(move): any { 
        this.moves.unshift(move)
        localStorage.setItem('moves', JSON.stringify(this.moves))
    }

    getMoves(): Observable<any> { 
        this.moves = JSON.parse(localStorage.getItem('moves')) ? JSON.parse(localStorage.getItem('moves')) : []
        return of(this.moves)
    }

    reverseMove(): Observable<any> {
        const reversedMove: any = this.moves.shift();
        localStorage.setItem('moves', JSON.stringify(this.moves))

        if (reversedMove) { 
            this.board[this.correctRow(reversedMove.start[0])][reversedMove.start[1]] = this.board[this.correctRow(reversedMove.end[0])][reversedMove.end[1]]
            if (reversedMove.kill) { 
                this.board[this.correctRow(reversedMove.end[0])][reversedMove.end[1]] = reversedMove.kill
            } else { 
                this.board[this.correctRow(reversedMove.end[0])][reversedMove.end[1]] = null
            }
            if (reversedMove.castle) {
                this.board[this.correctRow(reversedMove.castle.rookStartPosition[0])][reversedMove.castle.rookStartPosition[1]] = this.board[this.correctRow(reversedMove.castle.rookEndPosition[0])][reversedMove.castle.rookEndPosition[1]]
            }
            localStorage.setItem('board', JSON.stringify(this.board))

            // if (this.selectedPlayer === SelectedPlayer.WHITE) {
            //     this.selectedPlayer = SelectedPlayer.BLACK
            // } else {
            //     this.selectedPlayer = SelectedPlayer.WHITE
            // }
            // localStorage.setItem('selectedPlayer', this.selectedPlayer)
            // console.log('test')
            this.findMoves(this.board).subscribe((data) => {
                this.updateSelectedPlayer(data.selectedPlayer)
                this.updateBoard(data.board)
            })

            return of(this.moves)
        }
 
        return of(null)
    }

    resetMoves() { 
        this.moves = []
        localStorage.setItem('moves', JSON.stringify(this.moves))
    }

    // actual coordinates for chess is a mirror image of what I had before
    correctRow(row: number) { 
        const a = {
            1: 8,
            2: 7,
            3: 6,
            4: 5,
            5: 4,
            6: 3,
            7: 2,
            8: 1
        }
        return a[row]
    }
}