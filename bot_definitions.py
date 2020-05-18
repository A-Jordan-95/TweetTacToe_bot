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
            print("Error: invalid position entered.\n")
            return True


    def get_board(self):
        return str(f"\n{self.positions[0]}_|_{self.positions[1]}_|_"
        f"{self.positions[2]}\n{self.positions[3]}_|_{self.positions[4]}_|_"
        f"{self.positions[5]}\n{self.positions[6]}  |  {self.positions[7]}  |  "
        f"{self.positions[8]}\n")

    def check_move(self, other_board, x_or_o):
        num_difs = 0
        new_pos = 0
        same_game_piece = False
        for posnum, pos in enumerate(self.positions):
            if pos != other_board.positions[posnum]:
                num_difs += 1
                if new_pos == 0:
                    new_pos = posnum
                    if ((other_board.positions[new_pos] == 'x' or \
                    other_board.positions[new_pos] == 'X') and x_or_o == 0) or \
                    ((other_board.positions[new_pos] == 'o' or \
                    other_board.positions[new_pos] == 'O') and x_or_o == 1):
                        same_game_piece = True

        if same_game_piece == True:
            return 2
        if num_difs > 1:
            return 1
        elif num_difs < 1:
            return -1
        elif num_difs == 1:
            return 0


    def parse_board(self, tweet_text, x_or_o):
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
        other_board = board()
        first_board_line = None
        lines = tweet_text.split('\n')
        for lineno, line in enumerate(lines):
            if 'my move' in line:
                first_board_line = lineno + 1

        if first_board_line is None:
            print("'my move' not found in tweet.\n")
            return -2 #unable to read tweet, notify user
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


        print(f"Game board extracted from user's tweet:\n"
        f"{other_board.get_board()}\n")
        moveCheck = self.check_move(other_board, x_or_o)
        if moveCheck < 0:
            #print("Error: user did not make a move.\n")
            return -1
        elif moveCheck > 1:
            #print("Error: user chose same game piece as bot.\n")
            return 2
        elif moveCheck == 1:
            #print("Error: user made more than one move.\n")
            return 1
        elif moveCheck == 0:
            #print("Proper num of moves detected.\n")
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
        self.same_piece = False
        self.my_move_not_found = False

    def update_game(self, tweet_text):
        ret = self.the_board.parse_board(tweet_text, self.x_or_o)
        if ret  == 1:
            #cheat
            self.cheat = True
            return 1
        elif ret == -1:
            #no move
            self.no_move = True
            return -1
        elif ret == 2:
            #same game piece
            self.same_piece = True
            return 2
        elif ret == 0:
            return 0
        elif ret == -2:
            #'my move' not found, unable to parse.
            self.my_move_not_found = True
            return -2

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
            self.the_board.positions[rand_pos] = 'X'
        elif self.x_or_o == 1:
            self.the_board.positions[rand_pos] = 'O'
#end class game

class bot:
    def __init__(self):
        self.playing = False
        self.game = None
        self.last_tweet_id = 1
        self.tweet_tac_toe_not_found = False

    def get_reply_tweet(self):
        if self.game.game_over() == True:
            if self.game.tie == True:
                reply = str(f"{self.game.get_board()} {self.game.user} It's a tie! Good game!\n#tweettactoe")
            else:
                if self.game.user == self.game.winner:
                    reply = str(f"{self.game.get_board()} good game {self.game.winner}! you win!\n#tweettactoe")
                else:
                    reply = str(f"{self.game.get_board()} good game {self.game.user}! I win!\n#tweettactoe")
            self.playing = False
        else:
            if self.game.first_move == True:
                reply = str("copy everything from 'my move' to the end of the "
                "tweet, make your move, and change the username at the end to @TweetTacToe_bot "
                f"to reply!\nmy move:{self.game.get_board()}your turn {self.game.user}!\n#tweettactoe")
                self.game.first_move = False
            elif self.game.cheat == True:
                #cheat
                reply = str("You cheated! you can only make one move at a time,"
                f" and can't change any old moves {self.game.user}!"
                "try again!\n#tweettactoe")
                self.game.cheat = False
            elif self.game.no_move == True:
                #nomove
                reply = str(f"{self.game.user}, you didn't make a move! Try again!\n#tweettactoe")
                self.game.no_move = False
            elif self.game.same_piece == True:
                #same game piece chosen
                if self.game.x_or_o == 0:
                    correctLet = 'O'
                else:
                    correctLet = 'X'
                reply = str(f"{self.game.user}, You chose the same letter as me! try again with {correctLet} instead!\n#tweettactoe")
                self.game.same_piece = False
            elif self.game.my_move_not_found == True:
                reply = str(f"{self.game.user}, you forgot to include 'my move:' as the line before your game board,"
                " so I can't  find the board, please try again.\n#tweettactoe")
                self.game.my_move_not_found = False
            else:
                reply = str(f"my move: {self.game.get_board()} your turn {self.game.user}!\n#tweettactoe")
        return reply



    def check_for_and_play_game(self, api):
        #print("checking recent mentions...\n")
        mention_tweets = api.mentions_timeline()
        if not mention_tweets:
            #prevent crash if there are no tweets
            #mentioning the bot
            print("mention tweets empty\n")
            return
        else:
            latest_tweet = mention_tweets[0]
        curr_tweet_id = latest_tweet.id


        if self.last_tweet_id != curr_tweet_id:
            self.last_tweet_id = curr_tweet_id
            if self.playing == False:
                print("starting new game...\n")
                self.game = game(str(f"@{latest_tweet.user.screen_name}"))
            else:
                api.update_status(str(f"Sorry, @{latest_tweet.user.screen_name}, "
                "I'm playing against someone, try again soon!\n#tweettactoe"))

            if ("let's play" in latest_tweet.text or \
            "Let's play" in latest_tweet.text or \
            "lets play" in latest_tweet.text or \
            "Lets play" in latest_tweet.text) \
            and "#tweettactoe" in latest_tweet.text:
                self.game.make_move()
                self.playing = True
                print("tweeting move...\n")
                api.update_status(self.get_reply_tweet())

            elif "your turn" in (latest_tweet.text) and \
            "#tweettactoe" in (latest_tweet.text) and playing == True:
                if str(f"@{latest_tweet.user.screen_name}") == self.game.user:
                    print("attempting to update game...\n")
                    if self.game.update_game(latest_tweet.text) == 0:
                        if self.game.game_over() == False:
                            self.game.make_move()
                            print("tweeting move...\n")
                            api.update_status(self.get_reply_tweet())
                        else:
                            print("tweeting winner...\n")
                            api.update_status(self.get_reply_tweet())
                            self.playing == False
                    else:
                        print("tweeting error...\n")
                        api.update_status(self.get_reply_tweet())
            elif "#tweettactoe" not in latest_tweet.text:
                print("no hashtag...\n")
                reply = str(f"Sorry {self.game.user}, I'll only play if you include the hashtag: "
                "#tweettactoe in your tweet, try again!")
                api.update_status(reply)
        else:
            return
    #end check_for_and_play_game()
#end class bot
