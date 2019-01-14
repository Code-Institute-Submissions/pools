import os
import json
import random
from flask import Flask, render_template, url_for, flash, redirect, session, escape, request
from flask_pymongo import PyMongo
from forms import PlayerNumForm, NameForm, AnswerForm
from game import Question, Player, calc_winner, create_player_list, get_player_name, add_to_highscores, get_highscores, get_rand_match_week, create_fixtures, get_correct_result, init_game, reset_highscores, get_scores


app = Flask(__name__)


app.config['SECRET_KEY'] = 'nusmmirhdl4472hfjhfxszlonn52t'
app.config['MONGO_DBNAME'] = 'scores_game'
app.config['MONGO_URI'] = 'mongodb://roykeane:roykeane16@ds251284.mlab.com:51284/scores_game'

mongo = PyMongo(app)

highscores = get_scores(mongo)



@app.route("/")
@app.route("/home")
def home():
    if session:
        session.clear()
    return render_template('home.html')




@app.route("/newgame", methods=['GET', 'POST'])
def newgame():
    session = { 'id': 1, 'players': 0, 'name': 'Joe', 'score': 0, 'attempt': 1, 'week': 0 }
    form = PlayerNumForm()
    if form.validate_on_submit():
        num_players = int(form.players.data)
        session['players'] = num_players
        flash(f'{num_players} player game created!', 'dark')
        return redirect(url_for('enternames', id=1, num_players=num_players, name1='name1', name2='name2'))
    return render_template('newgame.html', title='newgame', form=form )




@app.route("/enternames/<int:id>/<int:num_players>/<name1>/<name2>", methods=['GET', 'POST'])
def enternames(id, num_players, name1, name2):
    form = NameForm()
    if form.validate_on_submit():
        name = form.playername.data
        flash(f'Good luck {name}!! ', 'dark')
        if num_players == 1:
            session['name'] = name
            rand_week = random.randrange(38)
            session['week'] = rand_week
            session['id'] = 1
            session['score'] = 0
            return redirect(url_for('game', id=1, attempt=1))
        if id < num_players:
            return redirect(url_for('enternames', id=id+1, num_players=num_players, name1=name, name2=name2))
        elif id == num_players:
            name_2=name
            rand_week = random.randrange(38)
            return redirect(url_for('multiplayer', id=1, p_num=1, attempt=1, week=rand_week, name_1=name1, score_a=0, name_2=name_2, score_b=0))
    return render_template('enternames.html', form=form, id=id, num_players=num_players)




@app.route("/game/<int:id>/<int:attempt>", methods=['GET', 'POST'])
def game(id, attempt):
    form = AnswerForm()
    week = session['week']
    fix_list = init_game(week)
    name = session['name']
    score = session['score']    
    if form.validate_on_submit():
        plr_answer = form.answer.data
        currId = id
        correct_result = get_correct_result(currId, fix_list)
        if id <= 9:
            if attempt == 1:
                if plr_answer != correct_result:
                    flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                    return redirect(url_for('game', id=id, attempt=2))
                else:
                    flash(f'You are correct {name}', 'success')
                    session['score'] = session['score'] + plr_answer
                    return redirect(url_for('game', id=id+1, attempt=1))
            elif attempt == 2:
                if plr_answer != correct_result:
                    flash(f'Wrong answer {name}', 'dark')
                    return redirect(url_for('game', id=id+1, attempt=1))
                else:
                    flash(f'You are correct {name}', 'success')
                    session['score'] = session['score'] + 1
                    return redirect(url_for('game', id=id+1, attempt=1))
        elif id == 10:
            if attempt == 1:
                if plr_answer != correct_result:
                    flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                    return redirect(url_for('game', id=10, attempt=2))
                else:
                    score = score + plr_answer
                    return redirect(url_for('winner'))
            if attempt == 2:
                if plr_answer != correct_result:
                    return redirect(url_for('winner'))
                else:
                    session['score'] = session['score'] + 1
                    return redirect(url_for('winner'))
    return render_template('game.html', form=form,
                                   id=id, fix_list=fix_list, name=name, week=week)




