from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(message="Please enter your First Name.")])
    last_name = StringField('Last Name',
                            validators=[DataRequired(message="Please enter your Last Name.")])
    email = StringField('Email',
                        validators=[DataRequired(message="Please provide an email."),
                                    Email(message="A valid email address is required")])
    password = PasswordField('Password',
                             validators=[DataRequired(message="Please provide a password."),
                                         Length(min=6, message="Password must be at least 6 characters.")])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(message="Please provide your email address."),
                                    Email("Please make sure that it is a valid email address")]
                        )
    password = PasswordField('Password',
                             validators=[DataRequired(message="Please provide a password."),
                                         Length(min=6, message="Password must be at least 6 characters.")]
                             )
    submit = SubmitField("Sign In")


class AddressForm(FlaskForm):
    address = StringField('Address',
                          validators=[DataRequired("Please enter an address.")])
    submit = SubmitField("Search")