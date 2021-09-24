from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, ValidationError
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
moment = Moment(app)
bootstrap = Bootstrap(app)

def isEmail(form, field):
        if '@' not in field.data:
                raise ValidationError("Please include an '@' in the email address. '%s' is missing an '@'." %(field.data))

class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	email = StringField('What is your UofT Email address?', validators=[Required(), isEmail])
	submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name')
		old_email = session.get('email')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		if old_email is not None and old_email != form.email.data:
                        flash('Looks like you have changed your email!')
		session['name'] = form.name.data
		session['email'] = form.email.data
		return redirect(url_for('index'))
	return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'), email=session.get('email'))

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name, current_time=datetime.utcnow())
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

if __name__ == '__main__':
	app.run(debug=True)