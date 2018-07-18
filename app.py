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
    "result": 3}
    ]


players = []


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
            i = Player()
            players.append(i)
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
            return redirect(url_for('game', id=1, attempt=1))
    return render_template('enternames.html', title='names', form=form, id=1, players=players)


@app.route("/game/<int:id>/<int:attempt>", methods=['GET', 'POST'])
def game(id, attempt):
    form = AnswerForm()
    if form.validate_on_submit():
        answer = form.answer.data
        home = games[0]['teams'][0]
        away = games[0]['teams'][1]
        result = games[0]['result']
        question = Question(home, away, result)
        players[0].answer = answer
        if answer != result:
            if attempt < 2:
                flash(f'One more go {players[0].name}, your first guess was: {answer} ', 'warning')
                return redirect(url_for('game', id=id, attempt=attempt+1))
            else:
                flash(f'Wrong again {players[0].name}! ', 'warning')
                return redirect(url_for('game', id=id+1, attempt=1))
        else:
            flash(f'You are correct {players[0].name}', 'success')
            return redirect(url_for('game', id=id+1, attempt=1))
    return render_template('game.html', title='game', form=form, games=games)


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
