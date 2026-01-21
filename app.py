import os
from datetime import date, datetime
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from plotly import io as pio
from plotly import graph_objects as go
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import FloatField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired
from budget_health import calculate_budget_health_score

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
    onboarding_done = db.Column(db.Boolean, default=False)


class OnboardingData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True, nullable=False)
    # Einnahmen
    income_salary = db.Column(db.Float, default=0)
    income_side = db.Column(db.Float, default=0)
    income_invest = db.Column(db.Float, default=0)
    # Fixkosten
    fixed_housing = db.Column(db.Float, default=0)
    fixed_insurance = db.Column(db.Float, default=0)
    fixed_mobility = db.Column(db.Float, default=0)
    # Variable Kosten
    var_food = db.Column(db.Float, default=0)
    var_fun = db.Column(db.Float, default=0)
    var_shopping = db.Column(db.Float, default=0)
    # Sparen & Anlegen
    save_emergency = db.Column(db.Float, default=0)
    save_retirement = db.Column(db.Float, default=0)
    save_goals = db.Column(db.Float, default=0)
    # Schulden
    debt_credit = db.Column(db.Float, default=0)
    debt_student = db.Column(db.Float, default=0)


class CustomCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    kind = db.Column(db.String(20), nullable=False)  # income | fix | variable | save | debt
    amount = db.Column(db.Float, nullable=False, default=0)


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    target_amount = db.Column(db.Float, nullable=False, default=0)
    saved_amount = db.Column(db.Float, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()

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


class OnboardingForm(FlaskForm):
    income_salary = FloatField("Gehalt (netto/Monat)", validators=[NumberRange(min=0)], default=3000)
    income_side = FloatField("Nebenjob", validators=[NumberRange(min=0)], default=400)
    income_invest = FloatField("Investments", validators=[NumberRange(min=0)], default=150)

    fixed_housing = FloatField("Wohnen", validators=[NumberRange(min=0)], default=900)
    fixed_insurance = FloatField("Versicherungen", validators=[NumberRange(min=0)], default=400)
    fixed_mobility = FloatField("Mobilität", validators=[NumberRange(min=0)], default=500)

    var_food = FloatField("Essen", validators=[NumberRange(min=0)], default=250)
    var_fun = FloatField("Freizeit", validators=[NumberRange(min=0)], default=220)
    var_shopping = FloatField("Shopping", validators=[NumberRange(min=0)], default=130)

    save_emergency = FloatField("Notgroschen", validators=[NumberRange(min=0)], default=200)
    save_retirement = FloatField("Rente", validators=[NumberRange(min=0)], default=150)
    save_goals = FloatField("Kurzfristige Ziele", validators=[NumberRange(min=0)], default=150)

    debt_credit = FloatField("Kreditkarte", validators=[NumberRange(min=0)], default=140)
    debt_student = FloatField("Studienkredit", validators=[NumberRange(min=0)], default=110)

    submit = SubmitField("Speichern und weiter")


class CustomCategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=120)])
    amount = FloatField("Betrag", validators=[InputRequired(), NumberRange(min=0)])
    kind = SelectField(
        "Kategorie",
        choices=[
            ("income", "Einnahme"),
            ("fix", "Fixkosten"),
            ("variable", "Variable Kosten"),
            ("save", "Sparen & Anlegen"),
            ("debt", "Schulden"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Hinzufügen")


class GoalForm(FlaskForm):
    title = StringField("Zielname", validators=[DataRequired(), Length(min=2, max=120)])
    target_amount = FloatField("Zielbetrag (€)", validators=[InputRequired(), NumberRange(min=0.01)])
    saved_amount = FloatField("Bereits gespart (€)", validators=[InputRequired(), NumberRange(min=0)])
    submit = SubmitField("Ziel speichern")


# Register-Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        session.pop('_flashes', None)
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
        # Auto-Login und Onboarding starten
        session['logged_in'] = True
        session['user_id'] = user.id
        session['username'] = user.username
        flash("Registrierung erfolgreich! Lass uns mit dem Onboarding starten.", "success")
        return redirect(url_for('onboarding'))
    return render_template('register.html', form=form, active_page="register")

# Login-Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        session.pop('_flashes', None)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['logged_in'] = True
            session['user_id'] = user.id
            session['username'] = user.username
            flash("Login erfolgreich!", "success")
            if not user.onboarding_done:
                return redirect(url_for('onboarding'))
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
    user = User.query.get(session.get('user_id'))
    if user and not user.onboarding_done:
        return redirect(url_for('onboarding'))
    onboarding = None
    if user:
        onboarding = OnboardingData.query.filter_by(user_id=user.id).first()
    sankey_html, totals = build_financial_sankey(onboarding)
    goal = Goal.query.filter_by(user_id=user.id).order_by(Goal.id.desc()).first()
    return render_template('dashboard.html', active_page="dashboard", graph_html=sankey_html, goal=goal)


@app.route('/sankey/full')
def sankey_full():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    user = User.query.get(session.get('user_id'))
    if user and not user.onboarding_done:
        return redirect(url_for('onboarding'))
    onboarding = None
    if user:
        onboarding = OnboardingData.query.filter_by(user_id=user.id).first()
    sankey_html, _ = build_financial_sankey(onboarding)
    return render_template('sankey_full.html', active_page="dashboard", graph_html=sankey_html)

# Flow / Kategorien
@app.route('/fluss', methods=['GET', 'POST'])
def fluss():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    user = User.query.get(session.get('user_id'))
    if user and not user.onboarding_done:
        return redirect(url_for('onboarding'))

    onboarding = OnboardingData.query.filter_by(user_id=user.id).first()
    onboarding_form = OnboardingForm(obj=onboarding)
    custom_form = CustomCategoryForm()
    customs = CustomCategory.query.filter_by(user_id=user.id).all()

    # Handle onboarding update
    if "income_salary" in request.form and onboarding_form.validate_on_submit():
        data = onboarding or OnboardingData(user_id=user.id)
        data.income_salary = onboarding_form.income_salary.data or 0
        data.income_side = onboarding_form.income_side.data or 0
        data.income_invest = onboarding_form.income_invest.data or 0
        data.fixed_housing = onboarding_form.fixed_housing.data or 0
        data.fixed_insurance = onboarding_form.fixed_insurance.data or 0
        data.fixed_mobility = onboarding_form.fixed_mobility.data or 0
        data.var_food = onboarding_form.var_food.data or 0
        data.var_fun = onboarding_form.var_fun.data or 0
        data.var_shopping = onboarding_form.var_shopping.data or 0
        data.save_emergency = onboarding_form.save_emergency.data or 0
        data.save_retirement = onboarding_form.save_retirement.data or 0
        data.save_goals = onboarding_form.save_goals.data or 0
        data.debt_credit = onboarding_form.debt_credit.data or 0
        data.debt_student = onboarding_form.debt_student.data or 0
        db.session.add(data)
        db.session.commit()
        flash("Basiswerte aktualisiert.", "success")
        return redirect(url_for('fluss'))

    # Handle custom category add
    if "name" in request.form and custom_form.validate_on_submit():
        cat = CustomCategory(
            user_id=user.id,
            name=custom_form.name.data,
            kind=custom_form.kind.data,
            amount=custom_form.amount.data or 0,
        )
        db.session.add(cat)
        db.session.commit()
        flash("Kategorie hinzugefügt.", "success")
        return redirect(url_for('fluss'))

    return render_template(
        'fluss.html',
        active_page="fluss",
        onboarding_form=onboarding_form,
        custom_form=custom_form,
        customs=customs,
    )


@app.route('/fluss/delete/<int:cat_id>')
def delete_category(cat_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    cat = CustomCategory.query.filter_by(id=cat_id, user_id=user_id).first()
    if not cat:
        flash("Kategorie nicht gefunden.", "warning")
        return redirect(url_for('fluss'))
    db.session.delete(cat)
    db.session.commit()
    flash("Kategorie gelöscht.", "info")
    return redirect(url_for('fluss'))

# Ziele
@app.route('/ziele', methods=['GET', 'POST'])
def ziele():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    user = User.query.get(session.get('user_id'))
    if user and not user.onboarding_done:
        return redirect(url_for('onboarding'))
    goal = Goal.query.filter_by(user_id=user.id).order_by(Goal.id.desc()).first()
    form = GoalForm(obj=goal)

    if form.validate_on_submit():
        if goal:
            goal.title = form.title.data
            goal.target_amount = form.target_amount.data
            goal.saved_amount = form.saved_amount.data
        else:
            goal = Goal(
                user_id=user.id,
                title=form.title.data,
                target_amount=form.target_amount.data,
                saved_amount=form.saved_amount.data,
            )
            db.session.add(goal)
        db.session.commit()
        flash("Ziel gespeichert.", "success")
        return redirect(url_for('ziele'))

    return render_template('ziele.html', active_page="ziele", form=form, goal=goal)

# Logout-Route 
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)
    flash("Du wurdest ausgeloggt.", "info")
    return redirect(url_for('login'))


@app.route('/onboarding', methods=['GET', 'POST'])
def onboarding():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    user = User.query.get(session.get('user_id'))
    if not user:
        flash("Bitte erneut einloggen.", "warning")
        return redirect(url_for('login'))
    if user.onboarding_done:
        return redirect(url_for('dashboard'))

    existing = OnboardingData.query.filter_by(user_id=user.id).first()
    form = OnboardingForm(obj=existing)

    if form.validate_on_submit():
        data = existing or OnboardingData(user_id=user.id)
        # Einnahmen
        data.income_salary = form.income_salary.data or 0
        data.income_side = form.income_side.data or 0
        data.income_invest = form.income_invest.data or 0
        # Fixkosten
        data.fixed_housing = form.fixed_housing.data or 0
        data.fixed_insurance = form.fixed_insurance.data or 0
        data.fixed_mobility = form.fixed_mobility.data or 0
        # Variable
        data.var_food = form.var_food.data or 0
        data.var_fun = form.var_fun.data or 0
        data.var_shopping = form.var_shopping.data or 0
        # Sparen
        data.save_emergency = form.save_emergency.data or 0
        data.save_retirement = form.save_retirement.data or 0
        data.save_goals = form.save_goals.data or 0
        # Schulden
        data.debt_credit = form.debt_credit.data or 0
        data.debt_student = form.debt_student.data or 0

        db.session.add(data)
        user.onboarding_done = True
        db.session.commit()
        flash("Onboarding gespeichert. Willkommen!", "success")
        return redirect(url_for('dashboard'))

    return render_template('onboarding.html', form=form, active_page="dashboard")


@app.route('/budget-health')
def budget_health():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    user = User.query.get(session.get('user_id'))
    if user and not user.onboarding_done:
        return redirect(url_for('onboarding'))
    
    onboarding = None
    if user:
        onboarding = OnboardingData.query.filter_by(user_id=user.id).first()
    if not onboarding:
        flash("Bitte fülle zuerst das Onboarding aus.", "warning")
        return redirect(url_for('onboarding'))
    
    # Calculate totals from onboarding data
    monthly_income = (onboarding.income_salary or 0) + (onboarding.income_side or 0) + (onboarding.income_invest or 0)
    monthly_fixed_costs = (onboarding.fixed_housing or 0) + (onboarding.fixed_insurance or 0) + (onboarding.fixed_mobility or 0)
    monthly_savings = (onboarding.save_emergency or 0) + (onboarding.save_retirement or 0) + (onboarding.save_goals or 0)
    
    # Add custom categories
    customs_income = CustomCategory.query.filter_by(kind="income", user_id=user.id).all()
    customs_fix = CustomCategory.query.filter_by(kind="fix", user_id=user.id).all()
    customs_save = CustomCategory.query.filter_by(kind="save", user_id=user.id).all()
    
    # Summe der custom income categories
    for cat in customs_income:
        monthly_income += cat.amount
    
    # Summe der custom fix categories
    for cat in customs_fix:
        monthly_fixed_costs += cat.amount
    
    # Summe der custom save categories
    for cat in customs_save:
        monthly_savings += cat.amount
    
    # Calculate budget health score
    score_data = calculate_budget_health_score({
        "monthly_income": monthly_income,
        "monthly_fixed_costs": monthly_fixed_costs,
        "monthly_savings": monthly_savings,
    })
    
    return render_template('budget_health.html', active_page="budget_health", score_data=score_data)


def build_financial_sankey(onboarding=None):
    """Erstellt ein Sankey-Diagramm für einfache Finanzströme, personalisiert nach Onboarding."""
    labels = []
    colors = []

    def add_node(label, color):
        labels.append(label)
        colors.append(color)
        return len(labels) - 1

    # Basis-Knoten
    idx_net = add_node("Nettoeinnahmen", "rgba(33,150,243,0.9)")
    idx_salary = add_node("Gehalt", "rgba(76,175,80,0.9)")
    idx_side = add_node("Nebenjob", "rgba(76,175,80,0.9)")
    idx_invest = add_node("Investments", "rgba(76,175,80,0.9)")

    idx_fix = add_node("Fixkosten", "rgba(255,152,0,0.9)")
    idx_housing = add_node("Wohnen", "rgba(255,87,34,0.9)")
    idx_insurance = add_node("Versicherungen", "rgba(255,152,0,0.9)")
    idx_mobility = add_node("Mobilität", "rgba(255,152,0,0.9)")

    idx_var = add_node("Variable Kosten", "rgba(156,39,176,0.9)")
    idx_food = add_node("Essen", "rgba(156,39,176,0.9)")
    idx_fun = add_node("Freizeit", "rgba(156,39,176,0.9)")
    idx_shop = add_node("Shopping", "rgba(156,39,176,0.9)")

    idx_save = add_node("Sparen & Anlegen", "rgba(3,169,244,0.9)")
    idx_emerg = add_node("Notgroschen", "rgba(0,188,212,0.9)")
    idx_ret = add_node("Rente", "rgba(0,188,212,0.9)")
    idx_goals = add_node("Kurzfristige Ziele", "rgba(0,188,212,0.9)")

    idx_debt = add_node("Schulden", "rgba(233,30,99,0.9)")
    idx_cc = add_node("Kreditkarte", "rgba(233,30,99,0.9)")
    idx_student = add_node("Studienkredit", "rgba(233,30,99,0.9)")

   
    def v(val, default):
        return float(val) if val is not None else default

    income_salary = v(getattr(onboarding, "income_salary", None), 3200)
    income_side = v(getattr(onboarding, "income_side", None), 400)
    income_invest = v(getattr(onboarding, "income_invest", None), 150)

    fixed_housing = v(getattr(onboarding, "fixed_housing", None), 900)
    fixed_insurance = v(getattr(onboarding, "fixed_insurance", None), 400)
    fixed_mobility = v(getattr(onboarding, "fixed_mobility", None), 500)

    var_food = v(getattr(onboarding, "var_food", None), 250)
    var_fun = v(getattr(onboarding, "var_fun", None), 220)
    var_shopping = v(getattr(onboarding, "var_shopping", None), 130)

    save_emergency = v(getattr(onboarding, "save_emergency", None), 200)
    save_retirement = v(getattr(onboarding, "save_retirement", None), 150)
    save_goals = v(getattr(onboarding, "save_goals", None), 150)

    debt_credit = v(getattr(onboarding, "debt_credit", None), 140)
    debt_student = v(getattr(onboarding, "debt_student", None), 110)

    # Custom categories
    customs_income = []
    customs_fix = []
    customs_var = []
    customs_save = []
    customs_debt = []
    
    if onboarding:
        user_id = onboarding.user_id
        customs_income = CustomCategory.query.filter_by(kind="income", user_id=user_id).all()
        customs_fix = CustomCategory.query.filter_by(kind="fix", user_id=user_id).all()
        customs_var = CustomCategory.query.filter_by(kind="variable", user_id=user_id).all()
        customs_save = CustomCategory.query.filter_by(kind="save", user_id=user_id).all()
        customs_debt = CustomCategory.query.filter_by(kind="debt", user_id=user_id).all()

    income_salary = max(0, income_salary)
    income_side = max(0, income_side)
    income_invest = max(0, income_invest)

    fixed_housing = max(0, fixed_housing)
    fixed_insurance = max(0, fixed_insurance)
    fixed_mobility = max(0, fixed_mobility)

    var_food = max(0, var_food)
    var_fun = max(0, var_fun)
    var_shopping = max(0, var_shopping)

    save_emergency = max(0, save_emergency)
    save_retirement = max(0, save_retirement)
    save_goals = max(0, save_goals)

    debt_credit = max(0, debt_credit)
    debt_student = max(0, debt_student)

    # Summe der custom categories berechnen
    custom_fix_total = 0
    for cat in customs_fix:
        custom_fix_total += cat.amount
    
    custom_var_total = 0
    for cat in customs_var:
        custom_var_total += cat.amount
    
    custom_save_total = 0
    for cat in customs_save:
        custom_save_total += cat.amount
    
    custom_debt_total = 0
    for cat in customs_debt:
        custom_debt_total += cat.amount
    
    total_fix = fixed_housing + fixed_insurance + fixed_mobility + custom_fix_total
    total_var = var_food + var_fun + var_shopping + custom_var_total
    total_save = save_emergency + save_retirement + save_goals + custom_save_total
    total_debt = debt_credit + debt_student + custom_debt_total

    sources, targets, values = [], [], []

    def link(src, tgt, val):
        sources.append(src)
        targets.append(tgt)
        values.append(max(val, 0))

    # Incomes -> Net
    link(idx_salary, idx_net, income_salary)
    link(idx_side, idx_net, income_side)
    link(idx_invest, idx_net, income_invest)

    for c in customs_income:
        c_idx = add_node(c.name, "rgba(76,175,80,0.9)")
        link(c_idx, idx_net, c.amount)

    # Net -> main categories
    link(idx_net, idx_fix, total_fix)
    link(idx_net, idx_var, total_var)
    link(idx_net, idx_save, total_save)
    link(idx_net, idx_debt, total_debt)

    # Fix splits
    link(idx_fix, idx_housing, fixed_housing)
    link(idx_fix, idx_insurance, fixed_insurance)
    link(idx_fix, idx_mobility, fixed_mobility)
    for c in customs_fix:
        c_idx = add_node(c.name, "rgba(255,152,0,0.9)")
        link(idx_fix, c_idx, c.amount)

    # Variable splits
    link(idx_var, idx_food, var_food)
    link(idx_var, idx_fun, var_fun)
    link(idx_var, idx_shop, var_shopping)
    for c in customs_var:
        c_idx = add_node(c.name, "rgba(156,39,176,0.9)")
        link(idx_var, c_idx, c.amount)

    # Saving splits
    link(idx_save, idx_emerg, save_emergency)
    link(idx_save, idx_ret, save_retirement)
    link(idx_save, idx_goals, save_goals)
    for c in customs_save:
        c_idx = add_node(c.name, "rgba(3,169,244,0.9)")
        link(idx_save, c_idx, c.amount)

    # Debt splits
    link(idx_debt, idx_cc, debt_credit)
    link(idx_debt, idx_student, debt_student)
    for c in customs_debt:
        c_idx = add_node(c.name, "rgba(233,30,99,0.9)")
        link(idx_debt, c_idx, c.amount)

    # Farben für die Links erstellen
    link_colors = []
    for src in sources:
        color = colors[src].replace("0.9", "0.45")
        link_colors.append(color)

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

    # Summe der custom income categories
    custom_income_total = 0
    for cat in customs_income:
        custom_income_total += cat.amount
    
    income_total = income_salary + income_side + income_invest + custom_income_total
    totals = {
        "income_total": income_total,
        "fix_total": total_fix,
        "var_total": total_var,
        "save_total": total_save,
        "debt_total": total_debt,
    }

    return pio.to_html(fig, full_html=False, include_plotlyjs="cdn"), totals


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
