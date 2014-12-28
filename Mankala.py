import random, time, re

def get_index(player):
    if 1 in player.holes:
        return 0
    else:
        return 1

def is_same(arg1, arg2):
    if arg1 == arg2:
        return 1
    else:
        return -1

def get_hole(letter):
    abc = 'abcdef ghijkl'
    for index in range(len(abc)):
        if abc[index] == letter:
            return index
    return "None"

def delay(secs):
    start = time.clock()
    while time.clock() - secs < start:
        continue

class Player(object):
    def __init__(self, player):
        if player == 1:
            self.holes = [x for x in range(6)]
            self.bank = 6
        else:
            self.holes = [x for x in range(7,13)]
            self.bank = 13
        self.name = raw_input("Player" + str(player) +"'s name: ")
        com = raw_input("If you want the computer to play" + \
                        "this player type '1' or 'com' or 'yes': ")
        if com in ["1", "yes", "YES", "Yes", "COM", "com", "Com"]:
            self.com = True
            while True:
                try:
                    self.wisdom = int(raw_input("wisdom - depth of thinking" +\
                                                " (in moves): "))
                    break
                except:
                    print "Try again"  
        else:
            self.com = False

    def decide(self):
        choice = raw_input("It's " + self.name + "'s turn. choose a hole: ")
        hole = get_hole(choice)
        if hole in self.holes:
            return hole
        else:
            print "Impossible move"
            return self.decide()

class Board(object):
    def build(self, num):
        self.board = [num for x in range(14)]
        self.board[6] = 0
        self.board[13] = 0

    def score(self):
        diff = self.board[6] - self.board[13]
        return (diff, -diff)

    def check_winner(self):
        for hole in range(14):
            if hole not in [6, 13] and self.board[hole] > 0:
                return "None"
        winner = self.board[6] - self.board[13]
        if winner > 0:
            return 1
        elif winner < 0:
            return 2
        else:
            return "Tie"
        
    def check_lgl_moves(self, player):
        moves = []
        for hole in player.holes:
            if self.is_legal_move(hole, player):
                moves.append(hole)
        return moves
    
    def is_legal_move(self, hole, player):
        if hole in player.holes and self.board[hole] > 0:
            return True
        return False

    def make_board(self, hole, player):
    # to avoid changes in the  real game's board while...
    #... computer is calculating next moves
        new_board = Board()
        new_board.board = [self.board[i] for i in range(14)]
        turn = new_board.move(hole, player, False)
        return (new_board, turn)
        
    def move(self, hole, player, to_print):
    # 'to_print' role is to avoid printing the board while...
    #... computer calculating next moves.
        stones = self.board[hole]
        cur_hole = hole
        while stones > 0:
            if to_print:
                self.print_board()
                delay(0.8)
            cur_hole += 1
            if cur_hole == player.opp.bank:
                cur_hole += 1
            if cur_hole == 14:
                cur_hole = 0
            self.board[cur_hole] += 1
            self.board[hole] -= 1
            stones -= 1
            if stones == 0:
                if to_print:
                    self.print_board()
                    delay(0.8)
                if cur_hole in player.holes and self.board[cur_hole] == 1 \
                   and self.board[12 - cur_hole] > 0:
                # Mankala's rule #1: if your last stone landed on an empty...
                #... hole while the hole against him is not emtpy, all of the...
                #... stones in both holes go to your bank
                    self.board[player.bank] += self.board[12 - cur_hole] + 1
                    self.board[12 - cur_hole] = 0
                    self.board[cur_hole] = 0
                    if to_print:
                        self.print_board()
                        delay(0.8)
                blank = self.check_blank(player)
                # Mankala's rule #2: if all of your holes are empty, the game...
                # ... is over and all of the stones from your opponent holes...
                #... go to your bank
                if blank != None:
                    for hole in blank.opp.holes:
                        add = self.board[hole]
                        self.board[blank.bank] += add
                        self.board[hole] = 0
                        if to_print and add > 0:
                            self.print_board()
                            delay(0.8)
                    return "End"
                # Mankala's rule #3: if your last stone landed on your bank:...
                #... you've earned another turn
                if cur_hole == player.bank:
                    return "Again"
        return "Next"

    def check_blank(self, player, first = True):
        blank = player
        for hole in blank.holes:
            if self.board[hole] > 0:
                if first:
                    return self.check_blank(player.opp, False)
                blank = None
                break
        return blank
    
    def print_inst(self):
        abc = 'abcdefghijklmn'
        print "Holes' names:"
        print "      f  e  d  c  b  a"
        print "bank1 \t\t       bank2"
        print "      g  h  i  j  k  l"
        print
        
    def print_board(self):
        print
        print "Board:"
        line = "      "
        for hole in range(5, -1, -1):
            line += str(self.board[hole]) + " "
            if len(str(self.board[hole])) == 1:
                line += " "
        print line
        line = "   " + str(self.board[6]) + "                  "
        if len(str(self.board[6])) == 1:
            line += " "
        line += str(self.board[13])
        print line
        line = "      "
        for hole in range(7,13):
            line += str(self.board[hole]) + " "
            if len(str(self.board[hole])) == 1:
                line += " "
        print line
        print
            

