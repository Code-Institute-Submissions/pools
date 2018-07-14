from flask import Flask, render_template, url_for, flash, redirect
from forms import PlayerNumForm, NameForm, AnswerForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'nusmmirhdl4472'

games = [
    {'game': 1,
    'teams': ['Man Utd', 'Watford'],
    'result': 'Home Win'
    },
    {'game': 2,
    'teams': ['Hudd', 'Arsenal'],
    'result': 'Away Win'}
    ]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', games=games)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/newgame", methods=['GET', 'POST'])
def newgame():
    form = PlayerNumForm()
    if form.validate_on_submit():
        flash(f'{form.players.data} player game created!', 'success')
        return redirect(url_for('enternames'))
    return render_template('newgame.html', title='newgame', form=form)


@app.route("/enternames", methods=['GET', 'POST'])
def enternames():
    form = NameForm()
    if form.validate_on_submit():
        flash(f'Good luck {form.playername.data}!! ', 'success')
        return redirect(url_for('game'))
    return render_template('enternames.html', title='names', form=form)


@app.route("/game", methods=['GET', 'POST'])
def game():
    form = AnswerForm()
    if form.validate_on_submit():
        flash(f'You predicted {form.answer.data} ', 'success')
    return render_template('game.html', title='game', form=form)


@app.route("/leaderboard", methods=['GET', 'POST'])
def leaderboard():
    return render_template('leaderboard.html', title='leaderboard')


if __name__ == '__main__':
    app.run(debug=True)
