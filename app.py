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


player1 = Player()
player2 = Player()
names = ['a', 'b']
multiplayers = [player1, player2]
# highscores = get_highscores()
highscores = get_scores(mongo)




@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')




@app.route("/newgame", methods=['GET', 'POST'])
def newgame():
    # session.pop('player', None)
    form = PlayerNumForm()
    if form.validate_on_submit():
        num_players = int(form.players.data)
        flash(f'{num_players} player game created!', 'dark')
        return redirect(url_for('enternames', id=1, num_players=num_players))
    with open('player_Names.txt', 'r+') as f:
        f.truncate(0)
    return render_template('newgame.html', title='newgame', form=form )





@app.route("/enternames/<int:id>/<int:num_players>", methods=['GET', 'POST'])
def enternames(id, num_players):
    form = NameForm()
    if form.validate_on_submit():
        name = form.playername.data
        flash(f'Good luck {name}!! ', 'dark')
        if num_players == 1:
            rand_week = random.randrange(38)
            return redirect(url_for('game', id=1, name=name, score=0, attempt=1, week=rand_week))
        if id < num_players:
            names.append(name)
            player1 = mongo.db.players
            player1.insert({'name': name,
                            'score': 0})
            multiplayers[id-1].set_name(name)
            print('Names after first name entry..')
            print(names)
            return redirect(url_for('enternames', id=id+1, num_players=num_players))
        elif id == num_players:
            names.append(name)
            player2 = mongo.db.players
            player2.insert({'name': name,
                            'score': 0})
            multiplayers[id-1].set_name(name)
            rand_week = random.randrange(38)
            print('Names after second name entry..')
            print(names)
            return redirect(url_for('multiplayer', id=1, p_num=1, attempt=1, week=rand_week))
    return render_template('enternames.html', form=form, id=id, num_players=num_players)




@app.route("/game/<int:id>/<name>/<int:score>/<int:attempt>/<int:week>", methods=['GET', 'POST'])
def game(id, name, score, attempt, week):
    form = AnswerForm()
    fix_list = init_game(week)
    if form.validate_on_submit():
        name = name
        session['player'] = name
        plr_answer = form.answer.data
        currId = id
        correct_result = get_correct_result(currId, fix_list)
        if id <= 9:
            if attempt == 1:
                if plr_answer != correct_result:
                    flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                    return redirect(url_for('game', id=id, name=name, score=score, attempt=2, week=week))
                else:
                    flash(f'You are correct {name}', 'success')
                    return redirect(url_for('game', id=id+1, name=name, score=score+plr_answer, attempt=1, week=week))
            elif attempt == 2:
                if plr_answer != correct_result:
                    flash(f'Wrong answer {name}', 'dark')
                    return redirect(url_for('game', id=id+1, name=name, score=score, attempt=1, week=week))
                else:
                    flash(f'You are correct {name}', 'success')
                    return redirect(url_for('game', id=id+1, name=name, score=score+1, attempt=1, week=week))
        elif id == 10:
            if attempt == 1:
                if plr_answer != correct_result:
                    flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                    return redirect(url_for('game', id=10, name=name, score=score, attempt=2, week=week))
                else:
                    score = score + plr_answer
                    return redirect(url_for('winner', name=name, score=score))
            if attempt == 2:
                if plr_answer != correct_result:
                    return redirect(url_for('winner', name=name, score=score))
                else:
                    score = score +1
                    return redirect(url_for('winner', name=name, score=score))
    return render_template('game.html', form=form,
                                   id=id, fix_list=fix_list, name=name, week=week)




