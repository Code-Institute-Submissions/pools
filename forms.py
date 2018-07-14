from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class PlayerNumForm(FlaskForm):
    players = IntegerField('Please enter number of players, maximum is five',
                           validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Confirm')

class NameForm(FlaskForm):
    playername = StringField('Name', validators=[DataRequired(), Length(min=2, max=10)])
    submit = SubmitField('Enter Name')

class AnswerForm(FlaskForm):
    answer = IntegerField('Answer', validators=[DataRequired(), NumberRange(min=1, max=3)])
    submit = SubmitField('Confirm')
