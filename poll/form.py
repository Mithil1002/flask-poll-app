from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, IntegerField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from poll.models import User, Poll


class RegisterForm(FlaskForm):
    def validate_id(self, id_to_check):
        user = User.query.filter_by(id=id_to_check.data).first()
        if user:
            raise ValidationError('ID already exists! Please try a different ID')

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    # id = IntegerField(label='ID:', validators=[DataRequired()])
    username = StringField(label='User Name:', validators=[Length(min=2, max=50), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Length(max=30), validators.Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6, max=20), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class PollForm(FlaskForm):
    def validate_id(self, id_to_check):
        user = Poll.query.filter_by(id=id_to_check.data).first()
        if user:
            raise ValidationError('ID already exists! Please try a different ID')

    # id = IntegerField(label='ID:', validators=[DataRequired()])
    question = StringField(label='question', validators=[Length(min=2, max=350), DataRequired()])
    option1 = StringField(label='option1', validators=[Length(min=2, max=100), DataRequired()])
    option2 = StringField(label='option2', validators=[Length(min=2, max=100), DataRequired()])
    option3 = StringField(label='option3', validators=[Length(min=2, max=100), DataRequired()])
    option4 = StringField(label='option4', validators=[Length(min=2, max=100), DataRequired()])

    submit = SubmitField(label='Save Poll')


class LoginForm(FlaskForm):
    email = StringField(label='Email:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Log-in')


