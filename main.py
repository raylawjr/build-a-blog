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

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
	autoescape=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)

	def render_str(self,template,**params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class Blog(db.Model):
	title = db.StringProperty(required=True)
	blogpost = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
	def render_front(self, title="", blogpost="", error=""):
		blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")

		self.render("front2.html", title=title, blogpost=blogpost, error=error, blogs=blogs)

	def get(self):
		# self.render("front.html")
		self.render_front()

	def post(self):
		title = self.request.get('title')
		blogpost = self.request.get('blogpost')

		if title and blogpost:
			# self.write('Thanks!')

			# Create an instance 'a' of art object
			a = Blog(title=title, blogpost=blogpost)

			# Store our new art object instance in the database
			a.put()

			self.redirect('/')
		else:
			error = "We need both a title and content!"
			self.render_front(title=title, blogpost=blogpost, error=error)
class BlogHandler(Handler):
    def render_blog(self, title="", blogpost="", error=""):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")

        self.render("blog.html", title=title, blogpost=blogpost, error=error, blogs=blogs)
    def get(self):
        self.render_blog()

class ViewPostHandler(Handler):
	#webap2.RequestHandler
	def get(self, id):
		a = int(id)
		entry = Blog.get_by_id(a)
		if entry == None:
			self.response.write("No post with that id!")
		else:
			#self.response.write(id)
			#self.response.write(blogentry.key().id())
			title=""
			blogpost=""
			error=""
			self.render("blogpost.html", title=title, blogpost=blogpost, error=error, entry=entry)
		#posts = Blog.get_by_id(id)
		#error = "Sorry, that post doesn't exist!"
        #if Blog.get_by_id(int(id)) == None:
		#if Post.get_by_id(int(id)) == None:
		#	self.response.write(error)
		#else:
		#	self.response.write(Blog.get_by_id(int(id)))
class NewPostHandler(Handler):
    def render_newpost(self, title="", blogpost="", error=""):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")

        self.render("newpost.html", title=title, blogpost=blogpost, error=error, blogs=blogs)

    def get(self):
		# self.render("front.html")
		self.render_newpost()

    def post(self):
		title = self.request.get('title')
		blogpost = self.request.get('blogpost')

		if title and blogpost:
			# self.write('Thanks!')

			# Create an instance 'a' of art object
			a = Blog(title=title, blogpost=blogpost)

			# Store our new art object instance in the database
			a.put()

			self.redirect('/blog/%s'%a.key().id())
		else:
			error = "We need both a title and content!"
			self.render_newpost(title=title, blogpost_content=blogpost, error=error)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/blog', BlogHandler),
    ('/newpost', NewPostHandler),
	webapp2.Route('/blog/<id:\d+>', ViewPostHandler),

], debug=True)
