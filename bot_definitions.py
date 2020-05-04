import tweepy
import random

class board:
    def __init__(self):
        self.positions = ['_' for x in range(0,9)]
        for x in range (6,9):
            self.positions[x] = ' '


    def position_is_empty(self, pos):
        if pos < 6 and pos >= 0:
            if self.positions[pos] == "_":
                return True
            else:
                return False
        elif pos < 9:
                if self.positions[pos] == " ":
                    return True
                else:
                    return False
        else:
            print("Invalid position entered.\n")
            return True


    def get_board(self):
        theBoard = str("\n" + self.positions[0] + "_|_" + self.positions[1] + "_|_"
        + self.positions[2] + "\n" + self.positions[3] + "_|_" + self.positions[4] + "_|_"
        + self.positions[5] + "\n" + self.positions[6] + "  |  " + self.positions[7] + "  |  "
        + self.positions[8] + "\n")
        return theBoard
        #return '\n'.join(
        #    [self.positions[0].join('_|_'),
        #     self.positions[1].join('_|_'),
        #     self.positions[2].join('\n'),
        #     self.positions[3].join('_|_'),
        #     self.positions[4].join('_|_'),
        #     self.positions[5].join('\n'),
        #     self.positions[6].join(' | '),
        #     self.positions[7].join(' | '),
        #     self.positions[8].join('\n')]
        #)

    def num_differences(self, other_board):
        num_difs = 0
        for posnum, pos in enumerate(self.positions):
            print(f"self.positions[{posnum}]: {pos}\n")
            print(f"other_board.positions[{posnum}]: {other_board.positions[posnum]}\n")
            if pos != other_board.positions[posnum]:
                num_difs += 1
        return num_difs

    def parse_board(self, tweet_text):
        """
        Expected tweet example:
        my move:
        __|___|__
        __|___|__
        X  |     |
        your turn
        @TweetTacToe_bot
        !
        #tweettactoe
        """

        print("attempting to parse...\n")
        print("user's tweet:\n" + tweet_text + "\n")
        other_board = board()
        first_board_line = None
        lines = tweet_text.split('\n')
        for lineno, line in enumerate(lines):
            if 'my move' in line:
                first_board_line = lineno + 1

        if first_board_line is None:
            #return error to user: "my move" not found in tweet.
            print("'my move' not found in tweet.\n")
        else:
            otherpositions = []
            for lineno in range(first_board_line, first_board_line + 3):
                this_line = lines[lineno]
                if '_|_' in this_line:
                    stripped_line = this_line.replace('_|_', '')
                else:
                    stripped_line = this_line.replace('  |  ', '')
                for current_pos in stripped_line:
                    otherpositions.append(current_pos)
            other_board.positions = otherpositions


        print("Game board extracted from user's tweet:\n" +
        other_board.get_board() + "\n")
        numDif = self.num_differences(other_board)
        if numDif < 1:
            print("Error: user did not make a move.\n")
            return -1
        elif numDif > 1:
            print("Error: user made more than one move.\n")
            return 1
        else:
            print("Proper num of moves detected.\n")
            self.positions = other_board.positions #update the current board
            return 0


#end class baord

