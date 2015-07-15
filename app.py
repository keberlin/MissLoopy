#!/usr/bin/python

import sys

from functools import wraps
from flask import Flask, redirect, render_template, request, send_from_directory, g, jsonify

from html import *
from handlers_html import *
from handlers_json import *

from logger import *

PAGE_SIZE = 20

def debug(str):
  logger.debug(request.remote_addr + ' ' + str)

def info(str):
  logger.info(request.remote_addr + ' ' + str)

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
application = Flask(__name__)
application.debug = True

application.jinja_env.filters['bitcompare'] = bitcompare

@application.route("/")
def top():
  return redirect('index')

@application.route("/index")
@application.route("/about")
@application.route("/register")
@application.route("/registered")
@application.route("/login")
@application.route("/logout")
@application.route("/notverified")
@application.route("/verify")
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

@application.route("/cancelled")
@application.route("/dashboard")
@application.route("/profile")
@application.route("/photos")
@application.route("/seeking")
@application.route("/matches")
@application.route("/search")
@application.route("/results")
@application.route("/member")
@application.route("/emailthread")
@application.route("/emailthread2")
@application.route("/inbox")
@application.route("/outbox")
@application.route("/favorites")
@application.route("/blocked")
@application.route("/account")
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

  id   = g.entry[COL_ID]
  user = g.entry[COL_NAME]

  info('%s: id:%d %s' % (page, id, values))

  attrs = html_defaults(request.user_agent.string)
  attrs.update(values)
  if not 'nav' in attrs: attrs['nav'] = page
  attrs['user']   = user
  attrs['advert'] = True
  attrs['inbox']  = InboxCount(id)
  attrs['outbox'] = OutboxCount(id)
  func = globals().get("handle_%s" % page)
  if func: attrs.update(func(g.entry,values))
  attrs['num_pages'] = (len(attrs['entries'])+PAGE_SIZE-1)/PAGE_SIZE if 'entries' in attrs else 0
  attrs['per_page']  = PAGE_SIZE
  return render_template(page+'.html', **attrs)

@application.route('/mllogin')
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

@application.route('/closestnames', methods=['GET', 'POST'])
@application.route('/mlpassword', methods=['POST'])
@application.route('/mlregister', methods=['POST'])
@application.route('/mlresend', methods=['POST'])
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

@application.route('/mlaccount', methods=['POST'])
@application.route('/mladdfavorite', methods=['POST'])
@application.route('/mlblock', methods=['POST'])
@application.route('/mldeletefavorite', methods=['POST'])
@application.route('/mldeletephoto', methods=['POST'])
@application.route('/mlmasterphoto', methods=['POST'])
@application.route('/mlpassword', methods=['POST'])
@application.route('/mlprofile', methods=['POST'])
@application.route('/mlsearch', methods=['POST'])
@application.route('/mlseeking', methods=['POST'])
@application.route('/mlsendemail', methods=['POST'])
@application.route('/mlsendphoto', methods=['POST'])
@application.route('/mlspam', methods=['POST'])
@application.route('/mlunblock', methods=['POST'])
@application.route('/mluploadphoto', methods=['POST'])
@application.route('/mlwink', methods=['POST'])
@login_required
def logged_in_json():
  if not g.entry:
    return jsonify({'error': 'Not logged in.'})

  page = request.path[1:]
  values = dict([(x,'|'.join(request.values.getlist(x))) for x in request.values.keys()])
  json = request.get_json()
  if json: values.update(json)

  id = g.entry[COL_ID]

  info('%s: id:%d %s' % (page, id, values))

  func = globals().get("handle_%s" % page)
  data = func(g.entry, values, request.files)
  info('%s: %s' % (page, data))
  return jsonify(data)

@application.route("/<path:path>")
def the_rest(path):
  info(path)

  return send_from_directory(application.static_folder, path.encode('utf-8'))

if __name__ == "__main__":
  application.run()
