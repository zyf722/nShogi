# nShogi -- Portable shogi program
# Made by MaxAlex
# Powered by MicroPython

# Init
import sys

alphabets = "abcdefghi"

pieces = ([['L', 'l'],
           ['N', 'n'],
           ['S', 's'],
           ['G', 'g'],
           ['K', 'k'],
           ['B', 'b'],
           ['R', 'r'],
           ['P', 'p'],
           ['.', '.']])

board = (
[pieces[0][1], pieces[1][1], pieces[2][1], pieces[3][1], pieces[4][1], pieces[3][1], pieces[2][1], pieces[1][1],
 pieces[0][1]],
[pieces[8][1], pieces[6][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[5][1],
 pieces[8][1]],
[pieces[7][1], pieces[7][1], pieces[7][1], pieces[7][1], pieces[7][1], pieces[7][1], pieces[7][1], pieces[7][1],
 pieces[7][1]],
[pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1],
 pieces[8][1]],
[pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1],
 pieces[8][1]],
[pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1], pieces[8][1],
 pieces[8][1]],
[pieces[7][0], pieces[7][0], pieces[7][0], pieces[7][0], pieces[7][0], pieces[7][0], pieces[7][0], pieces[7][0],
 pieces[7][0]],
[pieces[8][0], pieces[5][0], pieces[8][0], pieces[8][0], pieces[8][0], pieces[8][0], pieces[8][0], pieces[6][0],
 pieces[8][0]],
[pieces[0][0], pieces[1][0], pieces[2][0], pieces[3][0], pieces[4][0], pieces[3][0], pieces[2][0], pieces[1][0],
 pieces[0][0]])

offensive = True
drop = False
last_move_from = ""
last_move_to = ""
move_from = ""
move_to = ""

# Hi Kaku Kin Gin Kei Kyou Fu
# p1 OFF      p2 DEF
p1Piece = [0, 0, 0, 0, 0, 0, 0]
p2Piece = [0, 0, 0, 0, 0, 0, 0]
GetPiece = ["Rr", "Bb", "Gg", "Ss", "Nn", "Ll", "Pp"]


def cls():
    print("\n" * 30)


def invalidmove():
    print("\n" * 13)
    print("                 Invalid Move / Drop! ", end=' ')
    print("\n" * 9)

def dispboard():
    print("        ", end=' ')
    for hori in range(1, 10):
        print(" " + str(10 - hori) + " ", end=' ')
    print("\n         ", end=' ')
    print("----" * 9)
    for x in range(0, 9):
        print("        ", end=' ')
        for y in range(0, 9):
            if ("*" in board[x][y]):
                print(board[x][y] + " ", end=' ')
            else:
                print(" " + board[x][y] + " ", end=' ')
        print("|" + alphabets[x], end=' ')
        print("\n")


def piece_owner(piece):
    # 1 OFF      0 DEF      -1 null
    owner = 1
    if (piece.isupper() == True):
        owner = 1
    elif (piece.islower() == True):
        owner = 0
    else:
        owner = -1
    return owner

def saveboard():
    boardfile = open("nShogi.dat",'w')
    for x in range(0,9):
        for y in range(0,9):
            boardfile.write(board[x][y]+" ")
        boardfile.write("\n")

def loadboard():
    boardfile = open("nShogi.dat",'r')
    line = boardfile.readlines()
    for a in range(0,9):
        boardline = line[a].split()
        for b in range(0,9):
            board[a][b] = boardline[b]
    print(board[a][b])

def num2coord(x, y):
    return (str(9 - x) + alphabets[y])

def coord2num(coord):
    # 0 x      1 y
    retnum = [0, 0]
    try:
        if (coord[0] not in "123456789"):
            retnum = [-1, -1]
            return retnum
        if (coord[1] not in alphabets):
            retnum = [-1, -1]
            return retnum
    except (NameError, IndexError):
        retnum = [-1, -1]
        return retnum
    retnum[1] = 8 - (int(coord[0]) - 1)
    retnum[0] = alphabets.index(coord[1])
    return retnum

