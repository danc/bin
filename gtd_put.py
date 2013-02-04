#! /usr/bin/env python
#  aptitude install python-setuptools
#  easy_install python-wordpress-xmlrpc
# http://python-wordpress-xmlrpc.readthedocs.org/en/latest/index.html
# https://github.com/maxcutler/python-wordpress-xmlrpc

# Configuration file read from $HOME/.gtd.ini, example :
#[WordPress]
#url=http://yoursite.wordpress.com
#xmlrpc=/xmlrpc.php
#user=yourlogin

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost
from sys import argv
from getpass import getpass
from os import getenv
import ConfigParser

home = getenv('HOME')

config = ConfigParser.RawConfigParser()
config.read(home+'/'+'.gtd.ini')
url = config.get('WordPress', 'url')
xmlrpc = config.get('WordPress', 'xmlrpc')
login = config.get('WordPress', 'user')
pwd = getpass("Password --> ")

wp = Client(url+xmlrpc, login, pwd)

posts = wp.call(GetPosts())
for post in posts:
	do_sync = 0

	for term in post.terms:
#		print term.name
		if term.name == "sync":
			do_sync = 1
#	if argv[1:]:
#		if argv[1] == post.title:
	if do_sync:
			print "----------------"
			print post.title
			f = open( post.title, 'r')
			cont = f.read().decode('utf-8')
			post.content = cont
#			post.id = wp.call(posts.NewPost(post))
			post.post_status = 'private'
			wp.call(EditPost(post.id, post))
			f.close
			print "Sync'ed : " + post.title
#print wp.call(GetUserInfo())
