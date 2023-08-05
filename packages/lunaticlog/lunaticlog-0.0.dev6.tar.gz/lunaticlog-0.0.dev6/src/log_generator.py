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

	def __init__(self, out_path='./log/apache.log'):
		# Instantiate the logger
		self.log = logging.getLogger('Gen')
		# Set the level
		logging.basicConfig(level=logging.INFO)
		# Instantiate a file Handler
		out = logging.FileHandler(out_path)

		log_format = logging.Formatter("%(message)s")
		# Set the Formatter for this Handler to form
		out.setFormatter(log_format)
		# Add the file Handler 'out' to the logger'log'
		self.log.addHandler(out)
	

	def run(self):
		self.loop = asyncio.get_event_loop()
		try:
			self.loop.run_until_complete(
				asyncio.wait([
					#self.heartbeat_lines()]
					self.heartbeat_lines(),
					self.access_lines()]
				)
			)
		finally:
			self.loop.close()


	@coroutine
	def heartbeat_lines(self):
		while True:
			t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')	
			self.log.info('- - - [%s] "%s" - -', t, 'HEARTBEAT')
			yield from asyncio.sleep(1)


	@coroutine
	def access_lines(self):
		while True:
			ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
			user_identifier = '-'
			user_id = 'frank'
			t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')

			#method = numpy.random.choice(self.methods, p=self.methods_dist)
			method = random.choice(['GET', 'PUT'])
			#resource = self.resources[random.randint(0, len(self.resources)-1)]
			resource = '/apache_pb.gif'
			#version = self.versions[random.randint(0, len(self.versions)-1)]
			version = 'HTTP/1.0'
			msg = method + " " + resource + " " + version
			#code = numpy.random.choice(self.codes, p=self.codes_dist)
			code = '200'
			size = random.randint(1024, 10240)
			self.log.info('%s %s %s [%s] "%s" %s %s', ip, user_identifier, user_id, t, msg, code, size)
			yield from asyncio.sleep(random.randint(1, 5))


'''def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", help="log output path")
	parser.add_argument("-m", help="log mode")
	args = parser.parse_args()

	# Identify the log format
	mode = args.m
	# Set default log format
	if not mode:
		mode = 'access'
	# Check if the log format is valid
	if mode not in ['access']:
		print('Argument error: -o')

	# Identufy the output path
	out_path = args.o
	# Set default output path
	if not out_path:
		out_path = './log/lunatic_log.log'

	# Instantiate the logger
	log = logging.getLogger('Gen')
	# Set the level
	logging.basicConfig(level=logging.INFO)
	# Instantiate a file Handler
	out = logging.FileHandler(out_path)

	# Instantiate a Formatter
	# Format the time string
	if mode == 'access':
		log_format = logging.Formatter("%(message)s")
	else:
		log_format = logging.Formatter("%(message)s")

	# Set the Formatter for this Handler to form
	out.setFormatter(log_format)
	# Add the file Handler 'out' to the logger'log'
	log.addHandler(out)

	# Load the configure json file to a dict
	#with open(os.environ['LUNATICHOME']+"/config/fake_log_gen.json") as config_file:
	#	config = json.load(config_file)
	

	# Instantiate a log generator
	if mode == 'access':
		log_gen = access_log_generator(log)

	log_gen.run()
'''




