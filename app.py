import os, json, random
from flask import Flask, render_template, url_for, flash, redirect
from forms import PlayerNumForm, NameForm, AnswerForm
from game import Question, Player, calcWinner, createPlayerList, getPlayerName, getPlayerNameList


app = Flask(__name__)

app.config['SECRET_KEY'] = 'nusmmirhdl4472'


# player objects
# multiplayers = []
# player scores dictionary
highscores = []
sortedArray = []
topTen = []


def resetHighscores():
    del highscores[:]


def initFixtures(f):
    f = []


#read last line of scores.txt and add to highscores array
def addToHighscores():
    with open('scores.txt', 'r') as f:
        player = {}
        last_line = f.readlines()[-1]
        name, score = last_line.split(':')
        player['name'] = name
        player['score'] = score
        highscores.append(player)


#function to extract scores from scores.txt and create dictionary of highscore player objects
def getHighscores():
    with open('scores.txt', 'r') as f:
        for line in f:
            player = {}
            name, score = line.split(':')
            player['name'] = name
            player['score'] = int(score)
            highscores.append(player)


# create fixtures manually for the game questions
# def getFixtures():
#     for game in games:
#         home = game['teams'][0]
#         away = game['teams'][1]
#         result = game['result']
#         question = Question(home, away, result)
#         fixture = question.fixture()
#         res = question.res()
#         fixList.append(fixture)
#         results.append(res)


# get random matchweek object from json stripped file, contains 10 fixtures
def getRandMatchWeek():
    with open('2015_stripped.json') as f:
        data = json.load(f)
        # There are 38 fixture weeks in the season
        randomWeek = random.randrange(38)
        # Select random week from the json data
        matchweek = data['rounds'][0]['matches']
    return matchweek


# create fixtures from extracted matchweek
def createFixtures(obj):
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


def getCorrectResult(num):
    currentGame = num-1
    result = fixList[currentGame]['result']
    return result


def initGame():
    week = getRandMatchWeek()
    fixtures = createFixtures(week)
    list = fixtures
    print('initgame ran')
    return list



fixList = initGame()
print(fixList)
multiplayers = createPlayerList()



getHighscores()
sortedHighscores = sorted(highscores, key=lambda item: int(item['score']), reverse=True)
topTen = sortedHighscores[0:10]


multiplayers = createPlayerList()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/newgame", methods=['GET', 'POST'])
def newgame():
    # del fixList[:]
    with open('player_Names.txt', 'r+') as f:
        f.truncate(0)
    form = PlayerNumForm()
    if form.validate_on_submit():
        numPlayers = int(form.players.data)
        flash(f'{numPlayers} player game created!', 'dark')
        return redirect(url_for('enternames', id=1, numPlayers=numPlayers))
    return render_template('newgame.html', title='newgame', form=form )



@app.route("/enternames/<int:id>/<int:numPlayers>", methods=['GET', 'POST'])
def enternames(id, numPlayers):
    form = NameForm()
    if form.validate_on_submit():
        name = form.playername.data
        with open('player_Names.txt', 'a') as f:
            name = name
            f.write(f'{name}\n')
        flash(f'Good luck {name}!! ', 'dark')
        if numPlayers == 1:
            return redirect(url_for('game', id=1, name=name, score=0, attempt=1))
        elif id < numPlayers:
            return redirect(url_for('enternames', id=id+1, numPlayers=numPlayers))
        elif id == numPlayers:
            # createPlayerList()
            return redirect(url_for('multiplayer', id=1, pNum=1, attempt=1))
    return render_template('enternames.html', form=form, id=id, numPlayers=numPlayers)



@app.route("/game/<int:id>/<name>/<int:score>/<int:attempt>", methods=['GET', 'POST'])
def game(id, name, score, attempt):
    print(f'Length of multiplayers is {len(multiplayers)}')
    print(f'Length of fixtures is {len(fixList)}')
    form = AnswerForm()
    if form.validate_on_submit():
        name = name
        plrAnswer = form.answer.data
        currId = id
        correctRes = getCorrectResult(currId)
        if id <= 9:
            if attempt == 1:
                if plrAnswer != correctRes:
                    flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                    return redirect(url_for('game', id=id, name=name, score=score, attempt=2))
                else:
                    flash(f'You are correct {name}', 'success')
                    return redirect(url_for('game', id=id+1, name=name, score=score+plrAnswer, attempt=1))
            elif attempt == 2:
                if plrAnswer != correctRes:
                    flash(f'Wrong answer {name}', 'dark')
                    return redirect(url_for('game', id=id+1, name=name, score=score, attempt=1))
                else:
                    flash(f'You are correct {name}', 'success')
                    return redirect(url_for('game', id=id+1, name=name, score=score+1, attempt=1))
        elif id == 10:
            if attempt == 1:
                if plrAnswer != correctRes:
                    flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                    return redirect(url_for('game', id=10, name=name, score=score, attempt=2))
                else:
                    score = score + plrAnswer
                    return redirect(url_for('winner', name=name, score=score))
            if attempt == 2:
                if plrAnswer != correctRes:
                    return redirect(url_for('winner', name=name, score=score))
                else:
                    score = score +1
                    return redirect(url_for('winner', name=name, score=score))
    return render_template('game.html', form=form,
                                   id=id, fixList=fixList, name=name)




