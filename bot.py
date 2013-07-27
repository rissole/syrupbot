""" Manages reading the schemepunk blog RSS and posting new entries to reddit """

from apscheduler.scheduler import Scheduler
import praw
import feedparser
import time
import logging

logging.basicConfig()
r = praw.Reddit(user_agent='Syrup Games bot')

# Start the scheduler
sched = Scheduler()
sched.start()

# Download blog RSS and post new blog entries to reddit
def check_blog_and_post():
	try:
		f = open('credentials.txt', 'r')
		user,pw = f.read().split(',')
		f.close()
		r.login(user, pw)
	except:
		return
	f = open('lastcheck', 'a+')
	lastcheck = f.read()
	f.close()
	if (lastcheck != ''):
		lastcheck = float(lastcheck)
	print 'Checking... lastcheck=' + str(lastcheck)
	feed = feedparser.parse('http://syrupdev.blogspot.com/feeds/posts/default')
	pubdate = 0
	items = feed['items']
	items.reverse()
	for item in items:
		pubdate = time.mktime(item['published_parsed'])
		if (lastcheck == '' or pubdate > lastcheck):
			try:
				r.submit('schemepunk', item['title'], url=item['link'])
				print 'Posted',item['title']
			except Exception as inst:
				if (("ALREADY_SUB") in str(inst)):
					lastcheck = pubdate
					continue
				print inst + "(" + item['title'] + ")"
				break
	f = open('lastcheck', 'w')
	f.write(str(lastcheck))
	f.close()
	
sched.add_interval_job(check_blog_and_post, minutes=10)
	
while True:
    pass