def droppiece(dp,mto):
    # 0 x      1 y
    droppiece = dp[1]
    mt = coord2num(mto)
    if (mt == [-1, -1]):
        invalidmove()
        return False
    if (board[mt[0]][mt[1]] != pieces[8][0]):
        invalidmove()
        return False
    if (droppiece not in "RrBbGgSsNnLlPp"):
        invalidmove()
        return False
    if (offensive == True):
        droppiece = droppiece.upper()
    else:
        droppiece = droppiece.lower()
    # Fu
    if (droppiece == "P"):
        if (mt[0] == 0):
            invalidmove()
            return False
        # print("mt:"+str(mt[0])+","+str(mt[1]))
        for a in range(0,9):
            if (board[a][mt[1]] == "P"):
                invalidmove()
                return False
    if (droppiece == "p"):
        if (mt[0] == 8):
            invalidmove()
            return False
        for a in range(0,9):
            if (board[a][mt[1]] == "p"):
                invalidmove()
                return False
    # Kyou
    if (droppiece == "L"):
        if (mt[0] == 0):
            invalidmove()
            return False
    if (droppiece == "l"):
        if (mt[0] == 8):
            invalidmove()
            return False
    # Kei
    if (droppiece == "N"):
        if (mt[0] == 0 or mt[0] == 1):
            invalidmove()
            return False
    if (droppiece == "n"):
        if (mt[0] == 8 or mt[0] == 7):
            invalidmove()
            return False

    if (offensive == True):
        for a in range(0,7):
            if (GetPiece[a].find(droppiece) != -1):
                if (p1Piece[a] > 0):
                    p1Piece[a] = p1Piece[a] - 1
                else:
                    invalidmove()
                    return False
    else:
        for a in range(0,7):
            if (GetPiece[a].find(droppiece) != -1):
                if (p2Piece[a] > 0):
                    p2Piece[a] = p2Piece[a] - 1
                else:
                    invalidmove()
                    return False
    board[mt[0]][mt[1]] = droppiece
    return True