class ComMove(object):
    def __init__(self, base, turn, board, level, top_level):
        self.base = base
        self.board = board
        self.player2 = self.base.opp
        self.turn = turn
        self.level = level
        self.top_level = top_level
        self.options = self.board.check_lgl_moves(turn)
        self.best = self.get_best()

    def get_best(self):
        if self.level == self.top_level: # com reached max depth of thinking
            score = self.board.score()[get_index(self.base)]
            # for computer prefer continue playing for loosing for sure:
            winner = self.board.check_winner()
            if winner in [0,1]:
                score += 72 * is_same(winner - 1, get_index(self.base))
            # the priorities for best choice are: score(main)...
            # ... and turn (secondary)
            return (score, self.get_turn_val(winner))
        best = None
        for hole in self.options:
            move = self.board.make_board(hole, self.turn)
            if move[1] == "Next":
                next_turn = self.turn.opp
            else:
                next_turn = self.turn
            score = ComMove(self.base, next_turn, move[0],\
                            self.level + 1, self.top_level).best
            sign = self.get_min_plus()
            # 'sign' determines if the node returns the best option for...
            # ... computer or the worst one (if it's his oppenent turn)
            if self.level > 0:
                if best == None or score[0] * sign > best[0] * sign:
                    best = score
                elif best[0] == score[0] and best[1] * sign < score[1] * sign:
                    best = score
            else:
            #for level 0 the function returns a list of best values to allow...
            #...the computer to choose randomly between moves with same resluts            
                if best == None or best[0][0][0] * sign < score[0] * sign:
                    best = [(score, hole)]
                elif best[0][0][0] == score[0]:
                    if best[0][0][1] * sign < score[1] * sign:
                        best = [(score, hole)]
                    elif best[0][0][1] == score[1]:
                        best.append((score,hole))
        if best == None:
            score = self.board.score()[get_index(self.base)]
            # for computer prefer continue playing for loosing for sure:
            winner = self.board.check_winner()
            if winner in [0,1]:
                score += 72  * is_same(winner - 1, get_index(self.base)) 
            #
            best = (score, 1)
        return best

    def get_min_plus(self):
        if self.base == self.turn:
            return 1
        else:
            return -1

    def get_turn_val(self, winner):
        if winner != "None":
            return 1
        if self.turn == self.base:
            return 2
        else:
            return 0
           
class Game(object):
    def __init__(self):
        self.board = Board()
        self.stone_num = self.get_stone_num()
        self.board.build(self.stone_num)
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.player1.opp = self.player2
        self.player2.opp = self.player1
        self.turn = self.player1

    def get_stone_num(self):
        num = raw_input("Choose the number of stones in every hole (3-6): ")
        if num in ["3", "4", "5", "6"]:
            return int(num)
        print "Try again"
        return self.get_stone_num()

    def player_move(self):
        self.board.print_inst()
        move = self.turn.decide()
        if self.board.is_legal_move(move, self.turn):
            turn = self.board.move(move, self.turn, True)
            if turn == "Again":
                print "You've earned another turn"
                delay(1)
                self.player_move()
        else:
            print "Impossible move"
            self.player_move()

    def com_move(self):
        options = ComMove(self.turn, self.turn, self.board, 0, self.turn.wisdom).best
        print options
        choice = random.choice(options)[1]
        abc = 'abcdef ghijkl'
        print self.turn.name + " decided to move with hole '" + abc[choice]\
                                                                      + "'"
        delay(2)
        turn = self.board.move(choice, self.turn, True)
        if turn == "Again":
            print "The computer has earned another turn"
            delay(1)
            self.com_move()
        
    def declare(self):
        if self.board.check_winner() == 1:
            print self.player1.name + " Won!"
        elif self.board.check_winner() == 2:
            print self.player2.name + " Won!"
        else:
            print "It's a tie..."

    def start(self):
        self.board.print_board()
        while self.board.check_winner() == "None":
            if self.turn.com:
                self.board.print_inst()
                delay(1)
                print "Computer's turn, thinking..."
                delay(1)
                self.com_move()
                delay(1)
            else:
                self.player_move()
            self.turn = self.turn.opp
        self.declare()

game1 = Game()
game1.start()
        
