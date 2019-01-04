import os
import json
import random


# class Multiplayer:
#     def __init__(self, playerlist):
#
#         self.playerlist = playerlist


multiplayers = []



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
        Player class for creating instance of a player with a name and their scored
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



def create_player_list():
    """
    Function to open txt file containing names, make list of player objects
    """
    with open ('player_Names.txt', 'r') as f:
        list = []
        for name in f:
            player = Player(name)
            list.append(player)
    return list



def get_player_name(list, num):
    name = list[num].name
    return name



def calc_winner(playerA, playerB):
    """
    Function to calculate if there is a winner.  It only needs the top 2 sorted player objects.
    If these 2 scores are equal then its a draw and any remaining players dont matter
    """
    if playerA.score > playerB.score:
        return(f'{playerA.name} is the winner!')
    else:
        return('Game has finished in a draw!')



def add_to_highscores():
    """ read last line of scores.txt and add to highscores array """
    with open('scores.txt', 'r') as f:
        player = {}
        last_line = f.readlines()[-1]
        name, score = last_line.split(':')
        player['name'] = name
        player['score'] = score
        highscores.append(player)



def get_highscores():
    """
    function to extract scores from scores.txt and
    create dictionary of highscore player objects
    """
    highscores = []
    with open('scores.txt', 'r') as f:
        for line in f:
            player = {}
            name, score = line.split(':')
            player['name'] = name
            player['score'] = int(score)
            highscores.append(player)
    return highscores



def get_rand_match_week():
    """
    get random matchweek object from json stripped file, contains 10 fixtures
    """
    randomWeek = 0
    with open('38_week_season_results.json') as f:
        data = json.load(f)
        """ Season is 38 weeks long """
        randomWeek = random.randrange(38)
        """ Select random week from the json """
        matchweek = data['rounds'][16]['matches']

    return matchweek



def create_fixtures(obj):
    """ create fixtures from extracted matchweek """
    gList = []
    for game in obj:
        home = game['team1']['name']
        away = game['team2']['name']
        result = game['result']
        question = Question(home, away, result)
        fixture = question.fixture()
        gameDict = {'fixture': fixture,
                    'result': result}
        gList.append(gameDict)
    return gList



def get_correct_result(num, list):
    currentGame = num-1
    result = list[currentGame]['result']
    return result


def multi(list, id, name):
    list[id].name = name
    print('multi ran')
    return list

    # return list


# def get_multi():



def init_game():
    week = get_rand_match_week()
    fixtures = create_fixtures(week)
    list = fixtures
    print('init game ran')
    return list


def reset_highscores(list):
    del list[:]
