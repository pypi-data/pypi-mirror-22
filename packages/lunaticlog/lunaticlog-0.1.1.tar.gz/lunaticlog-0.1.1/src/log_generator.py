import os
import random
import json
import logging
import argparse
import asyncio
import datetime
from asyncio import coroutine
import numpy


# Apache Access Logs
class apache(object):

	def __init__(self, out_path='./apache.log', lines=['heartbeat', 'access'], heartbeat_interval=0.1, access_interval=[0.1, 2], methods=['GET', 'POST', 'PUT', 'DELETE'], methods_p = [0.7, 0.1, 0.1, 0.1], mode='normal', forever=True, count=1):
		# Assign the lines to generate	
		self.lines = lines
		self.lines_full = ['heartbeat', 'access']
		self.lines_gen = [self.heartbeat_lines(), self.access_lines()]
		# Assign the http methods to generate	
		self.methods = methods	
		# Assign the methods distribution
		self.methods_p = methods_p
		# Run forever or not
		self.forever = forever
		# Total # of logs to generate
		self.count = count
		# Assign the intervals
		self.heartbeat_interval = heartbeat_interval
		self.access_interval = access_interval
		# Assign the generator mode
		self.mode = mode

		# Instantiate the logger
		self.log = logging.getLogger('Gen')
		# Set the level
		logging.basicConfig(level=logging.INFO)
		# Instantiate a file Handler
		out = logging.FileHandler(out_path, mode='w')

		log_format = logging.Formatter("%(message)s")
		# Set the Formatter for this Handler to form
		out.setFormatter(log_format)
		# Add the file Handler 'out' to the logger'log'
		self.log.addHandler(out)


	def run(self):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		try:
			loop.run_until_complete(
				asyncio.wait([self.lines_gen[self.lines_full.index(x)] for x in self.lines])
		)
		finally:
			loop.close()



	@coroutine
	def heartbeat_lines(self):
		while self.forever or self.count > 0:
			t = self.get_time_field()
			self.log.info('- - - [%s] "%s" - -', t, 'HEARTBEAT')	
			if self.count > 0:
				self.count -= 1
			yield from asyncio.sleep(self.heartbeat_interval)


	def get_time_field(self):
		return datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')


	@coroutine
	def access_lines(self):
		while self.forever or self.count > 0:	
			ip = self.get_ip()
			user_identifier = self.get_user_identifier()
			user_id = self.get_user_id()
			t = self.get_time_field()

			method = self.get_method()
			#method = random.choice(self.methods)
			#resource = self.resources[random.randint(0, len(self.resources)-1)]
			resource = self.get_resource()
			#version = self.versions[random.randint(0, len(self.versions)-1)]
			version = self.get_version()
			msg = self.get_msg(method, resource, version)
			#code = numpy.random.choice(self.codes, p=self.codes_dist)
			#code = '200'
			code = self.get_code()
			#size = random.randint(1024, 10240)
			size = self.get_size()
			self.log.info('%s %s %s [%s] "%s" %s %s', ip, user_identifier, user_id, t, msg, code, size)

			if self.count > 0:
				self.count -= 1


			sleep_time = self.get_access_sleep_time()
			yield from asyncio.sleep(sleep_time)


	def get_ip(self):
		return '.'.join(str(random.randint(0, 255)) for i in range(4))


	def get_user_identifier(self):
		return '-'


	def get_user_id(self):
		return 'frank'


	def get_method(self):
		return numpy.random.choice(self.methods, p=self.methods_p)


	def get_resource(self):
		return '/apache_pb.gif'
	

	def get_version(self):
		return 'HTTP/1.0'


	def get_msg(self, method, resource, version):
		return method + " " + resource + " " + version


	def get_code(self):
		return '200'


	def get_size(self):
		return random.randint(1024, 10240)


	def get_access_sleep_time(self):
		# 'normal' mode - uniform distribution between min & max intervals
		if self.mode == 'normal':
			return random.uniform(self.access_interval[0], self.access_interval[1])
		# 'push' mode - at highest rate
		elif self.mode == 'push':
			return self.access_interval[0]

		# 'spike' mode
		elif self.mode == 'spike':
			mean = (self.access_interval[0]+self.access_interval[1])/2
			# Standard deviation
			sigma = (self.access_interval[1]-self.access_interval[0])/2
			return numpy.random.normal(mean, sigma)

		else:
			random.uniform(self.access_interval[0], self.access_interval[1])




