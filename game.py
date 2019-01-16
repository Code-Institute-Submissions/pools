import os
import json
import random


class Question:
    def __init__(self, home, away, result):
        """
        Question class used for creating a question instance containing
        2 teams denoted as home and away
        """
        self.home = home
        self.away = away
        self.result = result

    def fixture(self):
        """
        fixture method used for constructing the question
        """
        return(f'{self.home} vs {self.away}')

    def res(self):
        return(self.result)



class Player:
    def __init__(self, name='', score=0, answer=0):
        """
        Player class for creating instance of a player with a name and their score
        """
        self.name = name
        self.score = score

    def prediction(self):
        """
        Player can make a prediction of the score of games
        """
        answer = input(f'Enter your prediction {self.name}.. ')
        self.answer = int(answer)

    def inc_score(self, attempt, guess):
        if attempt == 1:
            self.score = self.score + guess
        elif attempt == 2:
            self.score = self.score + 1
        return self.score

    def set_name(self, nm):
        self.name = nm

    def set_score(self, sc):
        self.score = sc

    def get_name(self):
        return self.name

    def get_score(self):
        return self.score




class Open_File():
    def __init__(self, filename, mode):
        """
        Open file class for set up and taerdown of files
        """
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, traceback):
        self.file.close()




def calc_winner(playerA, playerB):
    """
    Function to calculate if there is a winner.  It only needs the top 2 sorted player objects.
    If these 2 scores are equal then its a draw and any remaining players dont matter
    """
    if playerA.score > playerB.score:
        return(f'{playerA.name} is the winner!')
    elif playerB.score > playerA.score:
        return(f'{playerB.name} is the winner!')
    else:
        return('Game has finished in a draw!')




def get_scores(store):
    """
    function to extract scores from mongo db and
    create dictionary of highscore player objects
    """
    scores = []
    scores_table = store.db.scores_table
    all_scores = scores_table.find()
    for record in all_scores:
        player = {}
        name = record['name']
        score = record['score']
        player['name'] = name
        player['score'] = int(score)
        scores.append(player)
    return scores




def get_rand_match_week(num):
    """
    get random matchweek object from json season, contains 10 fixtures
    """
    randomWeek = 0
    with open('38_week_season_results.json') as f:
        data = json.load(f)
        """ Season is 38 weeks long """
        randomWeek = random.randrange(38)
        """ Select random week from the json """
        matchweek = data['rounds'][num]['matches']

    return matchweek




def create_fixtures(list):
    """ create fixtures from extracted matchweek """
    game_list = []
    for game in list:
        home = game['team1']['name']
        away = game['team2']['name']
        result = game['result']
        question = Question(home, away, result)
        fixture = question.fixture()
        game_obj = {'fixture': fixture,
                    'result': result}
        game_list.append(game_obj)
    return game_list




def get_correct_result(num, list):
    currentGame = num-1
    result = list[currentGame]['result']
    return result




def init_game(num):
    week = get_rand_match_week(num)
    fixtures = create_fixtures(week)
    list = fixtures
    print('init game ran')
    return list
