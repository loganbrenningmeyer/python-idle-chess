# Python IDLE Chess

PvP Chess on Python IDLE. All the features of traditional chess except en passant. Can save/load games or overwrite current save.

NOTICE: This program only works properly when running on Python IDLE, preferrably in dark mode. 
Otherwise, the text for the pieces cannot be colored according to default IDLE colors and 
understanding the board is much harder.

Features:
  - Random white/black selection
  - Capturing
  - Check/Checkmate
  - Stalemate/Draw
  - Castling
  - Save/Load games
    * Stores file with name "Player1Player2.chs" in Chess.py folder
    * Select LOAD GAME and input proper Player 1 Name/Player 2 Name
      - Two players can have two concurrent games (Player1Player2.chs & Player2Player1.chs)

  - No En Passant


Game Layout:
```
                      ╔═══════╗
══════════════════════╣ CHESS ╠═════════════════════
                      ╚═══════╝

1) PLAYER VS PLAYER
2) LOAD GAME

What would you like to do? 1

Player 1 Name: Logan
Player 2 Name: GitHub

Logan is White, GitHub is Black

                  ╔═══════════════╗
══════════════════╣ WHITE TO MOVE ╠═════════════════
                  ╚═══════════════╝

Black Captures: 

    A     B     C     D     E     F     G     H

  ‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗
  █▀▀▀▀█      █▀▀▀▀█      █▀▀▀▀█      █▀▀▀▀█     ║
8 █ BR █  BN  █ BB █  BQ  █ BK █  Bb  █ Bn █  Br ║ 8
  █▄▄▄▄█      █▄▄▄▄█      █▄▄▄▄█      █▄▄▄▄█     ║
  ║     █▀▀▀▀█      █▀▀▀▀█      █▀▀▀▀█      █▀▀▀▀█
7 ║ B8  █ B7 █  B6  █ B5 █  B4  █ B3 █  B2  █ B1 █ 7
  ║     █▄▄▄▄█      █▄▄▄▄█      █▄▄▄▄█      █▄▄▄▄█
  ██████      ██████      ██████      ██████     ║
6 ██████      ██████      ██████      ██████     ║ 6
  ██████      ██████      ██████      ██████     ║
  ║     ██████      ██████      ██████      ██████
5 ║     ██████      ██████      ██████      ██████ 5
  ║     ██████      ██████      ██████      ██████
  ██████      ██████      ██████      ██████     ║
4 ██████      ██████      ██████      ██████     ║ 4
  ██████      ██████      ██████      ██████     ║
  ║     ██████      ██████      ██████      ██████
3 ║     ██████      ██████      ██████      ██████ 3
  ║     ██████      ██████      ██████      ██████
  █▀▀▀▀█      █▀▀▀▀█      █▀▀▀▀█      █▀▀▀▀█     ║
2 █ W1 █  W2  █ W3 █  W4  █ W5 █  W6  █ W7 █  W8 ║ 2
  █▄▄▄▄█      █▄▄▄▄█      █▄▄▄▄█      █▄▄▄▄█     ║
  ║     █▀▀▀▀█      █▀▀▀▀█      █▀▀▀▀█      █▀▀▀▀█
1 ║ Wr  █ Wn █  Wb  █ WQ █  WK  █ WB █  WN  █ WR █ 1
  ║‗‗‗‗‗█▄▄▄▄█‗‗‗‗‗‗█▄▄▄▄█‗‗‗‗‗‗█▄▄▄▄█‗‗‗‗‗‗█▄▄▄▄█

    A     B     C     D     E     F     G     H

White Captures: 

Input move (PiecePosition e.g. W5E4): 
```


Checkmate:
```
                      ╔═══════╗
══════════════════════╣ CHECK ╠═════════════════════
                      ╚═══════╝

                   ╔═════════════╗
╔══════════════════╣ WHITE WINS! ╠═════════════════╗
║                  ╚═════════════╝                 ║
║                                                  ║
║                   ╔═══════════╗                  ║
╚═══════════════════╣ CHECKMATE ╠══════════════════╝
                    ╚═══════════╝

Black Captures: 

    A     B     C     D     E     F     G     H

  ‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗
  █▀▀▀▀█      █▀▀▀▀█      █▀▀▀▀█      █▀▀▀▀█     ║
8 █ BR █  BN  █ BB █  BQ  █ BK █  Bb  █ Bn █  Br ║ 8
  █▄▄▄▄█      █▄▄▄▄█      █▄▄▄▄█      █▄▄▄▄█     ║
  ║     █▀▀▀▀█      █▀▀▀▀█      ██████      █▀▀▀▀█
7 ║ B8  █ B7 █  B6  █ B5 █  B4  ██████      █ B1 █ 7
  ║     █▄▄▄▄█      █▄▄▄▄█      ██████      █▄▄▄▄█
  ██████      ██████      ██████      ██████     ║
6 ██████      ██████      ██████  B3  ██████     ║ 6
  ██████      ██████      ██████      ██████     ║
  ║     ██████      ██████      ██████      █▀▀▀▀█
5 ║     ██████      ██████      ██████  B2  █ WQ █ 5
  ║     ██████      ██████      ██████      █▄▄▄▄█
  ██████      ██████      █▀▀▀▀█      ██████     ║
4 ██████      ██████      █ W5 █      ██████     ║ 4
  ██████      ██████      █▄▄▄▄█      ██████     ║
  ║     ██████      ██████      ██████      ██████
3 ║     ██████  Wn  ██████      ██████      ██████ 3
  ║     ██████      ██████      ██████      ██████
  █▀▀▀▀█      █▀▀▀▀█      ██████      █▀▀▀▀█     ║
2 █ W1 █  W2  █ W3 █  W4  ██████  W6  █ W7 █  W8 ║ 2
  █▄▄▄▄█      █▄▄▄▄█      ██████      █▄▄▄▄█     ║
  ║     ██████      ██████      █▀▀▀▀█      █▀▀▀▀█
1 ║ Wr  ██████  Wb  ██████  WK  █ WB █  WN  █ WR █ 1
  ║‗‗‗‗‗██████‗‗‗‗‗‗██████‗‗‗‗‗‗█▄▄▄▄█‗‗‗‗‗‗█▄▄▄▄█

    A     B     C     D     E     F     G     H

White Captures: 

Would you like to play again? (y/n): 
```
