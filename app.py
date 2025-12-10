from flask import Flask, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.secret_key = "mein_geheimes_passwort"

# LoginForm definieren
class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

# RegisterForm definieren
class RegisterForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrieren')

# Register-Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash("Registrierung erfolgreich! Du kannst dich jetzt einloggen.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form, active_page="register")

# Login-Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "admin" and form.password.data == "123456":
            session['logged_in'] = True  # Dummy-Session für Login
            flash("Login erfolgreich!", "success")
            return redirect(url_for('dashboard'))
            flash("Benutzername oder Passwort falsch!", "danger")
    return render_template('login.html', form=form, active_page="login")


# Startseite leitet automatisch auf Login weiter
@app.route('/')
def home():
    return redirect(url_for('register'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):  # Prüft, ob eingeloggt
        return redirect(url_for('login'))
    return render_template('dashboard.html', active_page="dashboard")

# Transaktionen
@app.route('/transaktionen')
def transaktionen():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('transaktionen.html', active_page="transaktionen")

# Ziele
@app.route('/ziele')
def ziele():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('ziele.html', active_page="ziele")

# Logout-Route 
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("Du wurdest ausgeloggt.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