@app.route("/multiplayer/<int:id>/<int:p_num>/<int:attempt>/<int:week>/<name_1>/<int:score_a>/<name_2>/<int:score_b>", methods=['GET', 'POST'])
def multiplayer(id, p_num, attempt, week, name_1, score_a, name_2, score_b):
    player1 = Player(name=name_1)
    player2 = Player(name=name_2)
    nm1 = player1.get_name()
    nm2 = player2.get_name()
    names = [nm1, nm2]
    multiplayers = [player1, player2]
    form = AnswerForm()
    fix_list = init_game(week)
    if form.validate_on_submit():
        plr_answer = form.answer.data
        count = 2
        currId = id
        correct_result = get_correct_result(currId, fix_list)
        fixtures = 10
        """ play game only for count number of players """
        if p_num <= count:
            """ last fixture, last player """
            if id == fixtures and p_num == count:
                if attempt == 1:
                    if plr_answer != correct_result:
                        flash(f'Wrong answer {names[p_num-1]}, you have one more attempt', 'dark')
                        return redirect(url_for('multiplayer', id=id, p_num=p_num, attempt=2, week=week, name_1=name_1, score_a=score_a, name_2=name_2, score_b=score_b))
                    else:
                        multiplayers[p_num-1].inc_score(1, plr_answer)
                        return redirect(url_for('winnermult', name_1=name_1, score_a=score_a, name_2=name_2, score_b=score_b+plr_answer))
                elif attempt == 2:
                    if plr_answer != correct_result:
                        return redirect(url_for('winnermult', name_1=name_1, score_a=score_a, name_2=name_2, score_b=score_b))
                    else:
                        multiplayers[p_num-1].inc_score(2, plr_answer)
                        return redirect(url_for('winnermult', name_1=name_1, score_a=score_a, name_2=name_2, score_b=score_b+1))
            # if last player in a Question
            elif p_num == count:
                if attempt == 1:
                    if plr_answer != correct_result:
                        flash(f'Wrong answer {names[p_num-1]}, you have one more attempt', 'dark')
                        print(multiplayers[p_num -1].get_score())
                        return redirect(url_for('multiplayer', id=id, p_num=p_num, attempt=2, week=week, name_1=name_1, score_a=score_a, name_2=name_2, score_b=score_b))
                    else:
                        flash(f'You are correct {names[p_num-1]}', 'success')
                        multiplayers[p_num-1].inc_score(1, plr_answer)
                        print(multiplayers[p_num -1].get_score())
                        return redirect(url_for('multiplayer', id=id+1, p_num=1, attempt=1, week=week, name_1=name_1, score_a=score_a, name_2=name_2, score_b=score_b+plr_answer))
                elif attempt == 2:
                    if plr_answer != correct_result:
                        flash(f'Wrong answer {names[p_num-1]}', 'dark')
                        print(multiplayers[p_num -1].get_score())
                        return redirect(url_for('multiplayer', id=id+1, p_num=1, attempt=1, week=week, name_1=name_1, score_a=score_a, name_2=name_2, score_b=score_b))
                    else:
                        flash(f'You are correct {names[p_num-1]}', 'success')
                        multiplayers[p_num-1].inc_score(2, plr_answer)
                        print(multiplayers[p_num -1].get_score())
                        return redirect(url_for('multiplayer', id=id+1, p_num=1, attempt=1, week=week, name_1=name_1, score_a=score_a, name_2=name_2, score_b=score_b+1))
            # fixture 1 to 9 all players excluding last player
            elif p_num < count:
                if attempt == 1:
                    if plr_answer != correct_result:
                        flash(f'Wrong answer {names[p_num-1]}, you have one more attempt', 'dark')
                        print(multiplayers[p_num -1].get_score())
                        return redirect(url_for('multiplayer', id=id, p_num=p_num, attempt=2, week=week, name_1=name_1, score_a=score_a, name_2=name_2, score_b=score_b))
                    else:
                        flash(f'You are correct {names[p_num-1]}', 'success')
                        multiplayers[p_num-1].inc_score(1, plr_answer)
                        print(multiplayers[p_num -1].get_score())
                        return redirect(url_for('multiplayer', id=id, p_num=p_num+1, attempt=1, week=week, name_1=name_1, score_a=score_a+plr_answer, name_2=name_2, score_b=score_b))
                elif attempt == 2:
                    if plr_answer != correct_result:
                        flash(f'Wrong answer {names[p_num-1]}', 'dark')
                        print(multiplayers[p_num -1].get_score())
                        return redirect(url_for('multiplayer', id=id, p_num=p_num+1, attempt=1, week=week, name_1=name_1, score_a=score_a, name_2=name_2, score_b=score_b))
                    else:
                        flash(f'You are correct {names[p_num-1]}', 'success')
                        multiplayers[p_num-1].inc_score(2, plr_answer)
                        print(multiplayers[p_num -1].get_score())
                        return redirect(url_for('multiplayer', id=id, p_num=p_num+1, attempt=1, week=week, name_1=name_1, score_a=score_a+1, name_2=name_2, score_b=score_b))
    return render_template('multiplayer.html', form=form,
                                   id=id, fix_list=fix_list, p_num=p_num, multiplayers=multiplayers, names=names, week=week)



@app.route("/winner", methods=['GET', 'POST'])
def winner():
    name = session['name']
    score = session['score']
    scores_table = mongo.db.scores_table
    scores_table.insert({'name': name,
                    'score': score})
    return render_template('winner.html', calc_winner=calc_winner, name=name, score=score)



@app.route("/winnermult/<name_1>/<int:score_a>/<name_2>/<int:score_b>", methods=['GET', 'POST'])
def winnermult(name_1, score_a, name_2, score_b):
    player1 = Player(name=name_1)
    player2 = Player(name=name_2)
    player1.set_score(score_a)
    player2.set_score(score_b)
    nm1 = player1.get_name()
    nm2 = player2.get_name()
    names = [nm1, nm2]
    scores = [score_a, score_b]
    multiplayers = [player1, player2]
    multiplayers.sort(key=lambda x: x.score, reverse=True)
    if len(multiplayers) > 1:
        calc_winner(multiplayers[0], multiplayers[1])
    return render_template('winnermult.html', multiplayers=multiplayers, calc_winner=calc_winner, highscores=highscores, names=names, scores=scores)



@app.route("/leaderboard", methods=['GET', 'POST'])
def leaderboard():
    updated_highscores = get_scores(mongo)
    sorted_highscores = sorted(updated_highscores, key=lambda item: item['score'], reverse=True)
    top_ten = sorted_highscores[0:10]
    return render_template('leaderboard.html', title='leaderboard', sorted_highscores=sorted_highscores, top_ten=top_ten)



@app.route("/rules")
def rules():
    return render_template('rules.html')



if __name__ == '__main__':
    app.run(host = os.environ.get("IP"),
            port = int(os.environ.get("PORT", 5000)),
            debug = True, use_reloader=False)
