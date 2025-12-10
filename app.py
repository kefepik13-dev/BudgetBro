import os
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from plotly import io as pio
from plotly import graph_objects as go
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.secret_key = "mein_geheimes_passwort"
os.makedirs(app.instance_path, exist_ok=True)
db_path = os.path.join(app.instance_path, "budgetbro.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

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
        existing = User.query.filter_by(username=form.username.data).first()
        if existing:
            flash("Benutzername ist bereits vergeben.", "danger")
            return redirect(url_for('register'))

        user = User(
            username=form.username.data,
            password_hash=generate_password_hash(form.password.data),
        )
        db.session.add(user)
        db.session.commit()
        session['logged_in'] = True
        session['user_id'] = user.id
        session['username'] = user.username
    return render_template('register.html', form=form, active_page="register")

# Login-Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['logged_in'] = True
            session['user_id'] = user.id
            session['username'] = user.username
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
    sankey_html = build_financial_sankey()
    return render_template('dashboard.html', active_page="dashboard", graph_html=sankey_html)

# Sankey Fullscreen
@app.route('/sankey/full')
def sankey_full():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    sankey_html = build_financial_sankey()
    return render_template('sankey_full.html', active_page="dashboard", graph_html=sankey_html)

# Fluss
@app.route('/fluss')
def fluss():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('fluss.html', active_page="fluss")

# Berixchte
@app.route('/berichte')
def berichte():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('berichte.html', active_page="berichte")


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

# Sankey-Diagramm
def build_financial_sankey():
    """Erstellt ein Sankey-Diagramm für einfache Finanzströme."""
    labels = [
        "Nettoeinnahmen",
        "Gehalt",
        "Nebenjob",
        "Investments",
        "Fixkosten",
        "Wohnen",
        "Versicherungen",
        "Mobilität",
        "Variable Kosten",
        "Essen",
        "Freizeit",
        "Shopping",
        "Sparen & Anlegen",
        "Notgroschen",
        "Rente",
        "Kurzfristige Ziele",
        "Schulden",
        "Kreditkarte",
        "Studienkredit",
    ]

     # Farbpalette je Knoten (wird für Links aufgehellt)
    colors = [
        "rgba(33,150,243,0.9)",  # Nettoeinnahmen
        "rgba(76,175,80,0.9)",   # Gehalt
        "rgba(76,175,80,0.9)",   # Nebenjob
        "rgba(76,175,80,0.9)",   # Investments Income
        "rgba(255,152,0,0.9)",   # Fixkosten
        "rgba(255,87,34,0.9)",   # Wohnen
        "rgba(255,152,0,0.9)",   # Versicherungen
        "rgba(255,152,0,0.9)",   # Mobilität
        "rgba(156,39,176,0.9)",  # Variable Kosten
        "rgba(156,39,176,0.9)",  # Essen
        "rgba(156,39,176,0.9)",  # Freizeit
        "rgba(156,39,176,0.9)",  # Shopping
        "rgba(3,169,244,0.9)",   # Sparen & Anlegen
        "rgba(0,188,212,0.9)",   # Notgroschen
        "rgba(0,188,212,0.9)",   # Rente
        "rgba(0,188,212,0.9)",   # Kurzfristige Ziele
        "rgba(233,30,99,0.9)",   # Schulden
        "rgba(233,30,99,0.9)",   # Kreditkarte
        "rgba(233,30,99,0.9)",   # Studienkredit
    ]

     # Flüsse (Indices beziehen sich auf labels)
    sources = [
        1,  # Gehalt -> Nettoeinnahmen
        2,  # Nebenjob -> Nettoeinnahmen
        3,  # Investments Income -> Nettoeinnahmen
        0, 0, 0, 0,      # Nettoeinnahmen -> Hauptkategorien
        4, 4, 4,         # Fixkosten -> Unterkategorien
        8, 8, 8,         # Variable -> Unterkategorien
        12, 12, 12,      # Sparen -> Unterkategorien
        16, 16           # Schulden -> Unterkategorien
    ]
    targets = [
        0,  # Gehalt -> Nettoeinnahmen
        0,  # Nebenjob -> Nettoeinnahmen
        0,  # Investments -> Nettoeinnahmen
        4, 8, 12, 16,    # Nettoeinnahmen -> Fix, Var, Sparen, Schulden
        5, 6, 7,         # Fixkosten -> Wohnen, Versicherungen, Mobilität
        9, 10, 11,       # Variable -> Essen, Freizeit, Shopping
        13, 14, 15,      # Sparen -> Notgroschen, Rente, Kurzfristige Ziele
        17, 18           # Schulden -> Kreditkarte, Studienkredit
    ]

    values = [
        3200, 400, 150,     # Einnahmen
        1800, 600, 500, 250,  # Verteilung auf Kategorien
        900, 400, 500,      # Fixkosten Split
        250, 220, 130,      # Variable Split
        200, 150, 150,      # Sparen Split
        140, 110            # Schulden Split
    ]

    link_colors = [colors[src].replace("0.9", "0.45") for src in sources]

    fig = go.Figure(
        data=[
            go.Sankey(
                valueformat=",.0f",
                valuesuffix="€",
                node=dict(
                    pad=15,
                    thickness=18,
                    line=dict(color="rgba(0,0,0,0.15)", width=0.5),
                    label=labels,
                    color=colors,
                ),
                link=dict(
                    source=sources,
                    target=targets,
                    value=values,
                    color=link_colors,
                ),
            )
        ]
    )

    fig.update_layout(
        title_text="Finanzfluss (Monatlich)",
        font_size=12,
        margin=dict(l=10, r=10, t=40, b=10),
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs="cdn")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
