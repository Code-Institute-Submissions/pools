from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class PlayerNumForm(FlaskForm):
    players = IntegerField('Enter 1 for 1 Player mode or 2 for 2 Player mode',
                           validators=[DataRequired(), NumberRange(min=1, max=2)])
    submit = SubmitField('Confirm')

class NameForm(FlaskForm):
    playername = StringField('Name', validators=[DataRequired(), Length(min=2, max=16)])
    submit = SubmitField('Enter Name')

class AnswerForm(FlaskForm):
    answer = IntegerField('Enter answer', validators=[DataRequired(), NumberRange(min=1, max=3)])
    submit = SubmitField('Confirm')
