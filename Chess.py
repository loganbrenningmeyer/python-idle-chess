#Plays normal chess with the exception of en passant
#Can only make legal moves, win by checkmate or draw by stalemate/insufficient mating material
#Can save and load games to continue where you left off
#Type PiecePosition to move (to move the white pawn W5 to E4, type W5E4)

import random, copy, sys

import tkinter
from tkinter import messagebox

check = ["  ","  "]

WK_moves = [0]
BK_moves = [0]
Wr_moves = [0]
WR_moves = [0]
Br_moves = [0]
BR_moves = [0]

#Allows coloring the pieces on the board in IDLE using default IDLE font colors
try:
    color = sys.stdout.shell
except AttributeError:
    # This code is to hide the main tkinter window
    root = tkinter.Tk()
    root.withdraw()
    # Message Box
    messagebox.showinfo("Use IDLE", "The game doesn't work properly outside of Python IDLE, use IDLE instead")
    raise RuntimeError("Use IDLE")

white_captures = []
black_captures = []

#Converts list of captured pieces into an ordered list of unicode chess pieces
def make_pieces(captures):
    pawns = []
    knights = []
    bishops = []
    rooks = []
    queens = []
    
    captures_return = []
    
    for i in captures:
        #PAWNS
        if i.upper() in ["W1","W2","W3","W4","W5","W6","W7","W8","B1","B2","B3","B4","B5","B6","B7","B8"]:
            if i.upper()[0] == "W":
                pawns.append("\u2659")
            else:
                pawns.append("\u265F")
        #KNIGHTS
        elif i in ["WN","Wn","BN","Bn"]:
            if i[0] == "W":
                knights.append("\u2658")
            else:
                knights.append("\u265E")
                
        #BISHOPS
        elif i in ["WB","Wb","BB","Bb"]:
            if i[0] == "W":
                bishops.append("\u2657")
            else:
                bishops.append("\u265D") 
        #ROOKS
        elif i in ["WR","Wr","BR","Br"]:
            if i[0] == "W":
                rooks.append("\u2656")
            else:
                rooks.append("\u265C")   
        #QUEENS
        elif i in ["WQ","BQ"]:
            if i[0] == "W":
                queens.append("\u2655")
            else:
                queens.append("\u265B")

    captures_return.append("".join(pawns))
    captures_return.append("".join(knights))
    captures_return.append("".join(bishops))
    captures_return.append("".join(rooks))
    captures_return.append("".join(queens))

    return captures_return

def main(white_captures, black_captures):
    
    print("\n             IDLE Dark Theme Recommended")

    #init()
    
    while(True):
        print("\n                      ╔═══════╗")
        print  ("══════════════════════╣ CHESS ╠═════════════════════")
        print  ("                      ╚═══════╝")        
        
        print("\n1) PLAYER VS PLAYER")
        print("2) LOAD GAME")

        try:
            choice = int(input("\nWhat would you like to do? "))
            if(choice != 1 and choice != 2):
                print("\nPlease input 1 or 2")
                continue
        except:
            print("\nPlease input 1 or 2")
            continue

        if(choice == 1):    

            gamestate = [["BR","BN","BB","BQ","BK","Bb","Bn","Br"],
                         ["B8","B7","B6","B5","B4","B3","B2","B1"],
                         ["  ","  ","  ","  ","  ","  ","  ","  "],
                         ["  ","  ","  ","  ","  ","  ","  ","  "],
                         ["  ","  ","  ","  ","  ","  ","  ","  "],
                         ["  ","  ","  ","  ","  ","  ","  ","  "],
                         ["W1","W2","W3","W4","W5","W6","W7","W8"],
                         ["Wr","Wn","Wb","WQ","WK","WB","WN","WR"]]
            
            player1 = input("\nPlayer 1 Name: ")
            player2 = input("Player 2 Name: ")
            
            white_captures = []
            black_captures = []
            
            pvp(player1, player2, gamestate, white_captures, black_captures,"White","None","None")

            replay = input("\nWould you like to play again? (y/n): ")

            if(replay.upper() != "Y"):
                break
            else:
                continue
            
        if(choice == 2):

            gamestate = [["BR","BN","BB","BQ","BK","Bb","Bn","Br"],
                         ["B8","B7","B6","B5","B4","B3","B2","B1"],
                         ["  ","  ","  ","  ","  ","  ","  ","  "],
                         ["  ","  ","  ","  ","  ","  ","  ","  "],
                         ["  ","  ","  ","  ","  ","  ","  ","  "],
                         ["  ","  ","  ","  ","  ","  ","  ","  "],
                         ["W1","W2","W3","W4","W5","W6","W7","W8"],
                         ["Wr","Wn","Wb","WQ","WK","WB","WN","WR"]]
            
            player1 = input("\nPlayer 1 Name: ")
            player2 = input("Player 2 Name: ")

            try:
            
                f = open(f"{player1+player2}.chs","r")

                f.seek(0)

                #For each row in the file
                for i in range(8):
                    #Create list of each horizontal row
                    line = f.readline()
                    line = line.split(",")
                    #Get rid of "\n"
                    del line[8]

                    for j in range(8):
                        gamestate[i][j] = line[j]

                white_captures = f.readline()
                white_captures = white_captures.split(",")
                del white_captures[len(white_captures)-1]

                if(white_captures[0] == ''):
                    del white_captures[0]
                    
                black_captures = f.readline()

                black_captures = black_captures.split(",")

                del black_captures[len(black_captures)-1]

                if(black_captures[0] == ''):
                    del black_captures[0]
                    
                color_to_move = f.readline().strip()

                p1_color = f.readline().strip()

                p2_color = f.readline().strip()

                f.close()


                pvp(player1,player2,gamestate,white_captures,black_captures,color_to_move,p1_color,p2_color)

                replay = input("\nWould you like to play again? (y/n): ")

                if(replay.upper() != "Y"):
                    break
                else:
                    continue

            except Exception as e:
                print("\nGame cannot be found.")
                continue

#Fills upper and lower halves of white squares depending on if they're occupied
def fill_block(piece, tb):
    if piece[0].upper() != "W" and piece[0].upper() != "B":
        return "████"
    else:
        if(tb == 1):
            return "▀▀▀▀"
        else:
            return "▄▄▄▄"

def print_board(gamestate):

    #Basically constructs blocks based on if they're white or empty and what's after it

    print("\n    A     B     C     D     E     F     G     H\n")

    vertical = 1
    
    for i in range(8,0,-1):

        blank = [0,0,0,0]

        if(vertical == 1):
            print(f"  ‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗")

            print(f"  █{fill_block(gamestate[0][0],1)}█      █{fill_block(gamestate[0][2],1)}█      █{fill_block(gamestate[0][4],1)}█      █{fill_block(gamestate[0][6],1)}█     ║")
        elif(vertical % 2 != 0):
            print(f"  █{fill_block(gamestate[vertical-1][0],1)}█      █{fill_block(gamestate[vertical-1][2],1)}█      █{fill_block(gamestate[vertical-1][4],1)}█      █{fill_block(gamestate[vertical-1][6],1)}█     ║")
        else:
            print(f"  ║     █{fill_block(gamestate[vertical-1][1],1)}█      █{fill_block(gamestate[vertical-1][3],1)}█      █{fill_block(gamestate[vertical-1][5],1)}█      █{fill_block(gamestate[vertical-1][7],1)}█")
        
        horizontal = 1

        if(vertical % 2 != 0):
            if(gamestate[vertical-1][horizontal-1] == "  "):
                print(f"{i} ██", end = "")
            else:
                print(f"{i} █ ", end = "")
        else:
            print(f"{i} ║ ", end = "")
            
        for j in range(0,7):
            if(gamestate[8-i][j][0].upper() == "B"):
                color.write(gamestate[8-i][j], "DEFINITION")
            elif(gamestate[8-i][j][0].upper() == "W"):
                color.write(gamestate[8-i][j])
            elif((vertical % 2 != 0 and horizontal % 2 != 0) or (vertical % 2 == 0 and horizontal % 2 == 0)):
                print("██", end ="")
            else:
                print("  ", end = "")
                
            if(vertical % 2 != 0):
                if(horizontal % 2 == 0):
                    if(gamestate[vertical-1][horizontal] == "  "):
                            print("  ██", end = "")
                    else:
                        print("  █ ", end = "")
                else:
                    if(gamestate[vertical-1][horizontal] == "  "):
                        if(gamestate[vertical-1][horizontal-1] == "  "):
                            print("██  ", end = "")
                        else:
                            print(" █  ", end = "")
                    else:
                        if(gamestate[vertical-1][horizontal-1] == "  "):
                            print("██  ", end = "")
                        else:
                            print(" █  ", end = "")
            else:
                if(horizontal % 2 == 0):
                    if(gamestate[vertical-1][horizontal-1] == "  "):
                        print("██  ", end = "")
                    else:
                        print(" █  ", end = "")
                else:
                    if(gamestate[vertical-1][horizontal] == "  "):
                        print("  ██", end = "")
                    else:
                        print("  █ ", end = "")

            horizontal += 1
            
        if(gamestate[8-i][7][0].upper() == "B"):
            color.write(gamestate[8-i][7], "DEFINITION")
        elif(gamestate[8-i][7][0].upper() == "W"):
            color.write(gamestate[8-i][7])
        elif((vertical % 2 != 0 and horizontal % 2 != 0) or (vertical % 2 == 0 and horizontal % 2 == 0)):
            print("██", end ="")
        else:
            print("  ", end = "")

        if(vertical % 2 == 0):
            if(gamestate[vertical-1][horizontal-1] == "  "):
                print(f"██ {i}")
            else:
                print(f" █ {i}")
        else:
            print(f" ║ {i}")

        if(vertical == 8):
            print(f"  ║‗‗‗‗‗█{fill_block(gamestate[7][1],0)}█‗‗‗‗‗‗█{fill_block(gamestate[7][3],0)}█‗‗‗‗‗‗█{fill_block(gamestate[7][5],0)}█‗‗‗‗‗‗█{fill_block(gamestate[7][7],0)}█")
        elif(vertical % 2 != 0):
            print(f"  █{fill_block(gamestate[vertical-1][0],0)}█      █{fill_block(gamestate[vertical-1][2],0)}█      █{fill_block(gamestate[vertical-1][4],0)}█      █{fill_block(gamestate[vertical-1][6],0)}█     ║")
        else:
            print(f"  ║     █{fill_block(gamestate[vertical-1][1],0)}█      █{fill_block(gamestate[vertical-1][3],0)}█      █{fill_block(gamestate[vertical-1][5],0)}█      █{fill_block(gamestate[vertical-1][7],0)}█")

        vertical += 1

    print("\n    A     B     C     D     E     F     G     H")

