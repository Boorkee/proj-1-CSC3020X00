"""School pages. Students: Brooke Andrie"""
from app import app, db, sp
from app.models import User, School, TransportationCost
from app.forms import SignUpForm, LoginForm, SchoolCreateForm, SchoolUpdateForm, SchoolDeleteForm, TransportationCostForm
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user
import bcrypt
import sys

TYPES = ['elementary', 'middle', 'high school']
STATUSES = ['Open', 'Closed']

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html', title='School District')

@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if db.session.get(User, form.id.data):
            flash('That user ID is already taken.')
        elif len(form.passwd.data.encode()) > 72:
            flash('Password must be at most 72 bytes.')
        else:
            user = User(id=form.id.data, name=form.name.data, about=form.about.data,
                        passwd=bcrypt.hashpw(form.passwd.data.encode(), bcrypt.gensalt()))
            db.session.add(user)
            db.session.commit()
            flash('Account created. Please log in.')
            return redirect(url_for('login'))
    return render_template('signup.html', form=form, title='Sign Up')

@app.route('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.get(User, form.id.data)
        if user and len(form.passwd.data.encode()) <= 72 and bcrypt.checkpw(form.passwd.data.encode(), user.passwd):
            login_user(user)
            return redirect(url_for('list_schools'))
        flash('Incorrect user ID or password.')
    return render_template('login.html', form=form, title='Login')

@app.route('/users/signout', methods=['GET', 'POST'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/schools')
@login_required
def list_schools():
    return render_template('schools.html', schools=School.query.order_by(School.id).all(), types=TYPES, statuses=STATUSES, title='Schools')

def save_school(school, form):
    # The dropdown labels are stored as numbers in the database.
    school.name = form.name.data
    school.address = form.address.data
    school._type = TYPES.index(form.type.data)
    school.status = STATUSES.index(form.status.data)
    db.session.add(school)
    db.session.commit()

def fill_school(form, school):
    form.name.data = school.name
    form.address.data = school.address
    form.type.data = TYPES[school._type]
    form.status.data = STATUSES[school.status]

@app.route('/schools/create', methods=['GET', 'POST'])
@login_required
def create_school():
    form = SchoolCreateForm()
    if form.validate_on_submit():
        save_school(School(), form)
        return redirect(url_for('list_schools'))
    return render_template('school_crud.html', form=form, title='Create School')

@app.route('/schools/<int:id>', methods=['GET', 'POST'])
@login_required
def update_school(id):
    school = db.get_or_404(School, id)
    form = SchoolUpdateForm()
    if form.validate_on_submit():
        save_school(school, form)
        return redirect(url_for('list_schools'))
    if request.method == 'GET':
        fill_school(form, school)
    return render_template('school_crud.html', form=form, title='Update School')

@app.route('/schools/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_school(id):
    school = db.get_or_404(School, id)
    form = SchoolDeleteForm()
    if form.validate_on_submit():
        # Remove its transfer costs before removing the school.
        TransportationCost.query.filter((TransportationCost.from_school_id == id) | (TransportationCost.to_school_id == id)).delete(synchronize_session=False)
        db.session.delete(school)
        db.session.commit()
        return redirect(url_for('list_schools'))
    fill_school(form, school)
    return render_template('school_crud.html', form=form, title='Delete School')

@app.route('/schools/<int:id>/cost', methods=['GET', 'POST'])
@login_required
def school_transportation_cost(id):
    school = db.get_or_404(School, id)
    form = TransportationCostForm()
    form.from_school_id.data = id
    if form.validate_on_submit():
        target = db.session.get(School, form.to_school_id.data)
        if target is None or target.id == id:
            flash('Choose the ID of a different, existing school.')
        else:
            cost = db.session.get(TransportationCost, (id, target.id))
            if cost is None:
                cost = TransportationCost(from_school_id=id, to_school_id=target.id)
                db.session.add(cost)
            cost.cost = form.cost.data
            db.session.commit()
            flash('Transportation cost saved.')
            return redirect(url_for('school_transportation_cost', id=id))
    costs = TransportationCost.query.filter_by(from_school_id=id).all()
    return render_template('transpo_cost_crud.html', form=form, costs=costs, school=school, title='Transportation Costs')

@app.route('/schools/<int:id>/routes', methods=['GET', 'POST'])
@login_required
def school_routes(id):
    source = db.get_or_404(School, id)
    schools = School.query.filter_by(status=0).order_by(School.id).all()
    graph = {school.id: {} for school in schools}
    results = []
    if id not in graph:
        flash('Open this school before planning transfers.')
    else:
        for edge in TransportationCost.query.all():
            if edge.from_school_id in graph and edge.to_school_id in graph:
                graph[edge.from_school_id][edge.to_school_id] = edge.cost
        distances, paths = sp.dijkstra(graph, id)
        names = {school.id: school.name for school in schools}
        for school in schools:
            if school.id != id:
                reachable = distances[school.id] != sys.maxsize
                results.append((school.name, distances[school.id] if reachable else None,
                                ' → '.join(names[n] for n in paths[school.id] + [school.id]) if reachable else 'No route'))
    return render_template('routes.html', school=source, results=results, title='Cheapest Routes')
