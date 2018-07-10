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
     'result': 1}]]

week_1 = [
    {'game': 1,
     'teams':['West Ham', 'Everton'],
     'result': 1},
    {'game': 2,
     'teams':['Spurs', 'Leicester'],
     'result': 1},
    {'game': 3,
     'teams':['Swansea', 'Stoke'],
     'result': 3}]

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
    num_players = input('Please enter number of players..')
    #Create list of player objects
    for player in range(int(num_players)):
        player = Player(f'Player {player+1}')
        players.append(player)

    print('Enter 1 for a Home Win, 2 for a Draw or 3 for an Away Win')
    print('---------------')
    wk_count = 1
    for week in season:
        for game in week:
            num = game['game']
            home = game['teams'][0]
            away = game['teams'][1]
            result = game['result']
            question = Question(home, away, result)
            print(f'Week {wk_count} Game {num}')
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
        wk_count += 1

    players.sort(key=lambda x: x.score, reverse=True)

    for player in players:
        print(f'{player.name} scored {player.score} points.')


main()
