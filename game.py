season = [[
    {'game': 1,
     'teams':['West Ham', 'Everton'],
     'result': 1},
    {'game': 2,
     'teams':['Spurs', 'Leicester'],
     'result': 1},
    {'game': 3,
     'teams':['Swansea', 'Stoke'],
     'result': 3}],
[
    {'game': 1,
     'teams':['Man Utd', 'Man City'],
     'result': 3},
    {'game': 2,
     'teams':['Liverpool', 'Brighton'],
     'result': 2},
    {'game': 3,
     'teams':['Chelsea', 'Newcastle'],
     'result': 1}],
[
    {'game': 1,
     'teams':['Athletico', 'Barcelona'],
     'result': 2},
    {'game': 2,
     'teams':['Getafe', 'Betis'],
     'result': 2},
    {'game': 3,
     'teams':['Alaves', 'Espanyol'],
     'result': 1}]]


class Question:
    def __init__(self, home, away, correct):
        self.home = home
        self.away = away
        self.correct = correct

    def fixture(self):
        print(f'{self.home} vs {self.away}')


class Player:
    def __init__(self, name='', score=0, answer=0):
        self.name = name
        self.score = score

    def prediction(self):
        answer = input(f'Enter your prediction {self.name}.. ')
        self.answer = int(answer)

# Function to convert guess to string
def ansConv(guess):
    if guess == 1:
        ansStr = 'Home Win'
    elif guess == 2:
        ansStr = 'Draw'
    else:
        ansStr = 'Away Win'
    return ansStr

def calcWinner(*players):
    #for player in players:
    print('Hi Nicky')


def main():
    players = []
    max_players = 10
    num_players = input('Please enter number of players..')
    num_weeks = int(input('Please enter number of weeks you would like to play..'))
    #Create list of player objects
    for player in range(int(num_players)):
        player = Player(f'Player {player+1}')
        players.append(player)

    print('Enter 1 for a Home Win, 2 for a Draw or 3 for an Away Win')
    print('---------------')
    # wk_num used to calculate week number on gui
    wk_num = 1
    # count used to keep track of current week
    count = 0
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

    #Sort players by score
    players.sort(key=lambda x: x.score, reverse=True)

    for player in players:
        print(f'{player.name} scored {player.score} points.')


main()
