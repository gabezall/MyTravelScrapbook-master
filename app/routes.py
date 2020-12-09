from datetime import datetime
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, CreateAccountForm, AddNewArtistForm, AddNewVenueForm, AddEventForm
from app.models import ArtistToEvent, Artist, Venue, Event, City
from flask_login import current_user, login_user, logout_user, login_manager
from app.models import User
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db


@app.route('/')
@app.route('/index')
@login_required
def index():
    '''posts = [
        {
            'author': {'username': 'Quail'},
            'body': 'New Music Soon!'
        }]'''
    return render_template('index.html', title='Home')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Invalid username')
            return redirect(url_for('login'))
        if not user.check_password(form.password.data):
            flash('Invalid password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/new_artists', methods=('GET', 'POST'))
@login_required
def new_artists():
    form = AddNewArtistForm()

    if form.validate_on_submit():
        new_artist = form.new_artist.data
        if Artist.query.filter_by(name=new_artist).first() is not None:
            flash('Artist Already Exists')
            return redirect('artists/' + new_artist)
        flash('New Artist Page Created for {}'.format(form.new_artist.data))

        if City.query.filter_by(name=form.town.data).first() is not None:
            city = City.query.filter_by(name=form.town.data).first()
        else:
            city = City(name=form.town.data)
        db.session.add(city)
        db.session.commit()
        a1 = Artist(name=new_artist, description=form.description.data, cityID=city.id)
        db.session.add(a1)
        db.session.commit()
        return redirect('artists/' + new_artist)

    return render_template('new_artists.html', title='New Artist', form=form)


@app.route('/artists')
def artists():
    # artist = Artist.query.filter_by(StageName=form.ArtistName.data).first_or_404()
    artists = Artist.query.all()
    return render_template('artists.html', title='Artists', artists=artists)


@app.route('/artist_page')
@login_required
def artist_page():
    user = {'username': 'Jay'}
    return render_template('artist_page.html', title='Artist Page', user=user)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CreateAccountForm()
    if form.validate_on_submit():
        new_user = form.username.data
        if User.query.filter_by(username=new_user).first() is not None:
            flash('User Already Exists')
        else:
            flash("New User {} Created!".format(form.username.data))
            u1 = User(username=form.username.data, email=form.email.data)
            u1.set_password(form.password.data)
            db.session.add(u1)
            db.session.commit()
            return redirect('/index')

    return render_template('create_user.html', title="Create User", form=form)


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
    return render_template('base.html', title='DB Reset')


@app.route('/artists/<name>')
@login_required
def artist(name):
    artist = Artist.query.filter_by(name=name).first()
    events = Event.query.join(Event.artistsToEvent).filter_by(artistID=artist.id)

    return render_template('artist_page.html', title='Artist Page', artist=artist, events=events)


@app.route('/populate_db')
def populate_db():
    c1 = City(name='Ithaca, NY')
    c2 = City(name='Binghamton, NY')
    c3 = City(name='Syracuse, NY')
    c4 = City(name='Rochester, NY')
    db.session.add_all([c1, c2, c3, c4])
    db.session.commit()
    a1 = Artist(name="Driftwood", description="Folk Rock", cityID=c2.id)
    a2 = Artist(name="Quail", description="Funk and Brass", cityID=c1.id)
    a3 = Artist(name="VeeDaBee", description="Rock Band", cityID=c1.id)
    a4 = Artist(name="Danielle Ponder", description="Soul", cityID=c4.id)
    db.session.add_all([a1, a2, a3, a4])
    db.session.commit()
    v1 = Venue(name='The Haunt', cityID=c2.id)
    v2 = Venue(name='State Theater', cityID=c1.id)
    v3 = Venue(name='Stewart Park', cityID=c1.id)
    v4 = Venue(name='University', cityID=c2.id)
    v5 = Venue(name='Oncenter', cityID=c3.id)
    db.session.add_all([v1, v2, v3, v4, v5])
    db.session.commit()
    e1 = Event(name='Ithaca Porchfest', time=datetime(2020, 11, 5, 20, 00), venueID=v3.id)
    e2 = Event(name='2020 Tour', time=datetime(2020, 10, 20, 18, 00), venueID=v5.id)
    e3 = Event(name='Anniversary Concert', time=datetime(2020, 10, 20, 19, 00), venueID=v1.id)
    e4 = Event(name='2020 Tour', time=datetime(2020, 10, 29, 18, 00), venueID=v2.id)
    e5 = Event(name='2020 Tour', time=datetime(2020, 10, 20, 12, 00), venueID=v4.id)
    db.session.add_all([e1, e2, e3, e4, e5])
    db.session.commit()
    x1 = ArtistToEvent(artistID=a1.id, eventID=e3.id)
    x2 = ArtistToEvent(artistID=a2.id, eventID=e3.id)
    x3 = ArtistToEvent(artistID=a1.id, eventID=e1.id)
    x4 = ArtistToEvent(artistID=a3.id, eventID=e4.id)
    x5 = ArtistToEvent(artistID=a4.id, eventID=e5.id)
    x6 = ArtistToEvent(artistID=a3.id, eventID=e2.id)
    db.session.add_all([x1, x2, x3, x4, x5, x6])
    db.session.commit()
    u1 = User(username='Username', email=('SamepleEmail@email.com'), password_hash='Password')
    db.session.add(u1)
    db.session.commit()
    return render_template('base.html', title='Populate DB')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/new_venue', methods=('GET', 'POST'))
@login_required
def new_venue():
    form = AddNewVenueForm()
    form.city.choices = [(t.id, t.name) for t in City.query.all()]

    if form.validate_on_submit():
        name = form.venue.data
        if Venue.query.filter_by(name=name).first() is not None:
            flash('Venue Already Documented')
            return redirect('/index')
        flash('New Venue Documented'.format(form.venue.data))

        city = form.city.data

        v1 = Venue(name=name, cityID=city)
        db.session.add(v1)
        db.session.commit()
        return redirect('/index')

    return render_template('new_venue.html', title='New Artist', form=form)


@app.route('/new_event', methods=('GET', 'POST'))
@login_required
def new_event():
    form = AddEventForm()
    form.venue.choices = [(v.id, v.name) for v in Venue.query.all()]
    form.artists.choices = [(a.id, a.name) for a in Artist.query.all()]

    if form.validate_on_submit():
        event = form.event.data
        venue = form.venue.data
        time = form.time.data
        artists = form.artists.data
        e1 = Event(name=event, time=time, venueID=venue)
        db.session.add(e1)
        db.session.commit()
        for a in artists:
            a2e = ArtistToEvent(artistID=a, eventID=e1.id)
            db.session.add(a2e)
            db.session.commit()
        return redirect('/index')

    return render_template('new_event.html', title='New Artist', form=form)
