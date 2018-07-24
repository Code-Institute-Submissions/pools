from flask import Flask, render_template, url_for, flash, redirect
from forms import PlayerNumForm, NameForm, AnswerForm
from game import Question, Player

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

players = []
fixList = []
results = []


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


getFixtures()

# home = games[0]['teams'][0]
# away = games[0]['teams'][1]
# result = games[0]['result']

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', games=games)


@app.route("/newgame", methods=['GET', 'POST'])
def newgame():
    form = PlayerNumForm()
    if form.validate_on_submit():
        numPlayers = form.players.data
        flash(f'{numPlayers} player game created!', 'success')
        for i in range(int(numPlayers)):
            #i = player
            player = Player()
            #players.append(i)
            players.append(player)
        return redirect(url_for('enternames', id=1))
    return render_template('newgame.html', title='newgame', form=form, player=Player)


@app.route("/enternames/<int:id>", methods=['GET', 'POST'])
def enternames(id):
    form = NameForm()
    if form.validate_on_submit():
        name = form.playername.data
        players[id-1].name = name
        flash(f'Good luck {name}!! ', 'success')
        if id < len(players):
            return redirect(url_for('enternames', id=id+1))
        else:
            return redirect(url_for('game', id=1, pNum=1, attempt=1))
    return render_template('enternames.html', title='names', form=form, id=1, players=players)


@app.route("/game/<int:id>/<int:pNum>/<int:attempt>", methods=['GET', 'POST'])
def game(id, pNum, attempt):
    form = AnswerForm()
    for game in games:
        if form.validate_on_submit():
            answer = form.answer.data
            players[pNum-1].answer = answer
            res = results[id-1]
            #secondAttempt = True
            if id == len(games):
                if len(players) > pNum:
                    if attempt == 1:
                        if answer != res:
                            flash(f'One more go {players[pNum-1].name}, your first guess was: {answer} ', 'warning')
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
                            flash(f'One more go {players[pNum-1].name}, your first guess was: {answer} ', 'warning')
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
                            flash(f'One more go {players[pNum-1].name}, your first guess was: {answer} ', 'warning')
                            secondAttempt = True
                            return redirect(url_for('game', id=id, pNum=pNum, attempt=attempt+1))
                        else:
                            flash(f'Wrong again {players[pNum-1].name}! ', 'warning')
                            return redirect(url_for('game', id=id+1, pNum=pNum, attempt=1))
                    else:
                        flash(f'You are correct {players[pNum-1].name}', 'success')
                        if secondAttempt == False:
                            players[pNum-1].score = players[pNum-1].score + int(answer)
                        else:
                            players[pNum-1].score = players[pNum-1].score +1
                        return redirect(url_for('game', id=id+1, pNum=pNum, attempt=1))
        return render_template('game.html', title='game', form=form, games=games,
                                       id=id, player=players, fixList=fixList, results=results, pNum=pNum)



@app.route("/winner", methods=['GET', 'POST'])
def winner():
    return render_template('winner.html', title='winner', players=players)


@app.route("/leaderboard", methods=['GET', 'POST'])
def leaderboard():
    return render_template('leaderboard.html', title='leaderboard')


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
    #app.run(debug=True, host='0.0.0.0')



'''
@app.route("/enternames/<int:id>", methods=['GET', 'POST'])
def enternames(id):
    form = NameForm()
    if form.validate_on_submit():
        name = form.playername.data
        players[id-1].name = name
        flash(f'Good luck {name}!! ', 'success')
        if len(players) == 2:
            return redirect(url_for('enternames', title='names', form=form, id=2))
        return redirect(url_for('game', id=1))
    return render_template('enternames.html', title='names', form=form, id=1)
'''