def movepiece(mfrom, mto):
    # 0 x      1 y
    mf = coord2num(mfrom)
    mt = coord2num(mto)
    if (mf == [-1, -1] or mt == [-1, -1]):
        invalidmove()
        return False
    ownerf = piece_owner(board[mf[0]][mf[1]])
    ownert = piece_owner(board[mt[0]][mt[1]])
    # print("("+str(mf[0])+","+str(mf[1])+")")
    # print("("+str(mt[0])+","+str(mf[1])+")")
    if (ownerf == ownert or ownerf == -1 or ownerf == (not offensive) or mf[0] < 0 or mf[0] > 8 or mf[1] < 0 or mf[
        1] > 8 or mt[0] < 0 or mt[0] > 8 or mt[1] < 0 or mt[1] > 8):
        invalidmove()
        return False
    # Fu
    if (board[mf[0]][mf[1]] == "P"):
        if ((mt[1] != mf[1]) or (mt[0] != mf[0] - 1)):
            invalidmove()
            return False
    if (board[mf[0]][mf[1]] == "p"):
        if ((mt[1] != mf[1]) or (mt[0] != mf[0] + 1)):
            invalidmove()
            return False
    # Kyou
    if (board[mf[0]][mf[1]] == "L"):
        if ((mt[1] != mf[1]) or (mt[0] > mf[0])):
            invalidmove()
            return False
        for a in range(min(mt[0], mf[0]) + 1, max(mt[0], mf[0])):
            if (board[a][mt[1]] != pieces[8][0]):
                invalidmove()
                return False
    if (board[mf[0]][mf[1]] == "l"):
        if ((mt[1] != mf[1]) or (mt[0] < mf[0])):
            invalidmove()
            return False
        for a in range(min(mt[0], mf[0]) + 1, max(mt[0], mf[0])):
            if (board[a][mt[1]] != pieces[8][0]):
                invalidmove()
                return False
    # Ou / Gyo
    if (board[mf[0]][mf[1]] == "K" or board[mf[0]][mf[1]] == "k"):
        if ((mt[0] >= mf[0] + 2) or (mt[0] <= mf[0] - 2) or (mt[1] >= mf[1] + 2) or (mt[1] <= mf[1] - 2)):
            invalidmove()
            return False
    # Hi
    if (board[mf[0]][mf[1]] == "R" or board[mf[0]][mf[1]] == "r"):
        if ((mt[1] != mf[1]) and (mt[0] != mf[0])):
            invalidmove()
            return False
        if (mt[0] == mf[0]):
            for a in range(min(mt[1], mf[1]) + 1, max(mt[1], mf[1])):
                if (board[mt[0]][a] != pieces[8][0]):
                    invalidmove()
                    return False
        if (mt[1] == mf[1]):
            for a in range(min(mt[0], mf[0]) + 1, max(mt[0], mf[0])):
                if (board[a][mt[1]] != pieces[8][0]):
                    invalidmove()
                    return False
    # Kaku
    if (board[mf[0]][mf[1]] == "B" or board[mf[0]][mf[1]] == "b"):
        if ((mt[1] == mf[1]) or (mt[0] == mf[0])):
            invalidmove()
            return False
        if (abs(mt[0] - mf[0]) != abs(mt[1] - mf[1])):
            invalidmove()
            return False
        # print(str(abs(mt[0] - mf[0]) + 2))
        if (mt[1] > mf[1] and mt[0] < mf[0]):
            # print("right-up")
            for a in range(1, abs(mt[0] - mf[0]) + 1):
                if (board[mf[0] - a][mf[1] + a] != pieces[8][0]):
                    invalidmove()
                    return False
        if (mt[1] > mf[1] and mt[0] > mf[0]):
            # print("right-down")
            for a in range(1, abs(mt[0] - mf[0]) + 1):
                if (board[mf[0] + a][mf[1] + a] != pieces[8][0]):
                    invalidmove()
                    return False
        if (mt[1] < mf[1] and mt[0] > mf[0]):
            # print("left-down")
            for a in range(1, abs(mt[0] - mf[0]) + 1):
                if (board[mf[0] + a][mf[1] - a] != pieces[8][0]):
                    invalidmove()
                    return False
        if (mt[1] < mf[1] and mt[0] < mf[0]):
            # print("left-up")
            for a in range(1, abs(mt[0] - mf[0]) + 1):
                if (board[mf[0] - a][mf[1] - a] != pieces[8][0]):
                    invalidmove()
                    return False
    # Kin and Promoted Pieces
    if (board[mf[0]][mf[1]] == "G" or board[mf[0]][mf[1]] == "*P" or board[mf[0]][mf[1]] == "*L" or board[mf[0]][
        mf[1]] == "*N" or board[mf[0]][mf[1]] == "*S"):
        if (((mt[0] >= mf[0] + 2) or (mt[0] <= mf[0] - 2) or (mt[1] >= mf[1] + 2) or (mt[1] <= mf[1] - 2)) or (
                (mt[0] == mf[0] + 1 and mt[1] == mf[1] + 1) or (mt[0] == mf[0] + 1 and mt[1] == mf[1] - 1))):
            invalidmove()
            return False
    if (board[mf[0]][mf[1]] == "g" or board[mf[0]][mf[1]] == "*p" or board[mf[0]][mf[1]] == "*l" or board[mf[0]][
        mf[1]] == "*n" or board[mf[0]][mf[1]] == "*s"):
        if (((mt[0] >= mf[0] + 2) or (mt[0] <= mf[0] - 2) or (mt[1] >= mf[1] + 2) or (mt[1] <= mf[1] - 2)) or (
                (mt[0] == mf[0] - 1 and mt[1] == mf[1] + 1) or (mt[0] == mf[0] - 1 and mt[1] == mf[1] - 1))):
            invalidmove()
            return False
    # Gin
    if (board[mf[0]][mf[1]] == "S"):
        if (((mt[0] >= mf[0] + 2) or (mt[0] <= mf[0] - 2) or (mt[1] >= mf[1] + 2) or (mt[1] <= mf[1] - 2)) or (
                (mt[0] == mf[0]) or (mt[0] == mf[0] + 1 and mt[1] == mf[1]))):
            invalidmove()
            return False
    if (board[mf[0]][mf[1]] == "s"):
        if (((mt[0] >= mf[0] + 2) or (mt[0] <= mf[0] - 2) or (mt[1] >= mf[1] + 2) or (mt[1] <= mf[1] - 2)) or (
                (mt[0] == mf[0]) or (mt[0] == mf[0] - 1 and mt[1] == mf[1]))):
            invalidmove()
            return False
    # Kei
    if (board[mf[0]][mf[1]] == "N"):
        if (mt[0] != mf[0] - 2):
            invalidmove()
            return False
        else:
            if (mt[1] != mf[1] + 1 and mt[1] != mf[1] - 1):
                invalidmove()
                return False
    if (board[mf[0]][mf[1]] == "n"):
        if (mt[0] != mf[0] + 2):
            invalidmove()
            return False
        else:
            if (mt[1] != mf[1] + 1 and mt[1] != mf[1] - 1):
                invalidmove()
                return False
    # Ryu
    if (board[mf[0]][mf[1]] == "*R" or board[mf[0]][mf[1]] == "*r"):
        if ((mt[1] != mf[1]) and (mt[0] != mf[0])):
            if ((mt[0] >= mf[0] + 2) or (mt[0] <= mf[0] - 2) or (mt[1] >= mf[1] + 2) or (mt[1] <= mf[1] - 2)):
                invalidmove()
                return False
        if (mt[0] == mf[0]):
            for a in range(min(mt[1], mf[1]) + 1, max(mt[1], mf[1])):
                if (board[mt[0]][a] != pieces[8][0]):
                    invalidmove()
                    return False
        if (mt[1] == mf[1]):
            for a in range(min(mt[0], mf[0]) + 1, max(mt[0], mf[0])):
                if (board[a][mt[1]] != pieces[8][0]):
                    invalidmove()
                    return False
    # Uma
    if (board[mf[0]][mf[1]] == "*B" or board[mf[0]][mf[1]] == "*b"):
        skip = False
        if (mt[1] == mf[1]):
            if (abs(mt[0] - mf[0]) >= 2):
                invalidmove()
                return False
            else:
                skip = True

        if (skip == False):
            if (mt[0] == mf[0]):
                if (abs(mt[1] - mf[1]) >= 2):
                    invalidmove()
                    return False
                else:
                    board[mt[0]][mt[1]] = board[mf[0]][mf[1]]
                    board[mf[0]][mf[1]] = pieces[8][0]
                    return True
            if (abs(mt[0] - mf[0]) != abs(mt[1] - mf[1])):
                invalidmove()
                return False
            # print(str(abs(mt[0] - mf[0]) + 2))
            if (mt[1] > mf[1] and mt[0] < mf[0]):
                # print("right-up")
                for a in range(1, abs(mt[0] - mf[0]) + 1):
                    if (board[mf[0] - a][mf[1] + a] != pieces[8][0]):
                        invalidmove()
                        return False
            if (mt[1] > mf[1] and mt[0] > mf[0]):
                # print("right-down")
                for a in range(1, abs(mt[0] - mf[0]) + 1):
                    if (board[mf[0] + a][mf[1] + a] != pieces[8][0]):
                        invalidmove()
                        return False
            if (mt[1] < mf[1] and mt[0] > mf[0]):
                # print("left-down")
                for a in range(1, abs(mt[0] - mf[0]) + 1):
                    if (board[mf[0] + a][mf[1] - a] != pieces[8][0]):
                        invalidmove()
                        return False
            if (mt[1] < mf[1] and mt[0] < mf[0]):
                # print("left-up")
                for a in range(1, abs(mt[0] - mf[0]) + 1):
                    if (board[mf[0] - a][mf[1] - a] != pieces[8][0]):
                        invalidmove()
                        return False

    # print("mf:"+str(mf[0])+","+str(mf[1]))
    # print("mt:"+str(mt[0])+","+str(mt[1]))
    # print("ownerf:"+str(ownerf)+",ownert:"+str(ownert))

    # Get Pieces
    if (ownert != -1):
        for a in range(0, 7):
            if ("*" in board[mt[0]][mt[1]]):
                tmpstr = board[mt[0]][mt[1]][1]
            else:
                tmpstr = board[mt[0]][mt[1]]
            if (GetPiece[a].find(tmpstr) != -1):
                if (ownerf == 1):
                    p1Piece[a] = p1Piece[a] + 1
                elif (ownerf == 0):
                    p2Piece[a] = p2Piece[a] + 1
            elif (tmpstr == "K"):
                print("\n" * 13)
                print("          P1 Loses and P2 Wins")
                sys.exit()
            elif (tmpstr == "k"):
                print("\n" * 13)
                print("          P2 Loses and P1 Wins")
                sys.exit()

    # Move    
    board[mt[0]][mt[1]] = board[mf[0]][mf[1]]
    board[mf[0]][mf[1]] = pieces[8][0]

    # Promote
    if (ownerf == 1 and (mt[0] >= 0 and mt[0] <= 2) and ("*" not in board[mt[0]][mt[1]])):
        if (mt[0] == 0 and (board[mt[0]][mt[1]] == "L" or board[mt[0]][mt[1]] == "P")):
            board[mt[0]][mt[1]] = "*" + board[mt[0]][mt[1]]
        elif (0 <= mt[0] <= 1 and board[mt[0]][mt[1]] == "N"):
            board[mt[0]][mt[1]] = "*" + board[mt[0]][mt[1]]
        else:
            pm = int(input("          Now  Move: Promote?(1 - Yes) "))
            if (pm == 1):
                board[mt[0]][mt[1]] = "*" + board[mt[0]][mt[1]]

    if (ownerf == 0 and (mt[0] >= 6 and mt[0] <= 8) and ("*" not in board[mt[0]][mt[1]])):
        if (mt[0] == 8 and (board[mt[0]][mt[1]] == "l" or board[mt[0]][mt[1]] == "p")):
            board[mt[0]][mt[1]] = "*" + board[mt[0]][mt[1]]
        elif (7 <= mt[0] <= 8 and board[mt[0]][mt[1]] == "n"):
            board[mt[0]][mt[1]] = "*" + board[mt[0]][mt[1]]
        else:
            pm = int(input("          Now  Move: Promote?(1 - Yes) "))
            if (pm == 1):
                board[mt[0]][mt[1]] = "*" + board[mt[0]][mt[1]]

    return True