class game:
    row_combos = [[0,1,2], [3,4,5], [6,7,8]]
    col_combos = [[0,3,6], [1,4,7], [2,5,8]]
    diag_combos = [[0,4,8], [2,4,6]]

    def __init__(self, user):
        self.user = user
        self.x_or_o = random.randint(0,1) #0 = x, 1 = o
        self.first_move = True
        self.tie = False
        self.over = False
        self.winner = ""
        self.the_board = board()
        self.cheat = False
        self.no_move = False

    def update_game(self, tweet_text):
        ret = self.the_board.parse_board(tweet_text)
        if ret  == 1:
            #cheat
            self.cheat = True
            return 1
        elif ret == -1:
            #no move
            self.no_move = True
            return -1
        elif ret == 0:
            return 0

    def check_combo(self, combo):
        x = self.the_board.positions[combo[0]]
        y = self.the_board.positions[combo[1]]
        z = self.the_board.positions[combo[2]]

        if (x == 'x' or x == 'X') and (y == 'x' or y == 'X') \
        and (z == 'x' or z == 'X'):
            if self.x_or_o == 0:
                self.winner = "@TweetTacToe_bot"
            else:
                self.winner = self.user
            return True

        elif (x == 'o' or x == 'O') and (y == 'o' or y == 'O') \
        and (z == 'o' or z == 'O'):
            if self.x_or_o == 1:
                self.winner = "@TweetTacToe_bot"
            else:
                self.winner = self.user
            return True
        else:
            return False

    def check_row_win(self):
        for combo in self.row_combos:
            if (self.the_board.positions[combo[0]] == 'x' \
            or self.the_board.positions[combo[0]] == 'X') \
            and (self.the_board.positions[combo[1]] == 'x' \
            or self.the_board.positions[combo[1]] == 'X') \
            and (self.the_board.positions[combo[2]] == 'x' \
            or self.the_board.positions[combo[2]] == 'X'):
                if self.x_or_o == 0:
                    self.winner = "@TweetTacToe_bot"
                else:
                    self.winner = self.user
                return True
            elif (self.the_board.positions[combo[0]] == 'o' \
            or self.the_board.positions[combo[0]] == 'O') \
            and (self.the_board.positions[combo[1]] == 'o' \
            or self.the_board.positions[combo[1]] == 'O') \
            and (self.the_board.positions[combo[2]] == 'o' \
            or self.the_board.positions[combo[2]] == 'O'):
                if self.x_or_o == 1:
                    self.winner = "@TweetTacToe_bot"
                else:
                    self.winner = self.user
                return True

        return False

    def check_col_win(self):
        for combo in self.col_combos:
            if (self.the_board.positions[combo[0]] == 'x' \
            or self.the_board.positions[combo[0]] == 'X') \
            and (self.the_board.positions[combo[1]] == 'x' \
            or self.the_board.positions[combo[1]] == 'X') \
            and (self.the_board.positions[combo[2]] == 'x' \
            or self.the_board.positions[combo[2]] == 'X'):
                if self.x_or_o == 0:
                    self.winner = "@TweetTacToe_bot"
                else:
                    self.winner = self.user
                return True
            elif (self.the_board.positions[combo[0]] == 'o' \
            or self.the_board.positions[combo[0]] == 'O') \
            and (self.the_board.positions[combo[1]] == 'o' \
            or self.the_board.positions[combo[1]] == 'O') \
            and (self.the_board.positions[combo[2]] == 'o' \
            or self.the_board.positions[combo[2]] == 'O'):
                if self.x_or_o == 1:
                    self.winner = "@TweetTacToe_bot"
                else:
                    self.winner = self.user
                return True

        return False

    def check_diag_win(self):
        for combo in self.diag_combos:
            if (self.the_board.positions[combo[0]] == 'x' \
            or self.the_board.positions[combo[0]] == 'X') \
            and (self.the_board.positions[combo[1]] == 'x' \
            or self.the_board.positions[combo[1]] == 'X') \
            and (self.the_board.positions[combo[2]] == 'x' \
            or self.the_board.positions[combo[2]] == 'X'):
                if self.x_or_o == 0:
                    self.winner = "@TweetTacToe_bot"
                else:
                    self.winner = self.user
                return True
            elif (self.the_board.positions[combo[0]] == 'o' \
            or self.the_board.positions[combo[0]] == 'O') \
            and (self.the_board.positions[combo[1]] == 'o' \
            or self.the_board.positions[combo[1]] == 'O') \
            and (self.the_board.positions[combo[2]] == 'o' \
            or self.the_board.positions[combo[2]] == 'O'):
                if self.x_or_o == 1:
                    self.winner = "@TweetTacToe_bot"
                else:
                    self.winner = self.user
                return True

        return False

    def is_winner(self):
        if self.check_row_win() == True \
        or self.check_col_win() == True \
        or self.check_diag_win() == True:
            return True

        return False

    def get_board(self):
        ret = self.the_board.get_board()
        return ret

    def game_over(self):
        if self.is_winner() == True:
            return True
        for i in range(1,9):
            if self.the_board.position_is_empty(i) == True:
                return False
        self.tie = True
        return True

    def make_move(self):
        rand_pos = random.randint(0, 8)
        while self.the_board.position_is_empty(rand_pos) != True:
            rand_pos = random.randint(0, 8)

        if self.x_or_o == 0:
            self.the_board.set_position(rand_pos, 'X')
        elif self.x_or_o == 1:
            self.the_board.set_position(rand_pos, 'O')
#end class game

def get_reply_tweet(the_game):
    if the_game.game_over() == True:
        if the_game.tie == True:
            reply = str(the_game.get_board() + the_game.user + " It's a tie! Good game!\n#tweettactoe")
        else:
            reply = str(the_game.get_board() + the_game.user + " good game! " + the_game.winner + " is the winner!\n#tweettactoe")
    else:
        if the_game.first_move == True:
            reply = str("copy everything from 'my move' to the end of the "
+ "tweet, make your move, and change the username at the end to @TweetTacToe_bot "
+ "to reply!\nmy move:" + the_game.get_board() + "your turn " + the_game.user + "!\n#tweettactoe")
            the_game.first_move = False
        else:
            if the_game.cheat == True:
                #cheat
                reply = str("You cheated! you can only make one move at a time,"
                + " and can't change any old moves " + the_game.user + "!" +
                "try again!\n#tweettactoe")
                the_game.cheat = False
            elif the_game.no_move == True:
                #nomove
                reply = str(the_game.user + " , you didn't make a move!"
                " Try again!\n#tweettactoe")
                the_game.no_move = False
            else:
                reply = str("my move: " + the_game.get_board() + "your turn " + the_game.user + "!\n#tweettactoe")
    return reply

playing = False
old_id = 1
newGame = None

def check_for_and_play_game(api):
    print("checking recent mentions...\n")
    global playing
    global old_id
    global newGame
    mention_tweets = api.mentions_timeline()
    latest_tweet = mention_tweets[0]
    curr_id = latest_tweet.id


    if old_id != curr_id:
        old_id = curr_id
        if ("let's play!" in latest_tweet.text or \
        "Let's play!" in latest_tweet.text) \
        and "#tweettactoe" in (latest_tweet.text):
            if playing == False:
                print("starting new game...\n")
                newGame = game(str("@" + latest_tweet.user.screen_name))#figure out how to get user
                newGame.make_move()
                playing = True
                print("tweeting move...\n")
                api.update_status(get_reply_tweet(newGame))
            else:
                api.update_status(str("Sorry, " + str("@" + latest_tweet.user.screen_name) +
                ", I'm playing against someone, try again soon!\n#tweettactoe"))

        elif "your turn" in (latest_tweet.text) and \
        "#tweettactoe" in (latest_tweet.text) and playing == True:
            if str("@" + latest_tweet.user.screen_name) == newGame.user:
                print("attempting to update game...\n")
                if newGame.update_game(latest_tweet.text) == 0:
                    if newGame.game_over() == False:
                        newGame.make_move()
                        print("tweeting move...\n")
                        api.update_status(get_reply_tweet(newGame))
                    else:
                        print("tweeting winner...\n")
                        api.update_status(get_reply_tweet(newGame))
                        playing == False
                else:
                    print("tweeting error...\n")
                    api.update_status(get_reply_tweet(newGame))

        else:
            return
