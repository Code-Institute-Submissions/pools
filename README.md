# Football Quiz

A web App testing a persons knowledge of football results from a season

## Description

The idea was to create a quiz which takes a set of football results from a recent football season, in this case The English Premiership.  The quiz presents each game in a particular week and asks the player to answer whether the game was a home win, away win or a draw.  They get 2 attempts per question, 1 point is received for a correct home win, 2 points for a correct draw, 3 points for a correct away win and 1 point for a correct second attempt.  Up to 5 players can play against each other and the total scores and winner is presented at the end of the game.  In the case of a one player game there is a leaderboard which contains the top ten scores.


### Dependencies

* HTML5, CSS3, Python Flask Framework, Bootstrap 4, Javascript


## Authors

Alan Smith (solanus@gmail.com)

## Deployed

https://github.com/alsmith808/pools

## Run locally
To run the code locally...


## Development
My approach was to first create python classes for player and question and build the game with objects of those classes.  I then created a standalone model of the quiz game in the game.py file.

## Pseudocode...
Click on new games
User inputs number of players between 1 and 5
User/Users input their name as unique identifier
User is presented with Fixture n
User inputs answer with forms
If answer is incorrect player gets second attempts
On correct answer or second wrong answer user goes to next Fixture
If last question in 1 player mode game finishes and score page is shown with option to view leaderboaerd
If multiplayer mode the next player then goes through the questions inputing their answers
When all players have enter answers game finishes, winner/draw screen is presented showing each players score


## Testing_Automated


## Testing_Manual


## Version History

* 0.1
    * Initial Release

## License

MIT

## Acknowledgments


* Corey Schaefer (Tutorials on Flask)
https://www.youtube.com/user/Corey Schaefer

* Miguel Grinberg pyCon2015