print("\n" * 13)
print("             nShogi - Shogi for Nspire ", end=' ')
tmp = input()
print("\n" * 9)

while 1:
    print("\n")
    dispboard()

    print("          P1:", end=' ')
    for a in range(0, 7):
        print(GetPiece[a][0] + "*" + str(p1Piece[a]) + " ", end=' ')
    print("")

    print("          P2:", end=' ')
    for a in range(0, 7):
        print(GetPiece[a][0] + "*" + str(p2Piece[a]) + " ", end=' ')
    print("")

    print("")
    if ((last_move_from != "" or last_move_to != "" ) and drop != True):
        print("          Last Move: From " + last_move_from + " To " + last_move_to)
    elif (drop == True):
        print("          Last Move: Drop " + last_move_from + " To " + last_move_to)
    else:

        print("          Last Move: None")
    move_from = input("          Now  Move: From / Drop ")
    move_to = input("          Now  Move: To ")
    if (move_from[0] == "D" or move_from[0] == "d"):
        if (droppiece(move_from, move_to) == True):
            offensive = (not offensive)
            last_move_from = move_from
            last_move_to = move_to
            cls()
    elif (move_from == "save"):
        saveboard()
        sys.exit()
    elif (move_from == "load"):
        loadboard()
        cls()
    else:
        if (movepiece(move_from, move_to) == True):
            offensive = (not offensive)
            last_move_from = move_from
            last_move_to = move_to
            cls()
