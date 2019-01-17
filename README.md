# Football Quiz

A web App testing a persons knowledge of football results from a season

## Description

The idea was to create a quiz which takes a set of football results from a recent football season, in this case The English Premiership.  The quiz presents each game in a particular week and asks the player to answer whether the game was a home win, away win or a draw.  They get 2 attempts per question, 1 point is received for a correct home win, 2 points for a correct draw, 3 points for a correct away win and 1 point for a correct second attempt.  The game can also be played in 2 player mode with plans to expand to more later.  In the case of a one player game there is a leaderboard which contains the top ten scores.


### Dependencies

* HTML5, CSS3, Python Flask Framework, Bootstrap 4, Javascript, Mlab for Mongodb


## Authors

Alan Smith (solanus@gmail.com)

## Deployed

https://github.com/alsmith808/pools
https://flask-scores.herokuapp.com/


## Run locally
Clone or download git repo
Install latest version of Python 3
Install latest version of flask
Set up your own mlab account and change mlab key in app.py to your own assigned key
Navigate to the root folder of project and open the terminal here
Run the command 'python app.py' to spin up a local server
Open the prompted location in your browser


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
Unit tests available in repo for two main classes and the main game functions
* test_player.py
* test_question.py
* test_game.py


## Testing_Manual
The app was continuosly tested manually in the browser throughout the lifecycle of the project.
It has also been made as responsive as possible and has been tested on various screen sizes and mobiles.


## Version History

* 0.1
    * Initial Release

## License

MIT

## Acknowledgments


* Corey Schaefer (Tutorials on Flask)
https://www.youtube.com/user/Corey Schaefer

* Miguel Grinberg pyCon2015

* Anthony at Pretty Printed
https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ
