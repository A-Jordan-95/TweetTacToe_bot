import tweepy
import random

class board:
    def __init__(self):
        self.positions = {1: "_", 2: "_", 3: "_", 4: "_", 5: "_",
                          6: "_", 7: " ", 8: " ", 9: " "}

    def position_is_empty(self, pos):
        if pos < 7 and pos > 0:
            if self.positions[pos] == "_":
                return True
            else:
                return False
        elif pos < 10:
                if self.positions[pos] == " ":
                    return True
                else:
                    return False
        else:
            print("Invalid position entered.\n")
            return True


    def get_board(self):
        #"\n__|___|__\n__|___|__\n  |   |  \n"
        theBoard = str("\n" + self.positions[1] + "_|_" + self.positions[2] + "_|_"
        + self.positions[3] + "\n" + self.positions[4] + "_|_" + self.positions[5] + "_|_"
        + self.positions[6] + "\n" + self.positions[7] + " | " + self.positions[8] + " | "
        + self.positions[9] + "\n")
        return theBoard

    def num_differences(self, other_board):
        num_difs = 0
        for i in range(1,9):
            if (self.positions[i] == 'x' or self.positions[i] == 'X') and \
            (other_board.positions[i] != 'x' or other_board.positions[i] != 'X'):
                num_difs += 1
            elif (self.positions[i] == 'o' or self.positions[i] == 'O') and \
            (other_board.positions[i] != 'o' or other_board.positions[i] != 'O'):
                num_difs += 1
            elif (self.positions[i] == '_' or self.positions[i] == ' ') and \
            (other_board.positions[i] != '_' or other_board.positions[i] != ' '):
                num_difs += 1
        return num_difs

    def set_position(self, pos, char):
        if pos > 0 and pos < 10:
            self.positions[pos] = char
        else:
            print("Error, invalid position.\n")

    def parse_board(self, tweet_text):
        other_board = board()
        other_board.set_position(1, tweet_text[9])
        other_board.set_position(2, tweet_text[13])
        other_board.set_position(3, tweet_text[17])
        other_board.set_position(4, tweet_text[19])
        other_board.set_position(5, tweet_text[23])
        other_board.set_position(6, tweet_text[27])
        other_board.set_position(7, tweet_text[29])
        other_board.set_position(8, tweet_text[33])
        other_board.set_position(9, tweet_text[37])
        if self.num_differences(other_board) < 1:
            print("Error: user did not make a move.\n")
            return -1
        elif self.num_differences(other_board) > 1:
            print("Error: user made more than one move.\n")
            return 1
        else:
            print("Proper num of moves detected.\n")
            self.positions = other_board.positions #update the current board
            return 0


#end class baord

class game:
    winning_combos = [[1,2,3], [4,5,6], [7,8,9], [1,4,7], [2,5,8],
    [3,6,9], [1,5,9], [3,5,7]]

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
        if self.the_board.parse_board(tweet_text) == 1:
            pass
        elif self.the_board.parse_board(tweet_text) == -1:
            pass
        elif self.the_board.parse_board(tweet_text) == 0:
            pass 

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

    def is_winner(self):
        for combo in self.winning_combos:
            if self.check_combo(combo) == True:
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
        rand_pos = random.randint(1, 9)
        while self.the_board.position_is_empty(rand_pos) != True:
            rand_pos = random.randint(1, 9)

        if self.x_or_o == 0:
            self.the_board.set_position(rand_pos, 'X')
        elif self.x_or_o == 1:
            self.the_board.set_position(rand_pos, 'O')
#end class game

def get_reply_tweet(the_game):
    if the_game.game_over() == True:
        if the_game.tie == True:
            reply = str(the_game.get_board() + "It's a tie! Good game!\n#tweettactoe")
        else:
            reply = str(the_game.get_board() + "Good game! " + the_game.winner + " is the winner!\n#tweettactoe")
    else:
        if the_game.first_move == True:
            if the_game.cheat == True:
                #cheat
                pass
            elif the_game.no_move = True:
                #nomove
                pass
            else:
                reply = str("copy everything from 'my move' to the end of the "
+ "tweet, make your move, and change the username at the end to @TweetTacToe_bot "
+ "to reply!\nmy move:" + the_game.get_board() + "your turn " + the_game.user + "!\n#tweettactoe")
            the_game.first_move = False
        else:
            if the_game.cheat == True:
                #cheat
                pass
            elif the_game.no_move = True:
                #nomove
                pass
            else:
                reply = str("my move: " + the_game.get_board() + "your turn " + the_game.user + "!\n#tweettactoe")
    return reply

playing = False

def check_for_and_play_game(api):
    global playing
    mention_tweets = api.mentions_timeline()
    curr_id = mention_tweets[0].id
    latest_tweet = mention_tweets[0]

    if old_id != curr_id:
        old_id = curr_id
        if ("let's play!" in latest_tweet.text or \
        "Let's play!" in latest_tweet.text \
        and "#tweettactoe" in latest_tweet.text:
            if playing == False:
                newGame = game(str("@" + latest_tweet.user.screen_name))#figure out how to get user
                newGame.make_move()
                playing = True
                api.update_status(get_reply_tweet(newGame))
            else:
                api.update_status(str("Sorry, " + str("@" + latest_tweet.user.screen_name) +
                ", I'm playing against someone, try again soon!"))

        elif "your turn" in latest_tweet.text and \
        "#tweettactoe" in latest_tweet.text and playing == True:
            if str("@" + latest_tweet.user.screen_name) == newGame.user:
                if newGame.update_game(latest_tweet.text) == 0:
                    if newGame.game_over() == False:
                        newGame.make_move()
                        api.update_status(get_reply_tweet(newGame))
                    else:
                        api.update_status(get_reply_tweet(newGame))
                        playing == False
                else:
                    api.update_status(get_reply_tweet(newGame))

        else:
            return
