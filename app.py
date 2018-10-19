import os, json, random
from flask import Flask, render_template, url_for, flash, redirect
from forms import PlayerNumForm, NameForm, AnswerForm
from game import Question, Player, calcWinner, createPlayerList, getPlayerName, getPlayerNameList

app = Flask(__name__)

app.config['SECRET_KEY'] = 'nusmmirhdl4472'

games = [
    {"game": 1,
    "teams": ["Man Utd", "Watford"],
    "result": 1
    },
    {"game": 2,
    "teams": ["Hudd", "Arsenal"],
    "result": 2
    },
    {"game": 3,
    "teams": ["Swansea", "Stoke"],
    "result": 3}
    ]

# player objects
players = []
fixList = []
results = []
# player scores dictionary
highscores = []
sortedArray = []
topTen = []


def resetHighscores():
    del highscores[:]


#read last line of scores.txt and add to highscores array
def addToHighscores():
    with open('scores.txt', 'r') as r:
        player = {}
        last_line = r.readlines()[-1]
        name, score = last_line.split(':')
        player['name'] = name
        player['score'] = score
        highscores.append(player)


#function to extract scores from scores.txt and create dictionary of highscore player objects
def getHighscores():
    with open('scores.txt', 'r') as r:
        for line in r:
            player = {}
            name, score = line.split(':')
            player['name'] = name
            player['score'] = score
            highscores.append(player)


# create fixtures manually for the game questions
def getFixtures():
    for game in games:
        home = game['teams'][0]
        away = game['teams'][1]
        result = game['result']
        question = Question(home, away, result)
        fixture = question.fixture()
        res = question.res()
        fixList.append(fixture)
        results.append(res)


# create fixtures from json stripped file
def getjFixtures():
    with open('2015_stripped.json') as f:
        data = json.load(f)
        # There are 38 fixture weeks in the season
        randomWeek = random.randrange(37)
        # Select random week from the json data
        matchweek = data['rounds'][randomWeek]['matches']
        for game in matchweek:
            home = game['team1']['name']
            away = game['team2']['name']
            result = game['result']
            question = Question(home, away, result)
            fixture = question.fixture()
            res = question.res()
            fixList.append(fixture)
            results.append(res)


def addToPlayersList(ply):
    players.append(ply)


getHighscores()
sortedHighscores = sorted(highscores, key=lambda item: item['score'], reverse=True)
topTen = sortedHighscores[0:10]

# getFixtures()

multiplayers = createPlayerList()



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', games=games)


@app.route("/newgame", methods=['GET', 'POST'])
def newgame():
    del fixList[:]
    del results[:]
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
        # player = Player(name)
        # addToPlayersList(player)
        # with open('player_Names.txt', 'w') as w:
        #     name = name
        #     w.write(f'{name}\n')
        flash(f'Good luck {name}!! ', 'dark')
        if numPlayers == 1:
            return redirect(url_for('game', id=1, pNum=1, name=name, score=0, attempt=1))
        elif id < numPlayers:
            return redirect(url_for('enternames', id=id+1, numPlayers=numPlayers))
        elif id == numPlayers:
            return redirect(url_for('multiplayer', id=1, pNum=1, attempt=1))
    getjFixtures()
    return render_template('enternames.html', form=form, id=id, numPlayers=numPlayers)



@app.route("/game/<int:id>/<name>/<int:score>/<int:attempt>", methods=['GET', 'POST'])
def game(id, name, score, attempt):
    form = AnswerForm()
    if form.validate_on_submit():
        name = name
        player = Player(name)
        plrAnswer = form.answer.data
        correctRes = results[id-1]
        if id <= 2:
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
        elif id == 3:
            if attempt == 1:
                if plrAnswer != correctRes:
                    flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                    return redirect(url_for('game', id=3, name=name, score=score, attempt=2))
                else:
                    score = score + plrAnswer
                    return redirect(url_for('winner', name=name, score=score))
            if attempt == 2:
                if plrAnswer != correctRes:
                    return redirect(url_for('winner', name=name, score=score))
                else:
                    score = score +1
                    return redirect(url_for('winner', name=name, score=score))
    return render_template('game.html', form=form, games=games,
                                   id=id, players=players, fixList=fixList, results=results, name=name)




@app.route("/multiplayer/<int:id>/<int:pNum>/<int:attempt>", methods=['GET', 'POST'])
def multiplayer(id, pNum, attempt):
    form = AnswerForm()
    if form.validate_on_submit():
        plrAnswer = form.answer.data
        correctRes = results[id-1]
        name = getPlayerName(multiplayers, pNum)
        # count is the number of players
        count = len(multiplayers)
        id = id
        pNum = pNum
        # number of fixtures limit
        fixtures = 3
        # do stuff only for count players
        if pNum <= count:
            # last player, last fixture, will be 10 in json
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
            # fixture 1 all players
            elif attempt == 1:
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
                                   id=id, fixList=fixList, results=results, pNum=pNum, multiplayers=multiplayers)


@app.route("/winner/<string:name>/<int:score>", methods=['GET', 'POST'])
def winner(name, score):
    name = name
    score = score
    with open('scores.txt', 'a') as w:
        name = name
        score = score
        w.write(f'{name}:{score}\n')
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
            debug = True)