@app.route("/multiplayer/<int:id>/<int:pNum>/<int:attempt>", methods=['GET', 'POST'])
def multiplayer(id, pNum, attempt):
    print(f'Length of multiplayers is {len(multiplayers)}')
    print(f'Length of fixtures is {len(fixList)}')
    form = AnswerForm()
    if form.validate_on_submit():
        plrAnswer = form.answer.data
        name = getPlayerName(multiplayers, pNum)
        # count is the number of players
        count = len(multiplayers)
        currId = id
        correctRes = getCorrectResult(currId)
        fixtures = 10
        # play game only for count number of players
        if pNum <= count:
            # last fixture, last player
            if id == fixtures and pNum == count:
                if attempt == 1:
                    if plrAnswer != correctRes:
                        flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                        return redirect(url_for('multiplayer', id=id, pNum=pNum, attempt=2))
                    else:
                        multiplayers[pNum-1].incScore(1, plrAnswer)
                        print(multiplayers[pNum-1].name)
                        print(multiplayers[pNum-1].score)
                        return redirect(url_for('winnermult'))
                elif attempt == 2:
                    if plrAnswer != correctRes:
                        return redirect(url_for('winnermult'))
                    else:
                        multiplayers[pNum-1].incScore(2, plrAnswer)
                        print(multiplayers[pNum-1].name)
                        print(multiplayers[pNum-1].score)
                        return redirect(url_for('winnermult'))
            # if last player in a Question
            elif pNum == count:
                if attempt == 1:
                    if plrAnswer != correctRes:
                        flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                        return redirect(url_for('multiplayer', id=id, pNum=pNum, attempt=2))
                    else:
                        flash(f'You are correct {name}', 'success')
                        multiplayers[pNum-1].incScore(1, plrAnswer)
                        print(multiplayers[pNum-1].name)
                        print(multiplayers[pNum-1].score)
                        return redirect(url_for('multiplayer', id=id+1, pNum=1, attempt=1))
                elif attempt == 2:
                    if plrAnswer != correctRes:
                        flash(f'Wrong answer {name}', 'dark')
                        return redirect(url_for('multiplayer', id=id+1, pNum=1, attempt=1))
                    else:
                        flash(f'You are correct {name}', 'success')
                        multiplayers[pNum-1].incScore(2, plrAnswer)
                        print(multiplayers[pNum-1].name)
                        print(multiplayers[pNum-1].score)
                        return redirect(url_for('multiplayer', id=id+1, pNum=1, attempt=1))
            # fixture 1 to 9 all players excluding last player
            elif pNum < count:
                if attempt == 1:
                    if plrAnswer != correctRes:
                        flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                        return redirect(url_for('multiplayer', id=id, pNum=pNum, attempt=2))
                    else:
                        flash(f'You are correct {name}', 'success')
                        multiplayers[pNum-1].incScore(1, plrAnswer)
                        print(multiplayers[pNum-1].name)
                        print(multiplayers[pNum-1].score)
                        return redirect(url_for('multiplayer', id=id, pNum=pNum+1, attempt=1))
                elif attempt == 2:
                    if plrAnswer != correctRes:
                        flash(f'Wrong answer {name}', 'dark')
                        return redirect(url_for('multiplayer', id=id, pNum=pNum+1, attempt=1))
                    else:
                        flash(f'You are correct {name}', 'success')
                        multiplayers[pNum-1].incScore(2, plrAnswer)
                        print(multiplayers[pNum-1].name)
                        print(multiplayers[pNum-1].score)
                        return redirect(url_for('multiplayer', id=id, pNum=pNum+1, attempt=1))
    return render_template('multiplayer.html', form=form,
                                   id=id, fixList=fixList, pNum=pNum, multiplayers=multiplayers)


@app.route("/winner/<string:name>/<int:score>", methods=['GET', 'POST'])
def winner(name, score):
    name = name
    score = score
    with open('scores.txt', 'a') as f:
        name = name
        score = score
        f.write(f'{name}:{score}\n')
    return render_template('winner.html', calcWinner=calcWinner, highscores=highscores, name=name, score=score)


@app.route("/winnermult", methods=['GET', 'POST'])
def winnermult():
    # name = name
    # score = score
    # if len(players) == 1:
    # with open('scores.txt', 'a') as w:
    #     name = name
    #     score = score
    #     w.write(f'{name}:{score}\n')
        # if len(highscores) > 0:
        #     addToHighscores()
    # else:
    # Sort players by score
    multiplayers.sort(key=lambda x: x.score, reverse=True)
    if len(multiplayers) > 1:
        calcWinner(multiplayers[0], multiplayers[1])
    return render_template('winnermult.html', multiplayers=multiplayers, calcWinner=calcWinner, highscores=highscores)



@app.route("/leaderboard", methods=['GET', 'POST'])
def leaderboard():
    resetHighscores()
    getHighscores()
    sortedHighscores = sorted(highscores, key=lambda item: item['score'], reverse=True)
    topTen = sortedHighscores[0:10]
    return render_template('leaderboard.html', title='leaderboard', highscores=highscores, sortedHighscores=sortedHighscores, topTen=topTen)


@app.route("/rules")
def rules():
    return render_template('rules.html')


if __name__ == '__main__':
    app.run(host = os.environ.get("IP"),
            port = int(os.environ.get("PORT", 5000)),
            debug = True, use_reloader=False)
