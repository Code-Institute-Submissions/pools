# Question class used for creating a question instance containing 2 teams denoted as home and away
# fixture method used for constructing the question
class Question:
    def __init__(self, home, away, result):
        self.home = home
        self.away = away
        self.result = result

    def fixture(self):
        return(f'{self.home} vs {self.away}')

    def res(self):
        return(self.result)


# Player class for creating instance of a player with a name and their scored
# Player can make a prediction of the score of games
class Player:
    def __init__(self, name='', score=0, answer=0):
        self.name = name
        self.score = score

    def prediction(self):
        answer = input(f'Enter your prediction {self.name}.. ')
        self.answer = int(answer)

    def incScore(self, attempt, guess):
        if attempt == 1:
            self.score = self.score + guess
        elif attempt == 2:
            self.score = self.score + 1
        return self.score

    def getName(self):
        return self.name

    def getScore(self):
        return self.score



# Open file class for set up and taerdown of files
class Open_File():
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, traceback):
        self.file.close()



# Function to open txt file containing names, make list of player objects
def createPlayerList():
    with open ('player_Names.txt', 'r') as f:
        list = []
        for name in f:
            player = Player(name)
            list.append(player)
    return list


# Get Player Name
def getPlayerName(list, num):
    name = list[num -1].name
    return name


# Get Player Name List
def getPlayerNameList():
    names = []
    with open('player_Names.txt', 'r') as f:
        for line in f:
            name = line
            names.append(name)
        pName = names
        return pName


# Function to convert guess input to string
def ansConv(guess):
    if guess == 1:
        ansStr = 'Home Win'
    elif guess == 2:
        ansStr = 'Draw'
    else:
        ansStr = 'Away Win'
    return ansStr


def checkAnswer(plrAnswer, correctRes):
    if plrAnswer != correctRes:
        flash(f'Wrong answer {name}, you have one more attempt', 'dark')
        return redirect(url_for('game', id=id, name=name, score=score, attempt=2))
    if plrAnswer == correctRes:
        # flash(f'You are correct {name}', 'success')
        return redirect(url_for('game', id=id+1, name=name, score=score+1, attempt=1))



# Function to calculate if there is a winner.  It only needs the top 2 sorted player objects.
# If these 2 scores are equal then its a draw and any remaining players dont matter
def calcWinner(playerA, playerB):
    if playerA.score > playerB.score:
        #change return to print to function in console
        return(f'{playerA.name} is the winner!')
    else:
        return('Game has finished in a draw!')



def main():
    # initialize empty list to store player objects
    players = []
    max_players = 10
    # Prompt for number of players
    num_players = input('Please enter number of players..')
    # Prompt for number of weeks/length of game
    num_weeks = int(input('Please enter number of weeks you would like to play..'))
    #Create player objects
    for player in range(int(num_players)):
        player = Player(f'Player {player+1}')
        players.append(player)

    print('Enter 1 for a Home Win, 2 for a Draw or 3 for an Away Win')
    print('---------------')
    # wk_num used to calculate week number on gui
    wk_num = 1
    # count used to keep track of current week
    count = 0
    # Traverse season Data Structure to evaluate player input
    for week in season:
        # while loop used to play as many weeks selected by user
        while count < num_weeks:
            for game in week:
                num = game['game']
                home = game['teams'][0]
                away = game['teams'][1]
                result = game['result']
                question = Question(home, away, result)
                print(f'Week {wk_num} Game {num}')
                question.fixture()
                for player in players:
                    player.prediction()
                    #print(f'The correct prediction is {ansConv(question.correct)}')
                    print(f'You guessed: {ansConv(player.answer)}')
                    if player.answer == question.correct:
                        print('Correct prediction!')
                        player.score += player.answer
                    else:
                        print('Incorrect prediction!')
                    print('---------------')
            wk_num += 1
            count += 1

    # Sort players by score
    players.sort(key=lambda x: x.score, reverse=True)

    # Print player leaderboard
    for player in players:
        print(f'{player.name} scored {player.score} points.')
        print('---------------')

    # Use calcWinner function on sorted player list to establish draw or winner
    calcWinner(players[0], players[1])


#main()
