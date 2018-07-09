week_1 = [
    {'game': 1,
     'teams':['West Ham', 'Everton'],
     'result': 1},
    {'game': 2,
     'teams':['Spurs', 'Leicester'],
     'result': 2}]

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
        answer = input('Enter 1 for Home Win, 2 for a Draw and 3 for an Away Win')
        self.answer = int(answer)



def main():
    nicky = Player('Nicky')
    #print('The first fixture is ') + week_1
    for game in week_1:
        question_1 = Question('West Ham', 'Everton', 3)
        question_1.fixture()
        nicky.prediction()
        print(f'The correct answer is {question_1.correct}')
        print(f'You guessed {nicky.answer}')
        if nicky.answer == question_1.correct:
            print('You guessed correct')
            nicky.score += nicky.answer
        else:
            print('wrong answer')

        print(f'Your current score is {nicky.score}')




main()
