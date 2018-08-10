from flask import Flask, render_template, url_for, flash, redirect
from forms import PlayerNumForm, NameForm, AnswerForm
from game import Question, Player, calcWinner

app = Flask(__name__)

# app.config['SECRET_KEY'] = 'nusmmirhdl4472'

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

# when new game is started the players list is cleared
def resetGame():
    del players[:]


#function to extract scores from scores.txt and create dictionary of highscore player objects
def getHighscores():
    with open('scores.txt', 'r') as r:
        for line in r:
            player = {}
            name, score = line.split(':')
            player['name'] = name
            player['score'] = score
            highscores.append(player)


# create fixtures for the game questions
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


# getHighscores()
getFixtures()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', games=games)


@app.route("/newgame", methods=['GET', 'POST'])
def newgame():
    resetGame()
    form = PlayerNumForm()
    if form.validate_on_submit():
        numPlayers = form.players.data
        flash(f'{numPlayers} player game created!', 'dark')
        for player in range(int(numPlayers)):
            player = Player()
            players.append(player)
        return redirect(url_for('enternames', id=1))
    return render_template('newgame.html', title='newgame', form=form )


# @app.route("/enternames/<int:id>", methods=['GET', 'POST'])
# def enternames(id):
#     form = NameForm()
#     if form.validate_on_submit():
#         if id < len(players):
#             name = form.playername.data
#             players[id].name = name
#             flash(f'Good luck {name}!! ', 'dark')
#             return redirect(url_for('enternames', id=id+1))
#         elif len(players) == 1:
#             name = form.playername.data
#             players[0].name = name
#             flash(f'Good luck {name}!! ', 'dark')
#             return redirect(url_for('game', id=1, pNum=1, attempt=1))
#         else:
#             return redirect(url_for('game', id=1, pNum=1, attempt=1))
#     return render_template('enternames.html', title='names', form=form, id=id, players=players)

@app.route("/enternames/<int:id>", methods=['GET', 'POST'])
def enternames(id):
    form = NameForm()
    if form.validate_on_submit():
        name = form.playername.data
        players[id-1].name = name
        flash(f'Good luck {name}!! ', 'dark')
        if id < len(players):
            return redirect(url_for('enternames', id=id+1))
        else:
            return redirect(url_for('game', id=1, pNum=1, attempt=1))
    return render_template('enternames.html', title='names', form=form, id=id, players=players)


@app.route("/game/<int:id>/<int:pNum>/<int:attempt>", methods=['GET', 'POST'])
def game(id, pNum, attempt):
    form = AnswerForm()
    for game in games:
        if form.validate_on_submit():
            answer = form.answer.data
            players[pNum-1].answer = answer
            res = results[id-1]
            if id == len(games):
                if len(players) > pNum:
                    if attempt == 1:
                        if answer != res:
                            flash(f'One more go {players[pNum-1].name}, your first guess was: {answer} ', 'dark')
                            return redirect(url_for('game', id=id, pNum=pNum, attempt=attempt+1))
                        else:
                            players[pNum-1].score = players[pNum-1].score + int(answer)
                            return redirect(url_for('game', id=1, pNum=pNum+1, attempt=1))
                    else:
                        if answer == res:
                            flash(f'You are correct {players[pNum-1].name}', 'success')
                            players[pNum-1].score = players[pNum-1].score +1
                            return redirect(url_for('game', id=1, pNum=pNum+1, attempt=1))
                        else:
                            return redirect(url_for('game', id=1, pNum=pNum+1, attempt=1))
                else:
                    if attempt == 1:
                        if answer != res:
                            flash(f'One more go {players[pNum-1].name}, your first guess was: {answer} ', 'dark')
                            return redirect(url_for('game', id=id, pNum=pNum, attempt=attempt+1))
                        else:
                            players[pNum-1].score = players[pNum-1].score + int(answer)
                            return redirect(url_for('winner'))
                    else:
                        if answer != res:
                            return redirect(url_for('winner'))
                        else:
                            players[pNum-1].score = players[pNum-1].score + 1
                            return redirect(url_for('winner'))
            if id < len(games):
                    secondAttempt = False
                    if answer != res:
                        if attempt < 2:
                            flash(f'One more go {players[pNum-1].name}, your first guess was: {answer} ', 'dark')
                            secondAttempt = True
                            return redirect(url_for('game', id=id, pNum=pNum, attempt=attempt+1))
                        else:
                            flash(f'Wrong again {players[pNum-1].name}! ', 'warning')
                            return redirect(url_for('game', id=id+1, pNum=pNum, attempt=1))
                    else:
                        flash(f'You are correct {players[pNum-1].name}', 'dark')
                        if secondAttempt == False:
                            players[pNum-1].score = players[pNum-1].score + int(answer)
                        else:
                            players[pNum-1].score = players[pNum-1].score +1
                        return redirect(url_for('game', id=id+1, pNum=pNum, attempt=1))
        return render_template('game.html', title='game', form=form, games=games,
                                       id=id, player=players, fixList=fixList, results=results, pNum=pNum)



@app.route("/winner", methods=['GET', 'POST'])
def winner():
    if len(players) == 1:
        with open('scores.txt', 'a') as w:
            name = players[0].name
            score = str(players[0].score)
            w.write(f'{name}:{score}\n')
            if len(highscores) > 0:
                highscore()
    else:
        # Sort players by score
        players.sort(key=lambda x: x.score, reverse=True)
        if len(players) > 1:
            calcWinner(players[0], players[1])
    return render_template('winner.html', title='winner', players=players, calcWinner=calcWinner, highscores=highscores)



#read last line of scores.txt and add to highscores array
def highscore():
    with open('scores.txt', 'r') as r:
        player = {}
        last_line = r.readlines()[-1]
        name, score = last_line.split(':')
        player['name'] = name
        player['score'] = score
        highscores.append(player)


getHighscores()
#sort highscores into top ten
sortedArray = sorted(highscores, key=lambda item: item['score'], reverse=True)
topTen = sortedArray[0:10]


@app.route("/leaderboard", methods=['GET', 'POST'])
def leaderboard():
    return render_template('leaderboard.html', title='leaderboard', highscores=highscores, sortedArray=sortedArray, topTen=topTen)


@app.route("/rules")
def rules():
    return render_template('rules.html')


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
    # app.run(debug=True)
    #app.run(debug=True, host='0.0.0.0')