def pvp(player1, player2, gamestate, white_captures, black_captures, color_to_move, p1_color, p2_color):

    gamestate_check = copy.deepcopy(gamestate)
    
    color = random.randint(0,1)

    first_move = 1

    if(p1_color == "None" and p2_color == "None"):
        if(color == 0):
            p1_color = "Black"
            p2_color = "White"
        else:
            p1_color = "White"
            p2_color = "Black"

    print(f"\n{player1} is {p1_color}, {player2} is {p2_color}")

    while(True):
        
        if(color_to_move == "White" or color_to_move == "Clear"):

            check = ["  ","  "]

            if(color_to_move == "White"):
                if (ischeck(gamestate_check, check)[0] == "White"):                    
                    print("\n                      ╔═══════╗")
                    print  ("══════════════════════╣ CHECK ╠═════════════════════")
                    print  ("                      ╚═══════╝")

                    check = ischeck(gamestate_check, check)

                    if(notcheckmate("White",gamestate,gamestate_check) != True):
                        print("\n                   ╔═════════════╗")
                        print  ("╔══════════════════╣ BLACK WINS! ╠═════════════════╗")
                        print  ("║                  ╚═════════════╝                 ║")
                        print  ("║                                                  ║")
                        print  ("║                   ╔═══════════╗                  ║")
                        print  ("╚═══════════════════╣ CHECKMATE ╠══════════════════╝")
                        print  ("                    ╚═══════════╝")
                        
                        print(f"\nBlack Captures: {''.join(make_pieces(black_captures))}")

                        print_board(gamestate)

                        print(f"\nWhite Captures: {''.join(make_pieces(white_captures))}")
                        return

            print("\n                  ╔═══════════════╗")
            print  ("══════════════════╣ WHITE TO MOVE ╠═════════════════")
            print  ("                  ╚═══════════════╝")

            print(f"\nBlack Captures: {''.join(make_pieces(black_captures))}")
    
            print_board(gamestate)

            print(f"\nWhite Captures: {''.join(make_pieces(white_captures))}")

            while(True):

                if(first_move == 1):      
                    move = input("\nInput move (PiecePosition e.g. W5E4): ")
                else:
                    move = input("\nInput move (PiecePosition)[x to save]: ")

                first_move = 0
                #Save game
                if(move.upper() == "X"):
                    f = open(f"{player1+player2}.chs","w")

                    f.seek(0)
                    
                    for i in gamestate:
                        for j in i:
                            f.write(j+",")
                        f.write("\n")

                    f.write(",".join(white_captures)+",\n")
                    f.write(",".join(black_captures)+",\n")

                    f.write("White\n")

                    f.write(p1_color+"\n")

                    f.write(p2_color+"\n")

                    f.close()

                    return

                try:
                    if(islegal("White",move,gamestate,gamestate_check,False,True, white_captures, black_captures)):
                        
                        piece = move[0:2]
                        position = move[2:4]
                        letter = position[:1]
                        
                        if(letter == "A"):
                            position = str((8-int(position[1]))) + "0"
                        elif(letter == "B"):
                            position = str((8-int(position[1]))) + "1"
                        elif(letter == "C"):
                            position = str((8-int(position[1]))) + "2"
                        elif(letter == "D"):
                            position = str((8-int(position[1]))) + "3"
                        elif(letter == "E"):
                            position = str((8-int(position[1]))) + "4"
                        elif(letter == "F"):
                            position = str((8-int(position[1]))) + "5"
                        elif(letter == "G"):
                            position = str((8-int(position[1]))) + "6"
                        elif(letter == "H"):
                            position = str((8-int(position[1]))) + "7"

                        for i in gamestate_check:
                            if piece in i:
                                original_position = str(gamestate_check.index(i))+str(i.index(piece))
                                
                        gamestate_check[int(original_position[0])][int(original_position[1])] = "  "
                        gamestate_check[int(position[0])][int(position[1])] = piece

                        check = ischeck(gamestate_check, check)

                        if(check[1] == "Black" and check[0] != "White"):
                            print("\n                      ╔═══════╗")
                            print  ("══════════════════════╣ CHECK ╠═════════════════════")
                            print  ("                      ╚═══════╝")
    
                            gamestate = copy.deepcopy(gamestate_check)
                            if(notcheckmate("Black",gamestate,gamestate_check) != True):
                                print("\n                   ╔═════════════╗")
                                print  ("╔══════════════════╣ WHITE WINS! ╠═════════════════╗")
                                print  ("║                  ╚═════════════╝                 ║")
                                print  ("║                                                  ║")
                                print  ("║                   ╔═══════════╗                  ║")
                                print  ("╚═══════════════════╣ CHECKMATE ╠══════════════════╝")
                                print  ("                    ╚═══════════╝")

                                print(f"\nBlack Captures: {''.join(make_pieces(black_captures))}")

                                print_board(gamestate)

                                print(f"\nWhite Captures: {''.join(make_pieces(white_captures))}")
                                
                                return

                        #If a white pawn moves to the end of the board
                        if piece in ["W1","W2","W3","W4","W5","W6","W7","W8"] and int(position[0]) == 0:
                            print("\n                  ╔═══════════════╗")
                            print  ("══════════════════╣ PAWN PROMOTED ╠═════════════════")
                            print  ("                  ╚═══════════════╝")
                            gamestate_check[int(position[0])][int(position[1])] = "w" + piece[1]

                        

                        #DRAW BY INSUFFICIENT MATERIAL
                        white_pieces = []
                        black_pieces = []
                        
                        for i in gamestate_check:
                            for j in i:
                                if j[0].upper() == "W":
                                    white_pieces.append(j)
                                elif j[0].upper() == "B":
                                    black_pieces.append(j)

                        #If white has only two pieces (King + knight/bishop) or just a king and black has only two pieces (King + knight/bishop) or just a king
                        if((len(white_pieces) == 2 and "WK" in white_pieces and ("WB" in white_pieces or "Wb" in white_pieces or "WN" in white_pieces or "Wn" in white_pieces)) or
                            len(white_pieces) == 1 and "WK" in white_pieces):
                            if((len(black_pieces) == 2 and "BK" in black_pieces and ("BB" in black_pieces or "Bb" in black_pieces or "BN" in black_pieces or "Bn" in black_pieces)) or
                                len(black_pieces) == 1 and "BK" in black_pieces):
                                print("\n                   ╔═════════════╗")
                                print  ("╔══════════════════╣ IT'S A DRAW ╠═════════════════╗")
                                print  ("║                  ╚═════════════╝                 ║")
                                print  ("║                                                  ║")
                                print  ("║             ╔═══════════════════════╗            ║")
                                print  ("╚═════════════╣ INSUFFICIENT MATERIAL ╠════════════╝")
                                print  ("              ╚═══════════════════════╝")

                                print(f"\nBlack Captures: {''.join(make_pieces(black_captures))}")

                                print_board(gamestate_check)

                                print(f"\nWhite Captures: {''.join(make_pieces(white_captures))}")
                                
                                return
                                
                        #STALEMATE
                        #If black has no legal moves but no one is in check
                        if(notcheckmate("Black",gamestate,gamestate_check) != True and check[0] != "White" and check[1] != "Black"):
                            print("\n                   ╔═════════════╗")
                            print  ("╔══════════════════╣ IT'S A DRAW ╠═════════════════╗")
                            print  ("║                  ╚═════════════╝                 ║")
                            print  ("║                                                  ║")
                            print  ("║                   ╔═══════════╗                  ║")
                            print  ("╚═══════════════════╣ STALEMATE ╠══════════════════╝")
                            print  ("                    ╚═══════════╝")

                            print(f"\nBlack Captures: {''.join(make_pieces(black_captures))}")

                            print_board(gamestate_check)

                            print(f"\nWhite Captures: {''.join(make_pieces(white_captures))}")
                            
                            return
                        
                            color_to_move = "Clear"
                            break
                        elif(check[0] == "White"):
                            print("\nYou can't put yourself in check, try again")
                            #If white legally captures something but puts itself in check
                            if(gamestate[int(position[0])][int(position[1])] != "  " and gamestate[int(position[0])][int(position[1])] == white_captures[len(white_captures)-1]):
                                del white_captures[len(white_captures)-1]
                                
                            gamestate_check = copy.deepcopy(gamestate)
                            continue
                        
                        gamestate = copy.deepcopy(gamestate_check)
                        
                    else:
                        print("\nThat move isn't legal, try again")
                        gamestate_check = copy.deepcopy(gamestate)
                        continue
                except Exception as e:
                    print("\nThat move isn't legal, try again")
                    gamestate_check = copy.deepcopy(gamestate)
                    continue

                color_to_move = "Clear"
                    
                break

        if(color_to_move == "Black" or color_to_move == "Clear"):

            check = ["  ","  "]

            if(color_to_move == "Black"):
                if ischeck(gamestate_check, check)[1] == "Black":
                    print("\n                      ╔═══════╗")
                    print  ("══════════════════════╣ CHECK ╠═════════════════════")
                    print  ("                      ╚═══════╝")

                    if(notcheckmate("Black",gamestate,gamestate_check) != True):
                        print("\n                   ╔═════════════╗")
                        print  ("╔══════════════════╣ WHITE WINS! ╠═════════════════╗")
                        print  ("║                  ╚═════════════╝                 ║")
                        print  ("║                                                  ║")
                        print  ("║                   ╔═══════════╗                  ║")
                        print  ("╚═══════════════════╣ CHECKMATE ╠══════════════════╝")
                        print  ("                    ╚═══════════╝")

                        print(f"\nBlack Captures: {''.join(make_pieces(black_captures))}")

                        print_board(gamestate)

                        print(f"\nWhite Captures: {''.join(make_pieces(white_captures))}")
                        
                        return

            print("\n                  ╔═══════════════╗")
            print  ("══════════════════╣ BLACK TO MOVE ╠═════════════════")
            print  ("                  ╚═══════════════╝")

            print(f"\nBlack Captures: {''.join(make_pieces(black_captures))}")

            print_board(gamestate)

            print(f"\nWhite Captures: {''.join(make_pieces(white_captures))}")

            while(True):
                
                if(first_move == 1):      
                    move = input("\nInput move (PiecePosition e.g. B4E5): ")
                else:
                    move = input("\nInput move (PiecePosition)[x to save]: ")

                first_move = 0
                #Save game
                if(move.upper() == "X"):
                    f = open(f"{player1+player2}.chs","w")

                    f.seek(0)
                    
                    for i in gamestate:
                        for j in i:
                            f.write(j+",")
                        f.write("\n")

                    f.write(",".join(white_captures)+",\n")
                    f.write(",".join(black_captures)+",\n")

                    f.write("Black\n")

                    f.write(p1_color+"\n")

                    f.write(p2_color+"\n")

                    f.close()

                    return
                    
                try:
                    if(islegal("Black",move,gamestate,gamestate_check,False,True, white_captures, black_captures)):

                        
                        piece = move[0:2]
                        position = move[2:4]
                        letter = position[:1]
                        
                        if(letter == "A"):
                            position = str((8-int(position[1]))) + "0"
                        elif(letter == "B"):
                            position = str((8-int(position[1]))) + "1"
                        elif(letter == "C"):
                            position = str((8-int(position[1]))) + "2"
                        elif(letter == "D"):
                            position = str((8-int(position[1]))) + "3"
                        elif(letter == "E"):
                            position = str((8-int(position[1]))) + "4"
                        elif(letter == "F"):
                            position = str((8-int(position[1]))) + "5"
                        elif(letter == "G"):
                            position = str((8-int(position[1]))) + "6"
                        elif(letter == "H"):
                            position = str((8-int(position[1]))) + "7"

                        for i in gamestate_check:
                            if piece in i:
                                original_position = str(gamestate_check.index(i))+str(i.index(piece))
                                
                        gamestate_check[int(original_position[0])][int(original_position[1])] = "  "
                        gamestate_check[int(position[0])][int(position[1])] = piece

                        if piece in ["B1","B2","B3","B4","B5","B6","B7","B8"] and int(position[0]) == 7:
                            print("\n                  ╔═══════════════╗")
                            print  ("══════════════════╣ PAWN PROMOTED ╠═════════════════")
                            print  ("                  ╚═══════════════╝")
                            gamestate_check[int(position[0])][int(position[1])] = "b" + piece[1]

                        check = ischeck(gamestate_check, check)

                        if(check[0] == "White" and check[1] != "Black"):
                            print("\n                      ╔═══════╗")
                            print  ("══════════════════════╣ CHECK ╠═════════════════════")
                            print  ("                      ╚═══════╝")

                            gamestate = copy.deepcopy(gamestate_check)


                            if(notcheckmate("White",gamestate,gamestate_check) != True):
                                print("\n                   ╔═════════════╗")
                                print  ("╔══════════════════╣ BLACK WINS! ╠═════════════════╗")
                                print  ("║                  ╚═════════════╝                 ║")
                                print  ("║                                                  ║")
                                print  ("║                   ╔═══════════╗                  ║")
                                print  ("╚═══════════════════╣ CHECKMATE ╠══════════════════╝")
                                print  ("                    ╚═══════════╝")
                                
                                print(f"\nBlack Captures: {''.join(make_pieces(black_captures))}")

                                print_board(gamestate)

                                print(f"\nWhite Captures: {''.join(make_pieces(white_captures))}")
                                return

                        #DRAW BY INSUFFICIENT MATERIAL
                        white_pieces = []
                        black_pieces = []
                        
                        for i in gamestate_check:
                            for j in i:
                                if j[0].upper() == "W":
                                    white_pieces.append(j)
                                elif j[0].upper() == "B":
                                    black_pieces.append(j)
                                    
                        #If white has only two pieces (King + knight/bishop) or just a king and black has only two pieces (King + knight/bishop) or just a king
                        if((len(white_pieces) == 2 and "WK" in white_pieces and ("WB" in white_pieces or "Wb" in white_pieces or "WN" in white_pieces or "Wn" in white_pieces)) or
                            len(white_pieces) == 1 and "WK" in white_pieces):
                            if((len(black_pieces) == 2 and "BK" in black_pieces and ("BB" in black_pieces or "Bb" in black_pieces or "BN" in black_pieces or "Bn" in black_pieces)) or
                                len(black_pieces) == 1 and "BK" in black_pieces):
                                print("\n                   ╔═════════════╗")
                                print  ("╔══════════════════╣ IT'S A DRAW ╠═════════════════╗")
                                print  ("║                  ╚═════════════╝                 ║")
                                print  ("║                                                  ║")
                                print  ("║             ╔═══════════════════════╗            ║")
                                print  ("╚═════════════╣ INSUFFICIENT MATERIAL ╠════════════╝")
                                print  ("              ╚═══════════════════════╝")

                                print(f"\nBlack Captures: {''.join(make_pieces(black_captures))}")

                                print_board(gamestate_check)

                                print(f"\nWhite Captures: {''.join(make_pieces(white_captures))}")
                                
                                return

                        #STALEMATE
                        #If white has no legal moves and no one is in check
                        if(notcheckmate("White",gamestate,gamestate_check) != True and check[0] != "White" and check[1] != "Black"):
                            print("\n                   ╔═════════════╗")
                            print  ("╔══════════════════╣ IT'S A DRAW ╠═════════════════╗")
                            print  ("║                  ╚═════════════╝                 ║")
                            print  ("║                                                  ║")
                            print  ("║                   ╔═══════════╗                  ║")
                            print  ("╚═══════════════════╣ STALEMATE ╠══════════════════╝")
                            print  ("                    ╚═══════════╝")

                            print(f"\nBlack Captures: {''.join(make_pieces(black_captures))}")

                            print_board(gamestate_check)

                            print(f"\nWhite Captures: {''.join(make_pieces(white_captures))}")
                            
                            return

                            color_to_move = "Clear"
                            break
                        elif(check[1] == "Black"):
                            print("\nYou can't put yourself in check, try again")
                            #If the new position pre-move isn't blank and is blacks most recent capturesture
                            #Meaning black legally captured the piece but put itself in check
                            if(gamestate[int(position[0])][int(position[1])] != "  " and gamestate[int(position[0])][int(position[1])] == black_captures[len(black_captures)-1]):
                                del black_captures[len(black_captures)-1]
                            gamestate_check = copy.deepcopy(gamestate)
                            continue

                        gamestate = copy.deepcopy(gamestate_check)
                        
                    else:
                        print("\nThat move isn't legal, try again")
                        gamestate_check = copy.deepcopy(gamestate)
                        continue
                except Exception as e:
                    print("\nThat move isn't legal, try again")
                    gamestate_check = copy.deepcopy(gamestate)
                    continue

                color_to_move = "Clear"

                break

