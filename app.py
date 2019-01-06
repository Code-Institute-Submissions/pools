import os
import json
import random
from flask import Flask, render_template, url_for, flash, redirect, session, escape, request
from forms import PlayerNumForm, NameForm, AnswerForm
from game import Question, Player, calc_winner, create_player_list, get_player_name, add_to_highscores, get_highscores, get_rand_match_week, create_fixtures, get_correct_result, init_game, reset_highscores, names


app = Flask(__name__)


# SECRET_KEY = os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = 'nusmmirhdl4472hfjhfxszlonn52t'


# fix_list = init_game()

player1 = Player()
player2 = Player()
multiplayers = [player1, player2]
highscores = get_highscores()



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')




@app.route("/newgame", methods=['GET', 'POST'])
def newgame():
    session.pop('player', None)
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
    names = names
    if form.validate_on_submit():
        name = form.playername.data
        names.append(name)
        # multiplayers[int(id)-1].name = name
        flash(f'Good luck {name}!! ', 'dark')
        if id < num_players:
            names.append(name)
            print('Names after first name entry..')
            print(names)
            return redirect(url_for('enternames', id=id+1, num_players=num_players))
        elif id == num_players:
            names.append(name)
            print('Names after second name entry..')
            print(names)
            # multiplayers[int(id)-1].name = name
            return redirect(url_for('multiplayer', id=1, p_num=1, attempt=1))
        elif num_players == 1:
            return redirect(url_for('game', id=1, name=name, score=0, attempt=1))
    return render_template('enternames.html', form=form, id=id, num_players=num_players)




@app.route("/game/<int:id>/<name>/<int:score>/<int:attempt>", methods=['GET', 'POST'])
def game(id, name, score, attempt):
    form = AnswerForm()
    fix_list = init_game()
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
                    return redirect(url_for('game', id=id, name=name, score=score, attempt=2))
                else:
                    flash(f'You are correct {name}', 'success')
                    return redirect(url_for('game', id=id+1, name=name, score=score+plr_answer, attempt=1))
            elif attempt == 2:
                if plr_answer != correct_result:
                    flash(f'Wrong answer {name}', 'dark')
                    return redirect(url_for('game', id=id+1, name=name, score=score, attempt=1))
                else:
                    flash(f'You are correct {name}', 'success')
                    return redirect(url_for('game', id=id+1, name=name, score=score+1, attempt=1))
        elif id == 10:
            if attempt == 1:
                if plr_answer != correct_result:
                    flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                    return redirect(url_for('game', id=10, name=name, score=score, attempt=2))
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
                                   id=id, fix_list=fix_list, name=name)




@app.route("/multiplayer/<int:id>/<int:p_num>/<int:attempt>", methods=['GET', 'POST'])
def multiplayer(id, p_num, attempt):
    print(multiplayers)
    print('Names at multi..')
    print(names)
    form = AnswerForm()
    fix_list = init_game()
    if form.validate_on_submit():
        plr_answer = form.answer.data
        # name = get_player_name(multiplayers, int(p_num)-1)
        # name = multiplayers[int(p_num) -1].get_name()
        name = names[p_num -1]
        count = len(names)
        currId = id
        correct_result = get_correct_result(currId, fix_list)
        fixtures = 10
        """ play game only for count number of players """
        if p_num <= count:
            """ last fixture, last player """
            if id == fixtures and p_num == count:
                if attempt == 1:
                    if plr_answer != correct_result:
                        flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                        return redirect(url_for('multiplayer', id=id, p_num=p_num, attempt=2))
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
                        flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                        return redirect(url_for('multiplayer', id=id, p_num=p_num, attempt=2))
                    else:
                        flash(f'You are correct {name}', 'success')
                        multiplayers[p_num-1].inc_score(1, plr_answer)
                        return redirect(url_for('multiplayer', id=id+1, p_num=1, attempt=1))
                elif attempt == 2:
                    if plr_answer != correct_result:
                        flash(f'Wrong answer {name}', 'dark')
                        return redirect(url_for('multiplayer', id=id+1, p_num=1, attempt=1))
                    else:
                        flash(f'You are correct {name}', 'success')
                        multiplayers[p_num-1].inc_score(2, plr_answer)
                        return redirect(url_for('multiplayer', id=id+1, p_num=1, attempt=1))
            # fixture 1 to 9 all players excluding last player
            elif p_num < count:
                if attempt == 1:
                    if plr_answer != correct_result:
                        flash(f'Wrong answer {name}, you have one more attempt', 'dark')
                        return redirect(url_for('multiplayer', id=id, p_num=p_num, attempt=2))
                    else:
                        flash(f'You are correct {name}', 'success')
                        multiplayers[p_num-1].inc_score(1, plr_answer)
                        return redirect(url_for('multiplayer', id=id, p_num=p_num+1, attempt=1))
                elif attempt == 2:
                    if plr_answer != correct_result:
                        flash(f'Wrong answer {name}', 'dark')
                        return redirect(url_for('multiplayer', id=id, p_num=p_num+1, attempt=1))
                    else:
                        flash(f'You are correct {name}', 'success')
                        multiplayers[p_num-1].inc_score(2, plr_answer)
                        return redirect(url_for('multiplayer', id=id, p_num=p_num+1, attempt=1))
    return render_template('multiplayer.html', form=form,
                                   id=id, fix_list=fix_list, p_num=p_num, multiplayers=multiplayers, names=names)



@app.route("/winner/<string:name>/<int:score>", methods=['GET', 'POST'])
def winner(name, score):
    name = name
    score = score
    with open('scores.txt', 'a') as f:
        name = name
        score = score
        f.write(f'{name}:{score}\n')
    return render_template('winner.html', calc_winner=calc_winner, name=name, score=score)



@app.route("/winnermult", methods=['GET', 'POST'])
def winnermult():
    multiplayers.sort(key=lambda x: x.score, reverse=True)
    if len(multiplayers) > 1:
        calc_winner(multiplayers[0], multiplayers[1])
    return render_template('winnermult.html', multiplayers=multiplayers, calc_winner=calc_winner, highscores=highscores)



@app.route("/leaderboard", methods=['GET', 'POST'])
def leaderboard():
    updated_highscores = get_highscores()
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
