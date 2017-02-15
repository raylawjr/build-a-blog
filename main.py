#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path,join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)

	def render_str(self,template,**params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Blog(db.Model):

	"""
	# This is in the database module from Google
	# And this is how you say something is a particular type
	# required=True sets a constraint on the database, it means that if we try to make an instance of art without giving it a title, it would give us an exception, python won't let us do that.
	# auto_now_add=True (in 'created' below) - it automatically, when we create an instance of art, will set the created to be the current time.
	"""
	title = db.StringProperty(required=True)
	postcontent = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
	def render_front(self, title="", postlisting="", error=""):
		"""
		This function is created to avoid code duplication as we are going to render form using "self.render" quite a few times
		"""

		"""
		Each time we render the front page, we get all the arts present in the database using the query as below (arts).
		"""
	    posts = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")

		self.render("front.html", title=title, =postlisting, error=error, posts=posts)

	def get(self):
		# self.render("front.html")
		self.render_front()

	def post(self):
		title = self.request.get('title')
		postcontent = self.request.get('postcontent')

		if title and postcontent:
			# self.write('Thanks!')

			# Create an instance 'a' of art object
			a = Blog(title=title, postcontent=postcontent)

			# Store our new art object instance in the database
			a.put()

			self.redirect('/')
		else:
			error = "We need both, a title and content!"
			self.render_front(title=title, postlisting=postcontent, error=error)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