def islegal(color, move, gamestate, gamestate_check, check_tf, real_tf, white_captures, black_captures):

    piece = move[0:2]
    position = move[2:4]
    letter = position[:1]

    #Finds current index of piece in gamestate
    for i in gamestate:
        if piece in i:
            original_position = str(gamestate.index(i))+str(i.index(piece))

    #Original Position Vertical Index
    opv = int(original_position[0])
    #Original Position Horizontal Index
    oph = int(original_position[1])

    #Convert grid letters/numbers to index numbers
    if(position[1] in ["1","2","3","4","5","6","7","8"]):
        if(letter == "A"):
            new_position = str((8-int(position[1]))) + "0"
        elif(letter == "B"):
            new_position = str((8-int(position[1]))) + "1"
        elif(letter == "C"):
            new_position = str((8-int(position[1]))) + "2"
        elif(letter == "D"):
            new_position = str((8-int(position[1]))) + "3"
        elif(letter == "E"):
            new_position = str((8-int(position[1]))) + "4"
        elif(letter == "F"):
            new_position = str((8-int(position[1]))) + "5"
        elif(letter == "G"):
            new_position = str((8-int(position[1]))) + "6"
        elif(letter == "H"):
            new_position = str((8-int(position[1]))) + "7"
        else:
            return False
    else:
        return False

    #New Position Vertical Index
    npv = int(new_position[0])
    #New Position Horizontal Index
    nph = int(new_position[1])

    #PAWNS
    if(piece in ["W1","W2","W3","W4","W5","W6","W7","W8","B1","B2","B3","B4","B5","B6","B7","B8"]):
        if color == "White":
                
            #If it is the same letter on its first move and moves 2 steps
            if(nph == oph and (opv-npv) == 2 and opv == 6):
                #For each step forward...
                for i in range(1,3):
                    #If a piece exists, the move is illegal
                    if(gamestate[opv-i][oph] != "  "):
                        return False
                return True
            #On single moves
            elif(nph == oph and (opv-npv) == 1):
                if(gamestate[opv-1][oph] != "  "):
                    return False
                else:
                    if(real_tf == True):
                        return True
            #If it is diagonal and forward (attack)
            elif((nph == oph-1 or nph == oph+1) and npv == opv-1):
                #If the new position contains a black piece and it isn't the king
                if(gamestate[npv][nph][0].upper() == "B" and gamestate[npv][nph] != "BK"):
                    if(real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False
            else:
                return False
        elif color == "Black":
            #If it is the same letter on its first move and moves 2 steps
            if(nph == oph and (npv-opv) == 2 and opv == 1):
                #For each step forward...
                for i in range(1,3):
                    #If a piece exists, the move is illegal
                    if(gamestate[opv+i][oph] != "  "):
                        return False
                return True
            #On single moves
            elif(nph == oph and (npv-opv) == 1):
                if(gamestate[opv+1][oph] != "  "):
                    return False
                else:
                    if(real_tf == True):
                        return True
            #If it is diagonal and forward (attack)
            elif((nph == oph-1 or nph == oph+1) and npv == opv+1):
                #If the new position contains a white piece and it isn't the king
                if(gamestate[npv][nph][0].upper() == "W" and gamestate[npv][nph] != "WK"):
                    if(real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False
            else:
                return False
            
    #ROOKS
    
    if(piece in ["Wr","WR","Br","BR"]):
        #If it goes vertically
        if(nph == oph):
            #If it is moving up
            if(opv-npv > 0):
                hit = 0
                #For each step forward...
                for i in range(1,opv-npv):
                    #If it hits a piece except at the end, it's illegal
                    if(opv-i >= 0 and gamestate[opv-i][oph] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv-i][oph][0] == piece[0]):
                            return False
                        elif(piece[0] == color[0] and check_tf == True and gamestate[opv-i][oph][0] != piece[0] and gamestate[opv-i][oph][1] != "K" and hit == 0):
                            #If it's a real move and not being tested for checkmate
                            if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                                white_captures.append(gamestate[npv][nph])
                            elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                                black_captures.append(gamestate[npv][nph])
                                    
                            if(real_tf == True):
                                if(piece == "Wr"):
                                    Wr_moves[0] += 1
                                elif(piece == "WR"):
                                    WR_moves[0] += 1
                                elif(piece == "Br"):
                                    Br_moves[0] += 1
                                elif(piece == "BR"):
                                    BR_moves[0] += 1
                            return True
                #If it lands on it's own color, it's illegal
                if(piece[0] == color[0] and gamestate[npv][nph][0] != piece[0] and gamestate[npv][nph][1] != "K" and hit == 0):
                    #If the rook is white and lands on a black piece
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                        
                    if(real_tf == True):
                        if(piece == "Wr"):
                            Wr_moves[0] += 1
                        elif(piece == "WR"):
                            WR_moves[0] += 1
                        elif(piece == "Br"):
                            Br_moves[0] += 1
                        elif(piece == "BR"):
                            BR_moves[0] += 1
                    return True
                else:
                    return False
            #If it is moving down
            elif(opv-npv < 0):
                hit = 0
                for i in range(1,npv-opv):
                    #If it hits a piece along the way, it's illegal
                    if(opv+i <= 7 and gamestate[opv+i][oph] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv+i][oph][0] == piece[0]):
                            return False
                        elif(piece[0] == color[0] and check_tf == True and gamestate[opv+i][oph][0] != piece[0] and gamestate[opv+i][oph][1] != "K" and hit == 0):
                            if(real_tf == True):
                                if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                                    white_captures.append(gamestate[npv][nph])
                                elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                                    black_captures.append(gamestate[npv][nph])
                                
                                if(piece == "Wr"):
                                    Wr_moves[0] += 1
                                elif(piece == "WR"):
                                    WR_moves[0] += 1
                                elif(piece == "Br"):
                                    Br_moves[0] += 1
                                elif(piece == "BR"):
                                    BR_moves[0] += 1
                            return True
                if(piece[0] == color[0] and gamestate[npv][nph][0] != piece[0] and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                        
                    if(real_tf == True):
                        if(piece == "Wr"):
                            Wr_moves[0] += 1
                        elif(piece == "WR"):
                            WR_moves[0] += 1
                        elif(piece == "Br"):
                            Br_moves[0] += 1
                        elif(piece == "BR"):
                            BR_moves[0] += 1
                    return True
                else:
                    return False
        #If it goes horizontally
        elif(npv == opv):
            #If it is moving right
            if(nph-oph > 0):
                hit = 0
                #For each step forward...
                for i in range(1,nph-oph):
                    #If it hits a piece along the way, it's illegal
                    if(oph+i <= 7 and gamestate[opv][oph+i] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv][oph+i][0] == piece[0]):
                            return False
                        elif(piece[0] == color[0] and check_tf == True and gamestate[opv][oph+i][0] != piece[0] and gamestate[opv][oph+i][1] != "K" and hit == 0):

                            if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                                white_captures.append(gamestate[npv][nph])
                            elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                                black_captures.append(gamestate[npv][nph])
                                
                            if(real_tf == True):
                                if(piece == "Wr"):
                                    Wr_moves[0] += 1
                                elif(piece == "WR"):
                                    WR_moves[0] += 1
                                elif(piece == "Br"):
                                    Br_moves[0] += 1
                                elif(piece == "BR"):
                                    BR_moves[0] += 1
                            return True

                #If it lands on it's own color, it's illegal
                if(piece[0] == color[0] and gamestate[npv][nph][0] != piece[0] and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                        
                    if(real_tf == True):
                        if(piece == "Wr"):
                            Wr_moves[0] += 1
                        elif(piece == "WR"):
                            WR_moves[0] += 1
                        elif(piece == "Br"):
                            Br_moves[0] += 1
                        elif(piece == "BR"):
                            BR_moves[0] += 1
                    return True
                else:
                    return False
            #If it is moving left
            elif(nph-oph < 0):
                hit = 0
                for i in range(1,oph-nph):
                    #If it hits a piece along the way, it's illegal
                    if(oph-i >= 0 and gamestate[opv][oph-i] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        #If it's checking for a checkmate then it's just looking for moves
                        #meaning if islegal sees it hitting an enemy piece it's actually okay and legal
                        elif(check_tf == True and gamestate[opv][oph-i][0] == piece[0]):
                            return False
                        elif(piece[0] == color[0] and check_tf == True and gamestate[opv][oph-i][0] != piece[0] and gamestate[opv][oph-i] != "K" and hit == 0):
                            if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                                white_captures.append(gamestate[npv][nph])
                            elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                                black_captures.append(gamestate[npv][nph])
                            if(real_tf == True):
                                if(piece == "Wr"):
                                    Wr_moves[0] += 1
                                elif(piece == "WR"):
                                    WR_moves[0] += 1
                                elif(piece == "Br"):
                                    Br_moves[0] += 1
                                elif(piece == "BR"):
                                    BR_moves[0] += 1
                            return True
                        
                if(piece[0] == color[0] and gamestate[npv][nph][0] != piece[0] and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                        
                    if(real_tf == True):
                        if(piece == "Wr"):
                            Wr_moves[0] += 1
                        elif(piece == "WR"):
                            WR_moves[0] += 1
                        elif(piece == "Br"):
                            Br_moves[0] += 1
                        elif(piece == "BR"):
                            BR_moves[0] += 1
                    return True
                else:
                    return False
        else:
            return False

    #BISHOPS
    if(piece in ["WB","Wb","BB","Bb"]):
        #If it goes diagonally
        if(abs(npv-opv) == abs(nph-oph)):
            #Up and Right
            if((opv-npv) > 0 and (nph-oph) > 0):
                hit = 0
                #If it hits a piece along the way, it's illegal
                for i in range(1,nph-oph):
                    #Step up and right each time
                    if(opv-i >= 0 and oph+i <= 7 and gamestate[opv-i][oph+i] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv-i][oph+i][0] == piece[0]):
                            return False
                        elif(check_tf == True and gamestate[opv-i][oph+i][0] != piece[0] and gamestate[opv-i][oph+i] != "K" and hit == 0):
                            return True
                if(piece[0] == color[0] and gamestate[npv][nph][0] != piece[0] and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False
                    
            #Up and Left
            elif((opv-npv) > 0 and (oph-nph) > 0):
                hit = 0
                #If it hits a piece along the way, it's illegal
                for i in range(1,oph-nph):
                    #Step up and left each time
                    if(opv-i >= 0 and oph-i >= 0 and gamestate[opv-i][oph-i] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv-i][oph-i][0] == piece[0]):
                            return False
                        elif(check_tf == True and gamestate[opv-i][oph-i][0] != piece[0] and gamestate[opv-i][oph-i] != "K" and hit == 0):
                            return True
                if(piece[0] == color[0] and gamestate[npv][nph][0] != piece[0] and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False
                
            #Down and Right
            elif((npv-opv) > 0 and (nph-oph) > 0):
                hit = 0
                #If it hits a piece along the way, it's illegal
                for i in range(1,nph-oph):
                    #Step down and right each time
                    if(opv+i <= 7 and oph+i <= 7 and gamestate[opv+i][oph+i] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv+i][oph+i][0] == piece[0]):
                            return False
                        elif(check_tf == True and gamestate[opv+i][oph+i][0] != piece[0] and gamestate[opv+i][oph+i] != "K" and hit == 0):
                            return True
                if(piece[0] == color[0] and gamestate[npv][nph][0] != piece[0] and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False
                 
            #Down and Left
            elif((npv-opv) > 0 and (oph-nph) > 0):
                hit = 0
                #If it hits a piece along the way, it's illegal
                for i in range(1,oph-nph):
                    #Step down and left each time
                    if(opv+i <= 7 and oph-i >= 0 and gamestate[opv+i][oph-i] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv+i][oph-i][0] == piece[0]):
                            return False
                        elif(check_tf == True and gamestate[opv+i][oph-i][0] != piece[0] and gamestate[opv+i][oph-i] != "K" and hit == 0):
                            return True
                if(piece[0] == color[0] and gamestate[npv][nph][0] != piece[0] and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False

    #KNIGHTS
    if(piece in ["WN","Wn","BN","Bn"]):
        #If piece moves two units one way and one unit the other
        if((abs(npv-opv) == 2 or abs(nph-oph) == 2) and (abs(npv-opv) == 1 or abs(nph-oph) == 1)):
            if(piece[0] == color[0] and gamestate[npv][nph][0] != piece[0] and gamestate[npv][nph][1] != "K"):
                if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                    white_captures.append(gamestate[npv][nph])
                elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                    black_captures.append(gamestate[npv][nph])
                return True
            else:
                return False
        else:
            return False

    #QUEENS
    if(piece in ["WQ","BQ"] or piece[0] == "w" or piece[0] == "b"):
        #If it goes diagonally
        if(abs(npv-opv) == abs(nph-oph)):
            #Up and Right
            if((opv-npv) > 0 and (nph-oph) > 0):
                hit = 0
                #If it hits a piece along the way, it's illegal
                for i in range(1,nph-oph):
                    #Step up and right each time
                    if(opv-i >= 0 and oph+i <= 7 and gamestate[opv-i][oph+i] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv-i][oph+i][0] == piece[0].upper()):
                            return False
                        elif(piece[0].upper() == color[0] and check_tf == True and gamestate[opv-i][oph+i][0] != piece[0].upper() and gamestate[opv-i][oph+i] != "K" and hit == 0):
                            return True
                if(piece[0].upper() == color[0] and gamestate[npv][nph][0] != piece[0].upper() and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False
                    
            #Up and Left
            elif((opv-npv) > 0 and (oph-nph) > 0):
                hit = 0
                #If it hits a piece along the way, it's illegal
                for i in range(1,oph-nph):
                    #Step up and left each time
                    if(opv-i >= 0 and oph-i >= 0 and gamestate[opv-i][oph-i] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv-i][oph-i][0] == piece[0].upper()):
                            return False
                        elif(piece[0].upper() == color[0] and check_tf == True and gamestate[opv-i][oph-i][0] != piece[0].upper() and gamestate[opv-i][oph-i] != "K" and hit == 0):
                            return True
                if(piece[0].upper() == color[0] and gamestate[npv][nph][0] != piece[0].upper() and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False
                
            #Down and Right
            elif((npv-opv) > 0 and (nph-oph) > 0):
                hit = 0
                #If it hits a piece along the way, it's illegal
                for i in range(1,nph-oph):
                    #Step down and right each time
                    if(opv+i <= 7 and oph+i <= 7 and gamestate[opv+i][oph+i] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv+i][oph+i][0] == piece[0].upper()):
                            return False
                        elif(piece[0].upper() == color[0] and check_tf == True and gamestate[opv+i][oph+i][0] != piece[0].upper() and gamestate[opv+i][oph+i] != "K" and hit == 0):
                            return True
                if(piece[0].upper() == color[0] and gamestate[npv][nph][0] != piece[0].upper() and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False
                 
            #Down and Left
            elif((npv-opv) > 0 and (oph-nph) > 0):
                hit = 0
                #If it hits a piece along the way, it's illegal
                for i in range(1,oph-nph):
                    #Step down and left each time
                    if(opv+i <= 7 and oph-i >= 0 and gamestate[opv+i][oph-i] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv+i][oph-i][0] == piece[0].upper()):
                            return False
                        elif(piece[0].upper() == color[0] and check_tf == True and gamestate[opv+i][oph-i][0] != piece[0].upper() and gamestate[opv+i][oph-i] != "K" and hit == 0):
                            return True
                if(piece[0].upper() == color[0] and gamestate[npv][nph][0] != piece[0].upper() and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False
                    
        #If it goes vertically
        elif(nph == oph):
            #If it is moving up
            if(opv-npv > 0):
                hit = 0
                #For each step forward...
                for i in range(1,opv-npv):
                    #If it hits a piece except at the end, it's illegal
                    if(opv-i >= 0 and gamestate[opv-i][oph] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv-i][oph][0] == piece[0].upper()):
                            return False
                        elif(piece[0].upper() == color[0] and check_tf == True and gamestate[opv-i][oph][0] != piece[0].upper() and gamestate[opv-i][oph][1] != "K" and hit == 0):
                            return True
                #If it lands on it's own color, it's illegal
                if(piece[0].upper() == color[0] and gamestate[npv][nph][0] != piece[0].upper() and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False
            #If it is moving down
            elif(opv-npv < 0):
                hit = 0
                for i in range(1,npv-opv):
                    #If it hits a piece along the way, it's illegal
                    if(opv+i <= 7 and gamestate[opv+i][oph] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv+i][oph][0] == piece[0].upper()):
                            return False
                        elif(piece[0].upper() == color[0] and check_tf == True and gamestate[opv+i][oph][0] != piece[0].upper() and gamestate[opv+i][oph][1] != "K" and hit == 0):
                            return True
                if(piece[0].upper() == color[0] and gamestate[npv][nph][0] != piece[0].upper() and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False
        #If it goes horizontally
        elif(npv == opv):
            #If it is moving right
            if(nph-oph > 0):
                hit = 0
                #For each step forward...
                for i in range(1,nph-oph):
                    #If it hits a piece along the way, it's illegal
                    if(oph+i <= 7 and gamestate[opv][oph+i] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        elif(check_tf == True and gamestate[opv][oph+i][0] == piece[0].upper()):
                            return False
                        elif(check_tf == True and gamestate[opv][oph+i][0] != piece[0].upper() and gamestate[opv][oph+i][1] != "K" and hit == 0):
                            return True

                #If it lands on it's own color, it's illegal
                if(gamestate[npv][nph][0] != piece[0].upper() and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False
            #If it is moving left
            elif(nph-oph < 0):
                hit = 0
                for i in range(1,oph-nph):
                    #If it hits a piece along the way, it's illegal
                    if(oph-i >= 0 and gamestate[opv][oph-i] != "  "):
                        hit += 1
                        if(check_tf != True):
                            return False
                        #If it's checking for a checkmate then it's just looking for moves
                        #meaning if islegal sees it hitting an enemy piece it's actually okay and legal
                        elif(check_tf == True and gamestate[opv][oph-i][0] == piece[0].upper()):
                            return False
                        elif(piece[0].upper() == color[0] and check_tf == True and gamestate[opv][oph-i][0] != piece[0].upper() and gamestate[opv][oph-i] != "K" and hit == 0):
                            return True
                        
                if(piece[0].upper() == color[0] and gamestate[npv][nph][0] != piece[0].upper() and gamestate[npv][nph][1] != "K" and hit == 0):
                    if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                        white_captures.append(gamestate[npv][nph])
                    elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                        black_captures.append(gamestate[npv][nph])
                    return True
                else:
                    return False
        else:
            return False
    #KINGS
    
    if(piece in ["WK","BK"]):
        #If it goes diagonally one square
        if(abs(npv-opv) == abs(nph-oph) and abs(npv-opv) == 1):
            if(piece[0] == color[0] and gamestate[npv][nph][0] != piece[0] and gamestate[npv][nph][1] != "K"):
                if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                    white_captures.append(gamestate[npv][nph])
                elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                    black_captures.append(gamestate[npv][nph])
                    
                if(piece == "WK"):
                    WK_moves[0] += 1
                    return True
                elif(piece == "BK"):
                    BK_moves[0] += 1
                    return True
            else:
                return False
        #If it goes vertically one square
        elif(nph == oph and abs(npv-opv) == 1):
            if(piece[0] == color[0] and gamestate[npv][nph][0] != piece[0] and gamestate[npv][nph][1] != "K"):
                if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                    white_captures.append(gamestate[npv][nph])
                elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                    black_captures.append(gamestate[npv][nph])

                if(piece == "WK"):
                    WK_moves[0] += 1
                    return True
                elif(piece == "BK"):
                    BK_moves[0] += 1
                    return True

            else:
                return False
        #If it goes horizontally one square
        elif(npv == opv and abs(nph-oph) == 1):
            if(piece[0] == color[0] and gamestate[npv][nph][0] != piece[0] and gamestate[npv][nph][1] != "K"):
                if(color == "White" and gamestate[npv][nph][0].upper() == "B" and real_tf == True):
                    white_captures.append(gamestate[npv][nph])
                elif(color == "Black" and gamestate[npv][nph][0].upper() == "W" and real_tf == True):
                    black_captures.append(gamestate[npv][nph])
                    
                if(piece == "WK"):
                    WK_moves[0] += 1
                    return True
                elif(piece == "BK"):
                    BK_moves[0] += 1
                    return True
            else:
                return False
        #WHITE KING Castling Long
        elif(piece[0] == color[0] and piece == "WK" and gamestate[7][4] == "WK" and WK_moves[0] == 0 and Wr_moves[0] == 0 and npv == 7 and nph == 2 and gamestate[7][1] == "  " and gamestate[7][2] == "  " and gamestate[7][3] == "  "):
            #If King moves two spaces left and it's empty between WK and Wr
            gamestate_temp = copy.deepcopy(gamestate)

            if(ischeck(gamestate_temp, check)[0] != "White"):

                gamestate_temp[7][4] = "  "
                gamestate_temp[7][3] = "WK"

                if(ischeck(gamestate_temp, check)[0] != "White"):
                    
                    gamestate_check[7][0] = "  "
                    gamestate_check[7][3] = "Wr"
                    return True
                    
        #WHITE KING Castling Short
        elif(piece[0] == color[0] and piece == "WK" and gamestate[7][4] == "WK" and WK_moves[0] == 0 and WR_moves[0] == 0 and npv == 7 and nph == 6 and gamestate[7][5] == "  " and gamestate[7][6] == "  "):
            #If King moves two spaces left and it's empty between WK and Wr
            gamestate_temp = copy.deepcopy(gamestate)

            if(ischeck(gamestate_temp, check)[0] != "White"):

                gamestate_temp[7][4] = "  "
                gamestate_temp[7][5] = "WK"

                if(ischeck(gamestate_temp, check)[0] != "White"):
                    
                    gamestate_check[7][7] = "  "
                    gamestate_check[7][5] = "WR"
                    return True
            
        #BLACK KING Castling Long
        elif(piece[0] == color[0] and piece == "BK" and gamestate[0][4] == "BK" and BK_moves[0] == 0 and BR_moves[0] == 0 and npv == 0 and nph == 2 and gamestate[0][1] == "  " and gamestate[0][2] == "  " and gamestate[0][3] == "  "):

            gamestate_temp = copy.deepcopy(gamestate)

            if(ischeck(gamestate_temp, check)[1] != "Black"):

                gamestate_temp[0][4] = "  "
                gamestate_temp[0][3] = "BK"

                if(ischeck(gamestate_temp, check)[1] != "Black"):
                    
                    gamestate_check[0][0] = "  "
                    gamestate_check[0][3] = "BR"
                    return True

        #BLACK KING Castling Short
        elif(piece[0] == color[0] and piece == "BK" and gamestate[0][4] == "BK" and BK_moves[0] == 0 and Br_moves[0] == 0 and npv == 0 and nph == 6 and gamestate[0][5] == "  " and gamestate[0][6] == "  "):
            
            gamestate_temp = copy.deepcopy(gamestate)

            if(ischeck(gamestate_temp, check)[1] != "Black"):

                gamestate_temp[0][4] = "  "
                gamestate_temp[0][5] = "BK"

                if(ischeck(gamestate_temp, check)[1] != "Black"):
                    
                    gamestate_check[0][7] = "  "
                    gamestate_check[0][5] = "Br"
                    return True
        else:
            return False

        

def ischeck(gamestate_check, check):
    #Need to provide the possibility of holding two checks
    #If White were in check and moved to put the Black king in check, without checking for two it would say it's a legal move
    #Because the function would see that the Black king is in check and stop before realizing White is still in check as well

    check = ["  ","  "]
    
    #Check if any piece is attacking a king
    #Check every legal direction for every piece every move to check for any type of check
    for i in gamestate_check:
        
        pv = gamestate_check.index(i)
        
        for j in i:
            
            ph = i.index(j)
            
            #PAWNS
            if j in ["W1","W2","W3","W4","W5","W6","W7","W8"]:
                #Up and left or up and right attacks king
                try:
                    if(gamestate_check[pv-1][ph-1] == "BK" or gamestate_check[pv-1][ph+1] == "BK"):
                        check[1] = "Black"
                except:
                    pass
            elif j in ["B1","B2","B3","B4","B5","B6","B7","B8"]:
                try:
                    if(gamestate_check[pv+1][ph-1] == "WK" or gamestate_check[pv+1][ph+1] == "WK"):
                        check[0] = "White"
                except:
                    pass

            #ROOKS
            elif j in ["Wr","WR","Br","BR"]:
                #Up, each square from height up
                while(True):
                    for k in range(1,pv+1):
                        if(gamestate_check[pv-k][ph] != "  "):
                            if(gamestate_check[pv-k][ph] == "BK" and j[0].upper() == "W" and pv-k >= 0):
                                check[1] = "Black"
                            if(gamestate_check[pv-k][ph] == "WK" and j[0].upper() == "B" and pv-k >= 0):
                                check[0] = "White"
                            else:
                                break
                    break
                #Down, each square from height down
                while(True):
                    for k in range(1,8-pv):
                        if(gamestate_check[pv+k][ph] != "  "):
                            if(gamestate_check[pv+k][ph] == "BK" and j[0].upper() == "W"):
                                check[1] = "Black"
                            if(gamestate_check[pv+k][ph] == "WK" and j[0].upper() == "B"):
                                check[0] = "White"
                            else:
                                break
                    break
                #Left, each square left from position
                while(True):
                    for k in range(1,ph+1):
                        if(gamestate_check[pv][ph-k] != "  "):
                            if(gamestate_check[pv][ph-k] == "BK" and j[0].upper() == "W" and ph-k >= 0):
                                check[1] = "Black"
                            if(gamestate_check[pv][ph-k] == "WK" and j[0].upper() == "B" and ph-k >= 0):
                                check[0] = "White"
                            else:
                                break
                    break
                #Right, each square right from position
                while(True):
                    for k in range(1,8-ph):
                        if(gamestate_check[pv][ph+k] != "  "):
                            if(gamestate_check[pv][ph+k] == "BK" and j[0].upper() == "W"):
                                check[1] = "Black"
                            if(gamestate_check[pv][ph+k] == "WK" and j[0].upper() == "B"):
                                check[0] = "White"
                            else:
                                break
                    break

            #BISHOPS
            elif j in ["WB","Wb","BB","Bb"]:
                #Up and to the right
                while(True):
                    for k in range(1,pv+1):
                        try:
                            if(gamestate_check[pv-k][ph+k] != "  "):
                                if(gamestate_check[pv-k][ph+k] == "BK" and j[0].upper() == "W" and pv-k >= 0 and ph+k <= 7):
                                    check[1] = "Black"
                                if(gamestate_check[pv-k][ph+k] == "WK" and j[0].upper() == "B" and pv-k >= 0 and ph+k <= 7):
                                    check[0] = "White"
                                else:
                                    break
                        except:
                            pass
                    break
                #Down and to the right
                while(True):
                    for k in range(1,8-pv):
                        try:
                            if(gamestate_check[pv+k][ph+k] != "  "):
                                if(gamestate_check[pv+k][ph+k] == "BK" and j[0].upper() == "W" and pv+k <= 7 and ph+k <= 7):
                                    check[1] = "Black"
                                if(gamestate_check[pv+k][ph+k] == "WK" and j[0].upper() == "B" and pv+k >= 0 and ph+k <= 7):
                                    check[0] = "White"
                                else:
                                    break
                        except:
                            pass
                    break
                #Up and to the left
                while(True):
                    for k in range(1,pv+1):
                        try:
                            if(gamestate_check[pv-k][ph-k] != "  "):
                                if(gamestate_check[pv-k][ph-k] == "BK" and j[0].upper() == "W" and pv-k >= 0 and ph-k >= 0):
                                    check[1] = "Black"
                                if(gamestate_check[pv-k][ph-k] == "WK" and j[0].upper() == "B" and pv-k >= 0 and ph+k >= 0):
                                    check[0] = "White"
                                else:
                                    break
                        except:
                            pass
                    break
                #Down and to the left
                while(True):
                    for k in range(1,8-pv):
                        try:
                            if(gamestate_check[pv+k][ph-k] != "  "):
                                if(gamestate_check[pv+k][ph-k] == "BK" and j[0].upper() == "W" and pv+k <= 7 and ph-k >= 0):
                                    check[1] = "Black"
                                if(gamestate_check[pv+k][ph-k] == "WK" and j[0].upper() == "B" and pv+k <= 7 and ph-k >= 0):
                                    check[0] = "White"
                                else:
                                    break
                        except:
                            pass
                    break

            #KNIGHTS
            elif j in ["WN","Wn","BN","Bn"]:
                #Up 2 Right 1
                try:
                    if(gamestate_check[pv-2][ph+1] == "BK" and j[0].upper() == "W" and pv-2 >= 0 and ph+1 <= 7):
                        check[1] = "Black"
                    if(gamestate_check[pv-2][ph+1] == "WK" and j[0].upper() == "B" and pv-2 >= 0 and ph+1 <= 7):
                        check[0] = "White"
                except:
                    pass
                #Up 2 Left 1
                try:
                    if(gamestate_check[pv-2][ph-1] == "BK" and j[0].upper() == "W" and pv-2 >= 0 and ph-1 >= 0):
                        check[1] = "Black"
                    if(gamestate_check[pv-2][ph-1] == "WK" and j[0].upper() == "B" and pv-2 >= 0 and ph-1 >= 0):
                        check[0] = "White"
                except:
                    pass
                #Down 2 Right 1
                try:
                    if(gamestate_check[pv+2][ph+1] == "BK" and j[0].upper() == "W" and pv+2 <= 7 and ph+1 <= 7):
                        check[1] = "Black"
                    if(gamestate_check[pv+2][ph+1] == "WK" and j[0].upper() == "B" and pv+2 <= 7 and ph+1 <= 7):
                        check[0] = "White"
                except:
                    pass
                #Down 2 Left 1
                try:
                    if(gamestate_check[pv+2][ph-1] == "BK" and j[0].upper() == "W" and pv+2 <= 7 and ph-1 >= 0):
                        check[1] = "Black"
                    if(gamestate_check[pv+2][ph-1] == "WK" and j[0].upper() == "B" and pv+2 <= 7 and ph-1 >= 0):
                        check[0] = "White"
                except:
                    pass
                #Right 2 Up 1
                try:
                    if(gamestate_check[pv-1][ph+2] == "BK" and j[0].upper() == "W" and pv-1 >= 0 and ph+2 <= 7):
                        check[1] = "Black"
                    if(gamestate_check[pv-1][ph+2] == "WK" and j[0].upper() == "B" and pv-1 >= 0 and ph+2 <= 7):
                        check[0] = "White"
                except:
                    pass
                #Right 2 Down 1
                try:
                    if(gamestate_check[pv+1][ph+2] == "BK" and j[0].upper() == "W" and pv+1 <= 7 and ph+2 <= 7):
                        check[1] = "Black"
                    if(gamestate_check[pv+1][ph+2] == "WK" and j[0].upper() == "B" and pv+1 <= 7 and ph+2 <= 7):
                        check[0] = "White"
                except:
                    pass
                #Left 2 Up 1
                try:
                    if(gamestate_check[pv-1][ph-2] == "BK" and j[0].upper() == "W" and pv-1 >= 0 and ph-2 >= 0):
                        check[1] = "Black"
                    if(gamestate_check[pv-1][ph-2] == "WK" and j[0].upper() == "B" and pv-1 >= 0 and ph-2 >= 0):
                        check[0] = "White"
                except:
                    pass
                #Left 2 Down 1
                try:
                    if(gamestate_check[pv+1][ph-2] == "BK" and j[0].upper() == "W" and pv+1 <= 7 and ph-2 >= 0):
                        check[1] = "Black"
                    if(gamestate_check[pv+1][ph-2] == "WK" and j[0].upper() == "B" and pv+1 <= 7 and ph-2 >= 0):
                        check[0] = "White"
                except:
                    pass

            #QUEENS
            elif j in ["WQ","BQ"] or j[0] == "w" or j[0] == "b":
                #Up, each square from height up
                while(True):
                    for k in range(1,pv+1):
                        if(gamestate_check[pv-k][ph] != "  "):
                            if(gamestate_check[pv-k][ph] == "BK" and j[0].upper() == "W" and pv-k >= 0):
                                check[1] = "Black"
                            if(gamestate_check[pv-k][ph] == "WK" and j[0].upper() == "B" and pv-k >= 0):
                                check[0] = "White"
                            else:
                                break
                    break
                #Down, each square from height down
                while(True):
                    for k in range(1,8-pv):
                        if(gamestate_check[pv+k][ph] != "  "):
                            if(gamestate_check[pv+k][ph] == "BK" and j[0].upper() == "W"):
                                check[1] = "Black"
                            if(gamestate_check[pv+k][ph] == "WK" and j[0].upper() == "B"):
                                check[0] = "White"
                            else:
                                break
                    break
                #Left, each square left from position
                while(True):
                    for k in range(1,ph+1):
                        if(gamestate_check[pv][ph-k] != "  "):
                            if(gamestate_check[pv][ph-k] == "BK" and j[0].upper() == "W" and ph-k >= 0):
                                check[1] = "Black"
                            if(gamestate_check[pv][ph-k] == "WK" and j[0].upper() == "B" and ph-k >= 0):
                                check[0] = "White"
                            else:
                                break
                    break
                #Right, each square right from position
                while(True):
                    for k in range(1,8-ph):
                        if(gamestate_check[pv][ph+k] != "  "):
                            if(gamestate_check[pv][ph+k] == "BK" and j[0].upper() == "W"):
                                check[1] = "Black"
                            if(gamestate_check[pv][ph+k] == "WK" and j[0].upper() == "B"):
                                check[0] = "White"
                            else:
                                break
                    break
                #Up and to the right
                while(True):
                    for k in range(1,pv+1):
                        try:
                            if(gamestate_check[pv-k][ph+k] != "  "):
                                if(gamestate_check[pv-k][ph+k] == "BK" and j[0].upper() == "W" and pv-k >= 0 and ph+k <= 7):
                                    check[1] = "Black"
                                if(gamestate_check[pv-k][ph+k] == "WK" and j[0].upper() == "B" and pv-k >= 0 and ph+k <= 7):
                                    check[0] = "White"
                                else:
                                    break
                        except:
                            pass
                    break
                #Down and to the right
                while(True):
                    for k in range(1,8-pv):
                        try:
                            if(gamestate_check[pv+k][ph+k] != "  "):
                                if(gamestate_check[pv+k][ph+k] == "BK" and j[0].upper() == "W" and pv+k <= 7 and ph+k <= 7):
                                    check[1] = "Black"
                                if(gamestate_check[pv+k][ph+k] == "WK" and j[0].upper() == "B" and pv+k >= 0 and ph+k <= 7):
                                    check[0] = "White"
                                else:
                                    break
                        except:
                            pass
                    break
                #Up and to the left
                while(True):
                    for k in range(1,pv+1):
                        try:
                            if(gamestate_check[pv-k][ph-k] != "  "):
                                if(gamestate_check[pv-k][ph-k] == "BK" and j[0].upper() == "W" and pv-k >= 0 and ph-k >= 0):
                                    check[1] = "Black"
                                if(gamestate_check[pv-k][ph-k] == "WK" and j[0].upper() == "B" and pv-k >= 0 and ph+k >= 0):
                                    check[0] = "White"
                                else:
                                    break
                        except:
                            pass
                    break
                #Down and to the left
                while(True):
                    for k in range(1,8-pv):
                        try:
                            if(gamestate_check[pv+k][ph-k] != "  "):
                                if(gamestate_check[pv+k][ph-k] == "BK" and j[0].upper() == "W" and pv+k <= 7 and ph-k >= 0):
                                    check[1] = "Black"
                                if(gamestate_check[pv+k][ph-k] == "WK" and j[0].upper() == "B" and pv+k <= 7 and ph-k >= 0):
                                    check[0] = "White"
                                else:
                                    break
                        except:
                            pass
                    break
            #KINGS
            elif j in ["WK","BK"]:
                #Up
                try:
                    if(gamestate_check[pv-1][ph] != "  "):
                        if(gamestate_check[pv-1][ph] == "BK" and j[0].upper() == "W" and pv-1 >= 0):
                            check[1] = "Black"
                        if(gamestate_check[pv-1][ph] == "WK" and j[0].upper() == "B" and pv-1 >= 0):
                            check[0] = "White"
                except:
                    pass
                #Down
                try:
                    if(gamestate_check[pv+1][ph] != "  "):
                        if(gamestate_check[pv+1][ph] == "BK" and j[0].upper() == "W"):
                            check[1] = "Black"
                        if(gamestate_check[pv+1][ph] == "WK" and j[0].upper() == "B"):
                            check[0] = "White"
                except:
                    pass
                #Left
                try:
                    if(gamestate_check[pv][ph-1] != "  "):
                        if(gamestate_check[pv][ph-1] == "BK" and j[0].upper() == "W" and ph-1 >= 0):
                            check[1] = "Black"
                        if(gamestate_check[pv][ph-1] == "WK" and j[0].upper() == "B" and ph-1 >= 0):
                            check[0] = "White"
                except:
                    pass
                #Right
                try:
                    if(gamestate_check[pv][ph+1] != "  "):
                        if(gamestate_check[pv][ph+1] == "BK" and j[0].upper() == "W"):
                            check[1] = "Black"
                        if(gamestate_check[pv][ph+1] == "WK" and j[0].upper() == "B"):
                            check[0] = "White"
                except:
                    pass
                #Up and Right
                try:
                    if(gamestate_check[pv-1][ph+1] != "  "):
                        if(gamestate_check[pv-1][ph+1] == "BK" and j[0].upper() == "W" and pv-1 >= 0):
                            check[1] = "Black"
                        if(gamestate_check[pv-1][ph+1] == "WK" and j[0].upper() == "B" and pv-1 >= 0):
                            check[0] = "White"
                except:
                    pass
                #Up and Left
                try:
                    if(gamestate_check[pv-1][ph-1] != "  "):
                        if(gamestate_check[pv-1][ph-1] == "BK" and j[0].upper() == "W" and ph-1 >= 0 and pv-1 >= 0):
                            check[1] = "Black"
                        if(gamestate_check[pv-1][ph-1] == "WK" and j[0].upper() == "B" and ph-1 >= 0 and pv-1 >= 0):
                            check[0] = "White"
                except:
                    pass
                #Down and Right
                try:
                    if(gamestate_check[pv+1][ph+1] != "  "):
                        if(gamestate_check[pv+1][ph+1] == "BK" and j[0].upper() == "W"):
                            check[1] = "Black"
                        if(gamestate_check[pv+1][ph+1] == "WK" and j[0].upper() == "B"):
                            check[0] = "White"
                except:
                    pass
                #Down and Left
                try:
                    if(gamestate_check[pv+1][ph-1] != "  "):
                        if(gamestate_check[pv+1][ph-1] == "BK" and j[0].upper() == "W" and ph-1 >= 0):
                            check[1] = "Black"
                        if(gamestate_check[pv+1][ph-1] == "WK" and j[0].upper() == "B" and ph-1 >= 0):
                            check[0] = "White"
                except:
                    pass
    return check

#Returns True if a legal move can be played to take the color out of check
def notcheckmate(color, gamestate, gamestate_check):
    gamestate = copy.deepcopy(gamestate_check)
    #For each possible move need to check if it's legal and then see if the king is still in check if that move is played
    #Check every legal direction for every piece every move to check for any type of check
    for i in gamestate_check:
        #Have to always refresh the gamestate_check
        gamestate_check = copy.deepcopy(gamestate)

        pv = gamestate_check.index(i)
        for j in i:
            #Always refresh
            gamestate_check = copy.deepcopy(gamestate)

            ph = i.index(j)

            #KINGS
            if j in ["WK","BK"]:
                #Up one square
                if(pv-1 >= 0 and islegal(color, index_to_grid(j+str(pv-1)+str(ph)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv-1][ph] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #Down one square
                if(pv+1 <= 7 and islegal(color, index_to_grid(j+str(pv+1)+str(ph)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv+1][ph] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #Right one square
                if(ph+1 <= 7 and islegal(color, index_to_grid(j+str(pv)+str(ph+1)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv][ph+1] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #Left one square
                if(ph-1 >= 0 and islegal(color, index_to_grid(j+str(pv)+str(ph-1)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv][ph-1] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #Up and right one square
                if(pv-1 >= 0 and ph+1 <= 7 and islegal(color, index_to_grid(j+str(pv-1)+str(ph+1)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv-1][ph+1] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #Up and left one square
                if(pv-1 >= 0 and ph-1 >= 0 and islegal(color, index_to_grid(j+str(pv-1)+str(ph-1)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv-1][ph-1] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #Down and right one square
                if(pv+1 <= 7 and ph+1 <= 7 and islegal(color, index_to_grid(j+str(pv+1)+str(ph+1)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv+1][ph+1] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #Down and left one square
                if(pv+1 <= 7 and ph-1 >= 0 and islegal(color, index_to_grid(j+str(pv+1)+str(ph-1)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv+1][ph-1] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        return True
                    gamestate_check = copy.deepcopy(gamestate)

            #QUEENS
            if j in ["WQ","BQ"] or j[0] == "w" or j[0] == "b":
                #Up and Right
                for k in range(1,pv+1):
                    if(pv-k >= 0 and ph+k <= 7 and islegal(color, index_to_grid(j+str(pv-k)+str(ph+k)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv-k][ph+k] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True

                    gamestate_check = copy.deepcopy(gamestate)
                #Up and Left
                for k in range(1,pv+1):
                    if(pv-k >= 0 and ph-k >= 0 and islegal(color, index_to_grid(j+str(pv-k)+str(ph-k)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv-k][ph-k] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True

                    gamestate_check = copy.deepcopy(gamestate)
                #Down and Right
                for k in range(1,8-pv):
                    if(pv+k <= 7 and ph+k <= 7 and islegal(color, index_to_grid(j+str(pv+k)+str(ph+k)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv+k][ph+k] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True

                    gamestate_check = copy.deepcopy(gamestate)
                #Down and Left
                for k in range(1,8-pv):
                    if(pv+k <= 7 and ph-k >= 0 and islegal(color, index_to_grid(j+str(pv+k)+str(ph-k)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv+k][ph-k] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True
                    gamestate_check = copy.deepcopy(gamestate)
                #Up
                for k in range(1,pv+1):
                    if(pv-k >= 0 and islegal(color, index_to_grid(j+str(pv-k)+str(ph)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv-k][ph] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True
                    gamestate_check = copy.deepcopy(gamestate)
                
                #Down
                for k in range(1,8-pv):
                    if(pv+k <= 7 and islegal(color, index_to_grid(j+str(pv+k)+str(ph)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv+k][ph] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True
                    gamestate_check = copy.deepcopy(gamestate)
                
                #Left
                for k in range(1,ph+1):
                    if(ph-k >= 0 and islegal(color, index_to_grid(j+str(pv)+str(ph-k)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv][ph-k] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True
                    gamestate_check = copy.deepcopy(gamestate)
                    

                #Right
                for k in range(1,8-ph):
                    if(ph+k <= 7 and islegal(color, index_to_grid(j+str(pv)+str(ph+k)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv][ph+k] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True
                    gamestate_check = copy.deepcopy(gamestate)
                    
            
            #KNIGHTS
            #WHITE/BLACK KNIGHTS
            #if(color == "White"):
            if j in ["WN","Wn","BN","Bn"]:
                #2 Up 1 Right
                if(pv-2 >= 0 and ph+1 <= 7 and islegal(color, index_to_grid(j+str(pv-2)+str(ph+1)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv-2][ph+1] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #2 Up 1 Left
                if(pv-2 >= 0 and ph-1 >= 0 and islegal(color, index_to_grid(j+str(pv-2)+str(ph-1)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv-2][ph-1] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #1 Up 2 Right
                if(pv-1 >= 0 and ph+2 <= 7 and islegal(color, index_to_grid(j+str(pv-1)+str(ph+2)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv-1][ph+2] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #1 Up 2 Left
                if(pv-1 >= 0 and ph-2 <= 7 and islegal(color, index_to_grid(j+str(pv-1)+str(ph-2)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv-1][ph-2] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #2 Down 1 Right
                if(pv+2 <= 7 and ph+1 <= 7 and islegal(color, index_to_grid(j+str(pv+2)+str(ph+1)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv+2][ph+1] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #2 Down 1 Left
                if(pv+2 <= 7 and ph-1 >= 0 and islegal(color, index_to_grid(j+str(pv+2)+str(ph-1)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv+2][ph-1] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #1 Down 2 Right
                if(pv+1 <= 7 and ph+2 <= 7 and islegal(color, index_to_grid(j+str(pv+1)+str(ph+2)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv+1][ph+2] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        
                        return True
                    gamestate_check = copy.deepcopy(gamestate)
                #1 Down 2 Left
                if(pv+1 <= 7 and ph-2 >= 0 and islegal(color, index_to_grid(j+str(pv+1)+str(ph-2)), gamestate_check, None, True, False, white_captures, black_captures)):
                    gamestate_check[pv][ph] = "  "
                    gamestate_check[pv+1][ph-2] = j

                    if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                        
                        return True
                    elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                        
                        return True
                    gamestate_check = copy.deepcopy(gamestate)

            
            #BISHOPS
            #WHITE/BLACK BISHOPS
            #if(color == "White"):
            if j in ["WB","Wb","BB","Bb"]:
                #Up and Right
                for k in range(1,pv+1):
                    if(pv-k >= 0 and ph+k <= 7 and islegal(color, index_to_grid(j+str(pv-k)+str(ph+k)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv-k][ph+k] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True

                    gamestate_check = copy.deepcopy(gamestate)
                #Up and Left
                for k in range(1,pv+1):
                    if(pv-k >= 0 and ph-k >= 0 and islegal(color, index_to_grid(j+str(pv-k)+str(ph-k)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv-k][ph-k] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True

                    gamestate_check = copy.deepcopy(gamestate)
                #Down and Right
                for k in range(1,pv+1):
                    if(pv+k <= 7 and ph+k <= 7 and islegal(color, index_to_grid(j+str(pv+k)+str(ph+k)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv+k][ph+k] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True

                    gamestate_check = copy.deepcopy(gamestate)
                #Down and Left
                for k in range(1,pv+1):
                    if(pv+k <= 7 and ph-k >= 0 and islegal(color, index_to_grid(j+str(pv+k)+str(ph-k)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv+k][ph-k] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True
                        
                    gamestate_check = copy.deepcopy(gamestate)
                        

            #ROOKS
            #WHITE/BLACK ROOKS
            #if(color == "White"):
            if j in ["WR","Wr","BR","Br"]:
                #Up
                for k in range(1,pv+1):
                    if(pv-k >= 0 and islegal(color, index_to_grid(j+str(pv-k)+str(ph)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv-k][ph] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True
                    gamestate_check = copy.deepcopy(gamestate)
                
                #Down
                for k in range(1,8-pv):
                    if(pv+k <= 7 and islegal(color, index_to_grid(j+str(pv+k)+str(ph)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv+k][ph] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True
                    gamestate_check = copy.deepcopy(gamestate)
                
                #Left
                for k in range(1,ph+1):
                    if(ph-k >= 0 and islegal(color, index_to_grid(j+str(pv)+str(ph-k)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv][ph-k] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True
                    gamestate_check = copy.deepcopy(gamestate)
                    

                #Right
                for k in range(1,8-ph):
                    if(ph+k <= 7 and islegal(color, index_to_grid(j+str(pv)+str(ph+k)), gamestate_check, None, True, False, white_captures, black_captures)):
                        gamestate_check[pv][ph] = "  "
                        gamestate_check[pv][ph+k] = j

                        if(color == "White" and ischeck(gamestate_check, check)[0] != "White" and j[0].upper() == "W"):
                            
                            return True
                        elif(color == "Black" and ischeck(gamestate_check, check)[1] != "Black" and j[0].upper() == "B"):
                            
                            return True
                    gamestate_check = copy.deepcopy(gamestate)
                    
         
            #PAWNS
            #WHITE PAWNS
            if(color == "White"):
                if j in ["W1","W2","W3","W4","W5","W6","W7","W8"]:
                    #Moving pawn forward 1 or 2 squares if pawn hasn't moved
                    if(pv == 6):
                        for k in range(1,3):               
                            if(islegal(color, index_to_grid(j+str(pv-k)+str(ph)), gamestate_check, None, True, False, white_captures, black_captures)):
                               
                                gamestate_check[pv][ph] = "  "
                                gamestate_check[pv-k][ph] = j
                               
                                if(ischeck(gamestate_check, check)[0] != "White"):
                                    
                                    return True

                            gamestate_check = copy.deepcopy(gamestate)
                            
                        #Up and right (attacking)
                        if(pv-1 >= 0 and ph+1 <= 7 and islegal(color, index_to_grid(j+str(pv-1)+str(ph+1)), gamestate_check, None, True, False, white_captures, black_captures)):
                            
                            gamestate_check[pv][ph] = "  "
                            gamestate_check[pv-1][ph+1] = j

                            if(ischeck(gamestate_check, check)[0] != "White"):
                                
                                return True

                            gamestate_check = copy.deepcopy(gamestate)
                            
                        #Up and left (attacking)
                        if(pv-1 >= 0 and ph-1 >= 0 and islegal(color, index_to_grid(j+str(pv-1)+str(ph-1)), gamestate_check, None, True, False, white_captures, black_captures)):

                            gamestate_check[pv][ph] = "  "
                            gamestate_check[pv-1][ph-1] = j

                            if(ischeck(gamestate_check, check)[0] != "White"):
                                
                                return True

                            gamestate_check = copy.deepcopy(gamestate)
                    #If pawn has already moved
                    else:
                        #Moving forward one square
                        if(pv-1 >= 0 and islegal(color, index_to_grid(j+str(pv-1)+str(ph)), gamestate_check, None, True, False, white_captures, black_captures)):

                            gamestate_check[pv][ph] = "  "
                            gamestate_check[pv-1][ph] = j
                           
                            if(ischeck(gamestate_check, check)[0] != "White"):
                                
                                return True

                            gamestate_check = copy.deepcopy(gamestate)
                            
                        #Up and right (attacking)
                        if(pv-1 >= 0 and ph+1 <= 7 and islegal(color, index_to_grid(j+str(pv-1)+str(ph+1)), gamestate_check, None, True, False, white_captures, black_captures)):
                            
                            gamestate_check[pv][ph] = "  "
                            gamestate_check[pv-1][ph+1] = j

                            if(ischeck(gamestate_check, check)[0] != "White"):
                                
                                return True

                            gamestate_check = copy.deepcopy(gamestate)
                            
                        #Up and left (attacking)
                        if(pv-1 >= 0 and ph-1 >= 0 and islegal(color, index_to_grid(j+str(pv-1)+str(ph-1)), gamestate_check, None, True, False, white_captures, black_captures)):

                            gamestate_check[pv][ph] = "  "
                            gamestate_check[pv-1][ph-1] = j

                            if(ischeck(gamestate_check, check)[0] != "White"):
                                
                                return True

                            gamestate_check = copy.deepcopy(gamestate)
            
            #BLACK PAWNS
            elif(color == "Black"):
                if j in ["B1","B2","B3","B4","B5","B6","B7","B8"]:
                    #Moving pawn forward 1 or 2 squares
                    if(pv == 1):
                        for k in range(1,3):
                            
                            if(islegal(color, index_to_grid(j+str(pv+k)+str(ph)), gamestate_check, None, True, False, white_captures, black_captures)):
                                gamestate_check[pv][ph] = "  "
                                gamestate_check[pv+k][ph] = j
                               
                                if(ischeck(gamestate_check, check)[1] != "Black"):
                                    #If the move results in Black no longer being in check, it isn't checkmate
                                    return True

                            gamestate_check = copy.deepcopy(gamestate)
                                
                        #Down and right (attacking)
                        if(pv+1 <= 7 and ph+1 <= 7 and islegal(color, index_to_grid(j+str(pv+1)+str(ph+1)), gamestate_check, None, True, False, white_captures, black_captures)):
                            gamestate_check[pv][ph] = "  "
                            gamestate_check[pv+1][ph+1] = j

                            if(ischeck(gamestate_check, check)[1] != "Black"):
                                return True
                            gamestate_check = copy.deepcopy(gamestate)
                            
                        #Down and left (attacking)
                        if(pv+1 <= 7 and ph-1 >= 0 and islegal(color, index_to_grid(j+str(pv+1)+str(ph-1)), gamestate_check, None, True, False, white_captures, black_captures)):
                            gamestate_check[pv][ph] = "  "
                            gamestate_check[pv+1][ph-1] = j

                            if(ischeck(gamestate_check, check)[1] != "Black"):
                                return True
                            gamestate_check = copy.deepcopy(gamestate)
                    #If pawn has already moved
                    else:
                        #Moving forward one square
                        if(pv+1 <= 7 and islegal(color, index_to_grid(j+str(pv+1)+str(ph)), gamestate_check, None, True, False, white_captures, black_captures)):
                        
                            gamestate_check[pv][ph] = "  "
                            gamestate_check[pv+1][ph] = j
                           
                            if(ischeck(gamestate_check, check)[1] != "Black"):
                                return True
                            gamestate_check = copy.deepcopy(gamestate)
                            
                        #Down and right (attacking)
                        if(pv+1 <= 7 and ph+1 <= 7 and islegal(color, index_to_grid(j+str(pv+1)+str(ph+1)), gamestate_check, None, True, False, white_captures, black_captures)):
                            gamestate_check[pv][ph] = "  "
                            gamestate_check[pv+1][ph+1] = j

                            if(ischeck(gamestate_check, check)[1] != "Black"):
                                return True
                            gamestate_check = copy.deepcopy(gamestate)
                            
                        #Down and left (attacking)
                        if(pv+1 <= 7 and ph-1 >= 0 and islegal(color, index_to_grid(j+str(pv+1)+str(ph-1)), gamestate_check, None, True, False, white_captures, black_captures)):
                            gamestate_check[pv][ph] = "  "
                            gamestate_check[pv+1][ph-1] = j

                            if(ischeck(gamestate_check, check)[1] != "Black"):
                                return True
                            gamestate_check = copy.deepcopy(gamestate)
                        

def index_to_grid(move_index):
    #Convert grid letters/numbers to index numbers
    move_list = list(move_index)
    move_list[3] = str(8-int(move_index[2]))
    
    if(move_index[3] == "0"):
        move_list[2] = "A"
    elif(move_index[3] == "1"):
        move_list[2] = "B"
    elif(move_index[3] == "2"):
        move_list[2] = "C"
    elif(move_index[3] == "3"):
        move_list[2] = "D"
    elif(move_index[3] == "4"):
        move_list[2] = "E"
    elif(move_index[3] == "5"):
        move_list[2] = "F"
    elif(move_index[3] == "6"):
        move_list[2] = "G"
    elif(move_index[3] == "7"):
        move_list[2] = "H"

    return "".join(move_list)

main(white_captures, black_captures)