@app.route("/multiplayer/<int:id>/<int:p_num>/<int:attempt>/<int:week>", methods=['GET', 'POST'])
def multiplayer(id, p_num, attempt, week):
    print(multiplayers)
    print(multiplayers[0].get_name())
    print(multiplayers[1].get_name())
    name1 = multiplayers[0].get_name()
    name2 = multiplayers[1].get_name()
    names = [name1, name2]
    form = AnswerForm()
    fix_list = init_game(week)
    # name = multiplayers[int(p_num) -1].get_name()
    if form.validate_on_submit():
        plr_answer = form.answer.data
        # name = multiplayers[int(p_num) -1].get_name()
        # print(name)
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
                        return redirect(url_for('multiplayer', id=id, p_num=p_num, attempt=2, week=week))
                    else:
                        multiplayers[p_num-1].inc_score(1, plr_answer)
                        return redirect(url_for('winnermult'))
                elif attempt == 2:
                    if plr_answer != correct_result:
                        return redirect(url_for('winnermult'))
                    else:
                        multiplayers[p_num-1].inc_score(2, plr_answer)
                        return redirect(url_for('winnermult'))
            # if last player in a Question
            elif p_num == count:
                if attempt == 1:
                    if plr_answer != correct_result:
                        flash(f'Wrong answer {names[p_num-1]}, you have one more attempt', 'dark')
                        return redirect(url_for('multiplayer', id=id, p_num=p_num, attempt=2, week=week))
                    else:
                        flash(f'You are correct {names[p_num-1]}', 'success')
                        multiplayers[p_num-1].inc_score(1, plr_answer)
                        return redirect(url_for('multiplayer', id=id+1, p_num=1, attempt=1, week=week))
                elif attempt == 2:
                    if plr_answer != correct_result:
                        flash(f'Wrong answer {names[p_num-1]}', 'dark')
                        return redirect(url_for('multiplayer', id=id+1, p_num=1, attempt=1, week=week))
                    else:
                        flash(f'You are correct {names[p_num-1]}', 'success')
                        multiplayers[p_num-1].inc_score(2, plr_answer)
                        return redirect(url_for('multiplayer', id=id+1, p_num=1, attempt=1, week=week))
            # fixture 1 to 9 all players excluding last player
            elif p_num < count:
                if attempt == 1:
                    if plr_answer != correct_result:
                        print(p_num)
                        flash(f'Wrong answer {names[p_num-1]}, you have one more attempt', 'dark')
                        return redirect(url_for('multiplayer', id=id, p_num=p_num, attempt=2, week=week))
                    else:
                        print(p_num)
                        flash(f'You are correct {names[p_num-1]}', 'success')
                        multiplayers[p_num-1].inc_score(1, plr_answer)
                        return redirect(url_for('multiplayer', id=id, p_num=p_num+1, attempt=1, week=week))
                elif attempt == 2:
                    print(p_num)
                    if plr_answer != correct_result:
                        flash(f'Wrong answer {names[p_num-1]}', 'dark')
                        return redirect(url_for('multiplayer', id=id, p_num=p_num+1, attempt=1, week=week))
                    else:
                        print(p_num)
                        flash(f'You are correct {names[p_num-1]}', 'success')
                        multiplayers[p_num-1].inc_score(2, plr_answer)
                        return redirect(url_for('multiplayer', id=id, p_num=p_num+1, attempt=1, week=week))
    return render_template('multiplayer.html', form=form,
                                   id=id, fix_list=fix_list, p_num=p_num, multiplayers=multiplayers, names=names, week=week)



@app.route("/winner/<string:name>/<int:score>", methods=['GET', 'POST'])
def winner(name, score):
    name = name
    score = score
    scores_table = mongo.db.scores_table
    scores_table.insert({'name': name,
                    'score': score})
    return render_template('winner.html', calc_winner=calc_winner, name=name, score=score)



@app.route("/winnermult", methods=['GET', 'POST'])
def winnermult():
    multiplayers.sort(key=lambda x: x.score, reverse=True)
    if len(multiplayers) > 1:
        calc_winner(multiplayers[0], multiplayers[1])
    return render_template('winnermult.html', multiplayers=multiplayers, calc_winner=calc_winner, highscores=highscores, names=names)



@app.route("/leaderboard", methods=['GET', 'POST'])
def leaderboard():
    # updated_highscores = get_highscores()
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
