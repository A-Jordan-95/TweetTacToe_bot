# TweetTacToe_bot
Twitter API app that plays tic tac toe with twitter users who tweet @TweetTacToe_bot "let's play! #tweettactoe".
version one will allow one other user to play with the bot at a time, pulling the next user from the top of the
list of recent mentions. Version one also uses random placement for it's moves, it does not implement a game
strategy to attempt to win every time. Hopefully that will come in a later version.

To do:
-error checking for user choosing same letter as bot.
-use MySQL to save game state of each user's game.
    -maybe keep stats about past games to tell users?
