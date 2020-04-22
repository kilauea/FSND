#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from sqlalchemy import text, func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  venues = Venue.query.order_by(Venue.create_time.desc()).limit(10).all()
  artists = Artist.query.order_by(Artist.create_time.desc()).limit(10).all()
  return render_template('pages/home.html', venues=venues, artists=artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # Query the venues grouped by location City/State
  locations_query = Venue.query.with_entities(func.count(Venue.id), Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()

  if locations_query == None:
    return not_found_error('No venues found')

  today = datetime.now()
  data = []

  for location in locations_query:
    # Query all the venues from each location
    venues_location = Venue.query.filter_by(state=location.state).filter_by(city=location.city).all()
    venues_data = []
    for venue in venues_location:
      venues_data.append({
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': len(Show.query.join(Venue).filter(Show.venue_id == venue.id).filter(Show.start_time >= today).all())
      })
    data.append({
      'city': location.city,
      'state': location.state,
      'venues': venues_data
    })

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # Implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  venues_query = Venue.query.filter(Venue.name.ilike('%' + request.form.get('search_term') + '%'))
  data = []
  today = datetime.now()
  for venue in venues_query:
    data.append({
      'id': venue.id,
      'name': venue.name,
      'num_upcoming_shows': Show.query.join(Artist).filter(Show.venue_id == venue.id).filter(Show.start_time >= today).count()
    })
  response = {
    'count': venues_query.count(),
    'data': data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # Get the venue by its id
  venue_query = Venue.query.get(venue_id)

  if venue_query == None:
    return not_found_error('Venue %d not found' % venue_id)

  today = datetime.now()
  past_shows_query = Show.query.join(Artist).filter(Show.venue_id == venue_id).filter(Show.start_time < today).all()
  past_shows = []
  for el in past_shows_query:
    past_shows.append({
      'artist_id' : el.artist_id,
      'artist_name' : el.artist.name,
      'artist_image_link': el.artist.image_link,
      'start_time': el.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })
  upcoming_shows_query = Show.query.join(Artist).filter(Show.venue_id == venue_id).filter(Show.start_time >= today).all()
  upcoming_shows = []
  for el in upcoming_shows_query:
    upcoming_shows.append({
      'artist_id' : el.artist_id,
      'artist_name' : el.artist.name,
      'artist_image_link': el.artist.image_link,
      'start_time': el.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })

  data = {
    'id': venue_query.id,
    'name': venue_query.name,
    'city': venue_query.city,
    'state': venue_query.state,
    'address': venue_query.address,
    'phone': venue_query.phone,
    'genres': venue_query.genres[1:-1].replace('"', '').split(','),
    'image_link': venue_query.image_link,
    'facebook_link' : venue_query.facebook_link,
    'website': venue_query.website,
    'seeking_talent': venue_query.seeking_talent,
    'seeking_description': venue_query.seeking_description,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'upcoming_shows_count': len(upcoming_shows)
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)
  if not form.validate():
    errors = ''
    if form.errors:
      for key, value in form.errors.items():
        errors += ' -' + key + ': ' + value[0]
    if errors:
      flash('Error! Venue ' + request.form['name'] + ' could not be created!' + errors)
      return render_template('forms/new_venue.html', form=form)
  else:
    try:
      venue = Venue(
        name = request.form['name'],
        city = request.form['city'],
        state = request.form['state'],
        address = request.form['address'],
        phone = request.form['phone'],
        genres = request.form.getlist('genres'),
        image_link = request.form['image_link'],
        facebook_link = request.form['facebook_link'],
        website = request.form['website'],
        seeking_talent = 'seeking_talent' in request.form,
        seeking_description = request.form['seeking_description']
      )
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully created!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('Error! Venue ' + request.form['name'] + ' could not be created!')
    finally:
      db.session.close()

 # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  name = Venue.query.get(venue_id).name
  error = False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue "' + name + '" was successfully deleted!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
    flash('Venue "' + name + '" could not be deleted! It may have some shows.')
  finally:
    db.session.close()

  return jsonify(success = not error)

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # Query all the artists ordered by id
  artists_query = Artist.query.with_entities(Artist.id, Artist.name).order_by(Artist.id.asc()).all()

  if artists_query == None:
    return not_found_error('No artists found')

  data = []
  for artist in artists_query:
    data.append({
      'id': artist.id,
      'name': artist.name
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # Implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  artists_query = Artist.query.filter(Artist.name.ilike('%' + request.form.get('search_term') + '%'))
  data = []
  today = datetime.now()
  for artist in artists_query:
    data.append({
      'id': artist.id,
      'name': artist.name,
      'num_upcoming_shows': Show.query.join(Venue).filter(Show.artist_id == artist.id).filter(Show.start_time >= today).count()
    })
  response = {
    'count': artists_query.count(),
    'data': data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # Get the artist by its id
  artist_query = Artist.query.get(artist_id)

  if artist_query == None:
    return not_found_error('Artist %d not found' % artist_id)

  today = datetime.now()
  past_shows_query = Show.query.join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time < today).all()
  past_shows = []
  for el in past_shows_query:
    past_shows.append({
      'venue_id' : el.venue_id,
      'venue_name' : el.venue.name,
      'venue_image_link': el.venue.image_link,
      'start_time': el.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })
  upcoming_shows_query = Show.query.join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time >= today).all()
  upcoming_shows = []
  for el in upcoming_shows_query:
    upcoming_shows.append({
      'venue_id' : el.venue_id,
      'venue_name' : el.venue.name,
      'venue_image_link': el.venue.image_link,
      'start_time': el.start_time.strftime('%Y-%m-%d %H:%M:%S')
    })

  data = {
    'id': artist_query.id,
    'name': artist_query.name,
    'city': artist_query.city,
    'state': artist_query.state,
    'phone': artist_query.phone,
    'genres': artist_query.genres[1:-1].replace('"', '').split(','),
    'image_link': artist_query.image_link,
    'facebook_link' : artist_query.facebook_link,
    'website': artist_query.website,
    'seeking_venue': artist_query.seeking_venue,
    'seeking_description': artist_query.seeking_description,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'upcoming_shows_count': len(upcoming_shows)
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO: populate form with fields from artist with ID <artist_id>
  # Get the artist by its id
  artist_query = Artist.query.get(artist_id)

  if artist_query == None:
    return not_found_error('Artist %d not found' % artist_id)

  form = ArtistForm()
  form.name.default = artist_query.name
  if artist_query.genres:
    form.genres.default = artist_query.genres[1:-1].replace('"', '').split(',')
  form.city.default = artist_query.city
  form.state.default = artist_query.state
  form.phone.default = artist_query.phone
  if artist_query.image_link:
    form.image_link.default = artist_query.image_link
  if artist_query.facebook_link:
    form.facebook_link.default = artist_query.facebook_link
  if artist_query.website:
    form.website.default = artist_query.website
  form.seeking_venue.default = artist_query.seeking_venue
  form.seeking_description.default = artist_query.seeking_description
  form.process()

  artist = {
    'id': artist_query.id,
    'name': artist_query.name,
    'city': artist_query.city,
    'state': artist_query.state,
    'phone': artist_query.phone,
    'genres': artist_query.genres[1:-1].replace('"', '').split(','),
    'image_link': artist_query.image_link,
    'facebook_link' : artist_query.facebook_link,
    'website': artist_query.website,
    'seeking_venue': artist_query.seeking_venue,
    'seeking_description': artist_query.seeking_description
  }

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist_query = Artist.query.get(artist_id)

  if artist_query == None:
    return not_found_error('Artist %d not found' % artist_id)

  try:
    artist_query.name = request.form['name']
    artist_query.city = request.form['city']
    artist_query.state = request.form['state']
    artist_query.phone = request.form['phone']
    artist_query.genres = request.form.getlist('genres')
    artist_query.image_link = request.form['image_link']
    artist_query.facebook_link = request.form['facebook_link']
    artist_query.website = request.form['website']
    artist_query.seeking_venue = 'seeking_venue' in request.form
    artist_query.seeking_description = request.form['seeking_description']
   
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('Error! Artist ' + request.form['name'] + ' could not be updated.') 
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # TODO: populate form with values from venue with ID <venue_id>
  venue_query = Venue.query.get(venue_id)

  if venue_query == None:
    return not_found_error('Venue %d not found' % venue_id)

  form = VenueForm()
  form.name.default = venue_query.name
  if venue_query.genres:
    form.genres.default = venue_query.genres[1:-1].replace('"', '').split(',')
  form.address.default = venue_query.address
  form.city.default = venue_query.city
  form.state.default = venue_query.state
  form.phone.default = venue_query.phone
  if venue_query.image_link:
    form.image_link.default = venue_query.image_link
  if venue_query.facebook_link:
    form.facebook_link.default = venue_query.facebook_link
  if venue_query.website:
    form.website.default = venue_query.website
  form.seeking_talent.checked = venue_query.seeking_talent
  form.seeking_description.default = venue_query.seeking_description
  form.process()

  venue = {
    'id': venue_query.id,
    'name': venue_query.name,
    'address': venue_query.address,
    'city': venue_query.city,
    'state': venue_query.state,
    'phone': venue_query.phone,
    'genres': venue_query.genres[1:-1].replace('"', '').split(','),
    'image_link': venue_query.image_link,
    'facebook_link' : venue_query.facebook_link,
    'website': venue_query.website,
    'seeking_talent': venue_query.seeking_talent,
    'seeking_description': venue_query.seeking_description
  }
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue_query = Venue.query.get(venue_id)

  if venue_query == None:
    return not_found_error('Venue %d not found' % venue_id)

  try:
    venue_query.name = request.form['name']
    venue_query.address = request.form['address']
    venue_query.city = request.form['city']
    venue_query.state = request.form['state']
    venue_query.phone = request.form['phone']
    venue_query.genres = request.form.getlist('genres')
    venue_query.image_link = request.form['image_link']
    venue_query.facebook_link = request.form['facebook_link']
    venue_query.website = request.form['website']
    venue_query.seeking_talent = 'seeking_talent' in request.form
    venue_query.seeking_description = request.form['seeking_description']
   
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('Error! Venue ' + request.form['name'] + ' could not be updated.') 
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  if not form.validate():
    errors = ''
    if form.errors:
      for key, value in form.errors.items():
        errors += ' -' + key + ': ' + value[0]
    if errors:
      flash('Error! Artist ' + request.form['name'] + ' could not be created!' + errors)
      return render_template('forms/new_artist.html', form=form)
  else:
    try:
      artist = Artist(
        name = request.form['name'],
        city = request.form['city'],
        state = request.form['state'],
        phone = request.form['phone'],
        genres = request.form.getlist('genres'),
        image_link = request.form['image_link'],
        facebook_link = request.form['facebook_link'],
        website = request.form['website'],
        seeking_venue = 'seeking_venue' in request.form,
        seeking_description = equest.form['seeking_description']
      )
      db.session.add(artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully created!')
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash('Error! Artist ' + request.form['name'] + ' could not be created!')
    finally:
      db.session.close()

  return render_template('pages/home.html')

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  # Complete this endpoint for taking a artist_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  name = Artist.query.get(artist_id).name
  try:
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
    flash('Artist "' + name + '" was successfully deleted!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    error = True
    flash('Artist "' + name + '" could not be deleted! It may have some shows.')
  finally:
    db.session.close()

  return jsonify(success = not error)

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # Get all the shows ordered by state_data
  query = Show.query.join(Venue).filter(Show.venue_id == Venue.id).\
    join(Artist).filter(Show.artist_id == Artist.id).\
    with_entities(Venue.id, Venue.name, Artist.id, Artist.name, Artist.image_link, Show.start_time).\
    order_by(Show.start_time.asc())

  data = []
  for el in query:
    newshow = {
      "venue_id": el[0],
      "venue_name": el[1],
      "artist_id": el[2],
      "artist_name": el[3],
      "artist_image_link": el[4],
      "start_time": el[5].strftime('%Y-%m-%d %H:%M:%S')
    }
    data.append(newshow)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    show = Show(
      artist_id = request.form['artist_id'],
      venue_id = request.form['venue_id'],
      start_time = request.form['start_time']
    )
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('Error! Show could not be listed!')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

def add_venues():
  '''
  Function for adding the mockup date to the Venue table
  '''
  data1={
    #"id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  }
  data2={
    #"id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  }
  data3={
    #"id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  }

  try:
    venues = [Venue(**data1), Venue(**data2), Venue(**data3)]
    db.session.add_all(venues)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

def add_artist():
  '''
  Function for adding the mockup date to the Artist table
  '''
  dummy={
    "name": "dummy",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "000-000-0000",
    "seeking_venue": False,
  }
  data1={
    #"id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  }
  data2={
    #"id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  }
  data3={
    #"id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  }

  try:
    artists = [Artist(**dummy), Artist(**dummy), Artist(**dummy), Artist(**data1), Artist(**data2), Artist(**data3)]
    db.session.add_all(artists)
    db.session.commit()
    Artist.query.filter_by(name='dummy').delete()
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

def add_shows():
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]

  try:
    shows = []
    for el in data:
      del el['venue_name']
      del el['artist_name']
      del el['artist_image_link']
      shows.append(Show(**el))
    db.session.add_all(shows)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

POPULATE = False
if POPULATE == True:
  db.drop_all(app=app)
  db.create_all(app=app)
  add_venues()
  add_artist()
  add_shows()

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
