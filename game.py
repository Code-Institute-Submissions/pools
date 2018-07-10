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
        answer = input('Enter your prediction.. ')
        self.answer = int(answer)

def ansConv(guess):
    if guess == 1:
        ansStr = 'Home Win'
    elif guess == 2:
        ansStr = 'Draw'
    else:
        ansStr = 'Away Win'

    return ansStr


def main():
    players = []
    num_players = input('Please enter number of players..')
    for player in range(int(num_players)):
        #print(f'Player {player +1} created')
        player = Player(f'Player {player+1}')
        players.append(player)
    nicky = Player('Nicky')
    print('Enter 1 for a Home Win, 2 for a Draw or 3 for an Away Win')
    print('---------------')
    for game in week_1:
        num = game['game']
        home = game['teams'][0]
        away = game['teams'][1]
        result = game['result']
        question = Question(home, away, result)
        print(f'Game {num}')
        question.fixture()
        nicky.prediction()
        print(f'The correct answer is {ansConv(question.correct)}')
        print(f'You guessed: {ansConv(nicky.answer)}')
        if nicky.answer == question.correct:
            print('You guessed correct')
            nicky.score += nicky.answer
        else:
            print('Wrong answer')
        print('---------------')

    print(f'You scored {nicky.score}')


main()
