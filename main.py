board = {}
results = [0,0]
games = []
files = ["games-easy", "games-medium", "games-hard", "games-vhard"]

def get_board(g):
   # Inputs each cell's data from "sudoku string"
    for i in range(1, 82):
        value = int(games[g][i - 1])
        board[i] = {}
        if value == 0:
            board[i]["value"] = " "
        else:
            board[i]["value"] = int(value)
        row = (i - 1) // 9
        column = (i - 1) % 9
        y = row // 3
        x = column // 3 + 1
        board[i]["row"] = row
        board[i]["column"] = column
        board[i]["segment"] = y * 3 + x
        board[i]["potential"] = []

def print_board():
    # Simple output
    for i in range(9):
        row = []
        row2 = []
        for item in board:
            if board[item]["row"] == i:
                row.append(board[item]["value"])
                row2.append(board[item]["potential"])
        print("+---+---+---+---+---+---+---+---+---+")
        print("|",row[0],"|",row[1],"|",row[2],"|",row[3],"|",row[4],"|",row[5],"|",row[6],"|",row[7],"|",row[8],"|")
        #print("|",row2[0],"|",row2[1],"|",row2[2],"|",row2[3],"|",row2[4],"|",row2[5],"|",row2[6],"|",row2[7],"|",row2[8],"|")
    print("+---+---+---+---+---+---+---+---+---+")

def get(op, s, c, r):
    # Finds related squares to the given one
    out = []
    for square in board:
        if board[square]["segment"] == board[op]["segment"] and op != square and s == True:
            out.append(square)
        elif board[square]["column"] == board[op]["column"] and op != square and c == True:
            out.append(square)
        elif board[square]["row"] == board[op]["row"] and op != square and r == True:
            out.append(square)
    return out

def generate():
    # Calculate potential values for every square
    for first in board:
        if board[first]["value"] == " ":
            possible = [1,2,3,4,5,6,7,8,9]
            values = get(first, True, True, True)
            for value in values:
                if board[value]["value"] in possible:
                    possible.remove(board[value]["value"])
            board[first]["potential"] = possible

def solve():
    generate()
    # Unique values
    for first in board:
        if board[first]["value"] == " ":
            flags = [
                [True, False, False],
                [False, True, False],
                [False, False, True],
                [True, True, True],
            ]
            for z in range(4):
                unique = [1,2,3,4,5,6,8,9]
                values = get(first, flags[z][0], flags[z][1], flags[z][2])
                for value in values:
                    for i in range(len(board[value]["potential"])):
                        if board[value]["potential"][i] in unique: 
                            unique.remove(board[value]["potential"][i])
                    if board[value]["value"] in unique:
                        unique.remove(board[value]["value"])
                if len(unique) == 1:
                    board[first]["potential"] = unique
    # Pairs
    for first in board:
        if board[first]["value"] == " " and len(board[first]["potential"]) == 2:
            compare = board[first]["potential"]
            values = get(first, True, True, True)
            found = 0
            for value in values:
                if board[value]["potential"] == compare:
                    found = value
            if found != 0:
                a = get(first, True, True, True)
                b = get(found, True, True, True)
                combine = []
                for c in a:
                    if c in b:
                        combine.append(c)
                for item in compare:
                    for value in combine:
                        if item in board[value]["potential"]:
                            board[value]["potential"].remove(item)
    # Set found values
    for first in board:
        if len(board[first]["potential"]) == 1:
            board[first]["value"] = board[first]["potential"][0]
            board[first]["potential"] = []

def adv():
    # Forces the "unsolvable"
    # Afer several failed attempts, taken from:
    # https://en.wikipedia.org/wiki/Sudoku_solving_algorithms
    squares = []
    for first in board:
        if board[first]["value"] == " ":
            squares.append(first)
    count = 0
    while len(squares) != count:
        if board[squares[count]]["value"] == " ":
            lb = 1
        else:
            lb = board[squares[count]]["value"] + 1
        if lb == 10:
            board[squares[count]]["value"] = " "
            count -= 1
        else:
            for i in range(lb,10):
                board[squares[count]]["value"] = i
                values = get(squares[count], True, True, True)
                legal = 0
                for value in values:
                    if board[value]["value"] != board[squares[count]]["value"]:
                        legal += 1
                if legal == len(values):
                    count += 1
                    break
                elif legal != len(values) and i == 9:
                    board[squares[count]]["value"] = " "
                    count -= 1
                #print_board()
                #input(" ")
    if check() == 2:
        return True
    else:
        return False


def check():
    # Check to see if it is/can be solved using the simple method
    tallies = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
    }
    for first in board:
        if board[first]["value"] != " ":
            tallies[board[first]["value"]] += 1
    total = 0
    for i in tallies:
        if tallies[i] < 10:
            total += tallies[i]
    if total == 81:
        return 2
    else:
        results.append(total)
    if total == results[-1] and total == results[-2]:
        return 1
    else:
        return 0

def main():
    # Main loop
    reader()
    print("\n[!] Sudoku Solver - by Hugh Wilson\n")
    # Very basic user interface system to test/showcase
    print("[1] Run stress test of 100-400 boards")
    print("[2] Solve 1 of 400 boards")
    print("[3] Input custom board")
    print("[4] Exit program")
    choice = input("[?] Enter your selection (1-4): ")
    if choice == "4":
        exit()
    elif choice == "1":
        print("[1] Easy boards (100)")
        print("[2] Medium boards (100)")
        print("[3] Hard boards (100)")
        print("[4] Very hard boards (100)")
        print("[5] All boards (400)")
        choice2 = int(input("[?] Enter your selecton (1-5): ")) - 1
        bounds = [[0,100],[100,200],[200,300],[300,400],[0,400]]
        counter = 0
        for i in range(bounds[choice2][0], bounds[choice2][1]):
            get_board(i)
            while check() == 0:
                solve() 
            if check() == 2:
                counter += 1
            else:
                print("[-]", i + 1, "Failed basic solve, moving to advanced.")
                if adv() == False:
                    print("[-]", i + 1, "Failed.")
                else:
                    counter += 1
        print("[+]", counter, "boards solved")
    elif choice == "2":
        choice3 = int(input("[?] Enter a board to solve (1-400): "))
        get_board(choice3 - 1)
        print_board()
        while check() == 0:
            solve()
        if check() == 2:
            print("[+] Success")
        else:
            if adv() == False:
                print("[-] Faliure")
            else:
                print("[+] Success")
        print_board()
    elif choice == "3":
        choice4 = input("[?] Enter board details (0 for a blank): ")
        games = [choice4]
        get_board(0)
        print_board()
        while check() == 0:
            solve()
        if check() == 2:
            print("[+] Success")
        else:
            if adv() == False:
                print("[-] Faliure")
            else:
                print("[+] Success")
        print_board()
        reader()
    else:
        print("[!] Invalid input")

def reader():
    # Reads game file
    for i in range(4):
        file = open(files[i], "r")
        for j in file:
              games.append(j) 

main()
