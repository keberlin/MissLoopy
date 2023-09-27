import sys, logging

from functools import wraps
from flask import Flask, redirect, render_template, request, send_from_directory, g, jsonify

from html import *
from handlers_html import *
from handlers_json import *
from database import db, MISSLOOPY_DB_URI
from model import *

logging.basicConfig(filename='/var/log/missloopy/log', level=logging.DEBUG)

#logger = logging.getLogger('missloopy')

PAGE_SIZE = 20

def debug(str):
  logging.debug(request.remote_addr + ' ' + str)

def info(str):
  logging.info(request.remote_addr + ' ' + str)

class MyFlask(Flask):
  def get_send_file_max_age(self, name):
    if re.search('\.(js|css|png|jpg|ico|woff|ttf|eof|svg)$', name.lower()):
      return 28*24*60*60 # 28 days
    return Flask.get_send_file_max_age(self, name)

# Jinja filters
def bitcompare(a,b):
  return a & b

# Route decorators
def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    g.entry = Authenticate(request.cookies, request.remote_addr)
    return f(*args, **kwargs)
  return decorated_function

# Flask application
def create_app():
  app = MyFlask(__name__)
  app.config['DEBUG'] = True
  # Databases
  app.config['SQLALCHEMY_ECHO'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = MISSLOOPY_DB_URI
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  app.jinja_env.filters['bitcompare'] = bitcompare

  db.init_app(app)

  return app

app = create_app()

@app.route("/")
def top():
  return redirect('index')

@app.route("/index")
@app.route("/about")
@app.route("/register")
@app.route("/registered")
@app.route("/login")
@app.route("/resetpassword")
@app.route("/logout")
@app.route("/notverified")
@app.route("/verify")
def logged_out_html():
  page = request.path[1:]
  values = dict([(x,'|'.join(request.values.getlist(x))) for x in request.values.keys()])
  json = request.get_json()
  if json: values.update(json)

  info('%s: %s' % (page, values))

  attrs = html_defaults(request.user_agent.string)
  attrs.update(values)
  func = globals().get("handle_%s" % page)
  if func: attrs.update(func(None,values))
  return render_template(page+'.html', **attrs)

@app.route("/cancelled")
@app.route("/dashboard")
@app.route("/profile")
@app.route("/photos")
@app.route("/seeking")
@app.route("/matches")
@app.route("/search")
@app.route("/results")
@app.route("/member")
@app.route("/emailthread")
@app.route("/inbox")
@app.route("/outbox")
@app.route("/favorites")
@app.route("/blocked")
@app.route("/account")
@login_required
def logged_in_html():
  if not g.entry:
    attrs = html_defaults(request.user_agent.string)
    attrs['redirect'] = request.url
    return render_template('login.html', **attrs)

  page = request.path[1:]
  values = dict([(x,'|'.join(request.values.getlist(x))) for x in request.values.keys()])
  json = request.get_json()
  if json: values.update(json)

  id   = g.entry.id
  user = g.entry.name

  info('%s: id:%d %s' % (page, id, values))

  attrs = html_defaults(request.user_agent.string)
  attrs.update(values)
  if not 'nav' in attrs: attrs['nav'] = page
  attrs['user']   = user
  attrs['advert'] = True
  attrs['inbox']  = InboxCount(id)
  attrs['outbox'] = OutboxCount(id)
  func = globals().get("handle_%s" % (page))
  if func: attrs.update(func(g.entry,values))
  attrs['per_page'] = PAGE_SIZE
  return render_template(page+'.html', **attrs)

@app.route('/mllogin')
def mllogin():
  page = request.path[1:]

  email    = request.cookies.get('email')
  password = request.cookies.get('password')

  if not email:
    return jsonify({'error': 'No email address specified.'})
  if not password:
    return jsonify({'error': 'No password specified.'})

  info('%s: %s %s' % (page, email, password))

  data = Login(email, password)

  info('%s: %s' % (page, data))

  return jsonify(data)

@app.route('/closestnames', methods=['GET', 'POST'])
@app.route('/mlpassword', methods=['POST'])
@app.route('/mlregister', methods=['POST'])
@app.route('/mlresend', methods=['POST'])
def logged_out_json():
  page = request.path[1:]
  values = dict([(x,'|'.join(request.values.getlist(x))) for x in request.values.keys()])
  json = request.get_json()
  if json: values.update(json)

  info('%s: %s' % (page, values))

  func = globals().get("handle_%s" % page)
  data = func(None, values, request.files)
  info('%s: %s' % (page, data))
  return jsonify(data)

@app.route('/mlaccount', methods=['POST'])
@app.route('/mladdfavorite', methods=['POST'])
@app.route('/mlblock', methods=['POST'])
@app.route('/mldeletefavorite', methods=['POST'])
@app.route('/mldeletephoto', methods=['POST'])
@app.route('/mlmasterphoto', methods=['POST'])
@app.route('/mlpassword', methods=['POST'])
@app.route('/mlprofile', methods=['POST'])
@app.route('/mlsearch', methods=['POST'])
@app.route('/mlseeking', methods=['POST'])
@app.route('/mlsendemail', methods=['POST'])
@app.route('/mlsendphoto', methods=['POST'])
@app.route('/mlspam', methods=['POST'])
@app.route('/mlunblock', methods=['POST'])
@app.route('/mluploadphoto', methods=['POST'])
@app.route('/mlwink', methods=['POST'])
@login_required
def logged_in_json():
  if not g.entry:
    return jsonify({'error': 'Not logged in.'})

  page = request.path[1:]
  values = dict([(x,'|'.join(request.values.getlist(x))) for x in request.values.keys()])
  json = request.get_json()
  if json: values.update(json)

  id = g.entry.id

  info('%s: id:%d %s' % (page, id, values))

  func = globals().get("handle_%s" % page)
  data = func(g.entry, values, request.files)
  info('%s: %s' % (page, data))
  return jsonify(data)

@app.route("/<path:path>")
def the_rest(path):
  info(path)

  return send_from_directory(app.static_folder, path.encode('utf-8'))

if __name__ == "__main__":
  app.run()
