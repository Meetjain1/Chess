import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

import { Board, BoardCircle, BoardColor } from 'src/app/core/models/board.interface';
import { CoreService } from 'src/app/core/core.service';
import { SelectedPlayer } from '../../enums/selected-player';

@Component({
  selector: 'app-board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.scss']
})
export class BoardComponent implements OnInit {
  @Input() board: Board;

  @Output() updateMoves = new EventEmitter();

  showCircle = false;
  startingPosition: string[];
  boardColor: BoardColor;
  boardCircle: BoardCircle;
  loading: boolean = false;
  errorMessage;
  nextPlayer: SelectedPlayer;

  move;

  constructor(
    private coreService: CoreService
  ) { }

  ngOnInit(): void {
    this.boardColor = this.coreService.boardColor
    this.boardCircle = this.coreService.boardEmptyCircle()
    this.getData();
  }

  getData() { 
    this.loading = true;
    this.errorMessage = "";
    this.coreService.findMoves(this.board)
      .subscribe((res) => {
        this.board = res.board
        this.nextPlayer = res.selectedPlayer
        this.coreService.updateSelectedPlayer(this.nextPlayer);
        this.coreService.updateBoard(this.board)
        console.log('Current Player')
        console.log(localStorage.getItem('selectedPlayer'))
      }, (error) => { 
        console.log(error)
        this.errorMessage = error;
        this.loading = false;
      }, () => { 
        this.loading = false; 
      })
  }

  findMovesOrMovePiece(row: string, col: string) {
    if (!this.loading) { 
      if (!this.showCircle) { 
        this.boardCircle = this.coreService.boardEmptyCircle()
        let moves = this.board[row][col]?.moves
        if (moves) { 
          moves?.map((move) => { 
            if (move) { 
              let position = move.newPosition
              this.boardCircle[position[0]][position[1]] = true 
            }
          })
          this.startingPosition = [row, col]
          this.showCircle = true
        }
      } else { 
        if (!this.boardCircle[row][col]) { 
          this.boardCircle = this.coreService.boardEmptyCircle()
          this.startingPosition = []
          this.showCircle = false
        } else { 
          this.movePiece(row, col)
        }
      }
    }
  }

  movePiece(row: string, col: string) { 
    let movingPiece = this.board[this.startingPosition[0]][this.startingPosition[1]]
    movingPiece.unmoved = false;
    let destPiece = this.board[row][col]
    let move = movingPiece.moves.filter((move) => { 
      return (move && move.newPosition[0] === row && move.newPosition[1] === col)
    })[0]

    // check if move is castle or en passant
    if (move.castle) { 
      let rook = this.board[move.castle.rookStartPosition[0]][move.castle.rookStartPosition[1]]
      this.board[move.castle.rookEndPosition[0]][move.castle.rookEndPosition[1]] = rook
      this.board[move.castle.rookStartPosition[0]][move.castle.rookStartPosition[1]] = null
    } else if (move.enPassant) { 
      this.board[move.enPassant.killPosition[0]][move.enPassant.killPosition[1]] = null
    }

    // add move to move list
    this.move = { 
      start: [this.correctRow(this.startingPosition[0]), this.startingPosition[1]], 
      end: [this.correctRow(row), col],
      piece: movingPiece,
      castle: move.castle,
      kill: destPiece
    }
    this.coreService.addMoves(this.move)
    this.updateMoves.emit(this.move);

    // update board
    this.board[this.startingPosition[0]][this.startingPosition[1]] = null
    this.board[row][col] = movingPiece
    this.boardCircle = this.coreService.boardEmptyCircle()
    this.startingPosition = []
    this.showCircle = false
    this.coreService.updateBoard(this.board)
    this.getData()
  }

  urlConcat(pieceType: string): string { 
    return 'assets/'+pieceType+'.png'
  }

  correctRow(row) {
    return this.coreService.correctRow(row)
  }

  reverseMove() { 
    if (!this.loading) { 
      this.coreService.reverseMove().subscribe((res) => {
        if (res) { 
          this.getData()
          this.updateMoves.emit(this.move);
        }
      })
    }
  }
}
