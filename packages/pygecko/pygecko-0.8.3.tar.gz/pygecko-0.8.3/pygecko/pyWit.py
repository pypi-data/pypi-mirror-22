# #!/usr/bin/env python

# ##############################################
# # The MIT License (MIT)
# # Copyright (c) 2016 Kevin Walchko
# # see LICENSE for full details
# ##############################################

# from __future__ import print_function
# from __future__ import division
# import os
# from wit import Wit
# import socket


# class pyWit(object):
# 	def __init__(self, token_env='WIT'):
# 		token = os.environ[token_env]
# 		self.client = Wit(token)
# 		self.speech_headers = {
# 			'authorization': 'Bearer ' + token,
# 			# 'accept': 'application/vnd.wit.20160330+json'
# 			'Content-Type': 'audio/wav'
# 			# 'Content-Type': 'audio/raw;encoding=signed-integer;bits=16;rate=16000;endian=little'
# 		}

# 		try:
# 			host = 'www.google.com'
# 			socket.gethostbyname(host)
# 		except socket.gaierror:
# 			raise Exception('ERROR: pyWit, you MUST be connected to internet, could not find {}'.format(host))

# 	@staticmethod
# 	def max(a):
# 		ret = None
# 		if not a:
# 			pass
# 		elif len(a) == 1:
# 			ret = a[0]
# 		else:
# 			ret = a.pop(0)
# 			for r in a:
# 				if r['confidence'] > ret['confidence']:
# 					ret = r

# 		return ret

# 	def filter_return(self, ans):
# 		pass

# 	def message(self, msg):
# 		intent = None
# 		confidence = 0.0
# 		ans = self.client.message(msg)
# 		# pprint(ans)

# 		if ans:
# 			ans = self.max(ans['outcomes'])
# 			intent = ans['intent']
# 			confidence = ans['confidence']
# 			# print('Result {} at {:.2f}%'.format(intent, confidence*100.0))
# 		return (intent, confidence, ans['entities'])

# 	def speech(self, wav):
# 		intent = None
# 		confidence = 0.0
# 		ans = self.client.speech(wav, headers=self.speech_headers)
# 		if ans:
# 			ans = self.max(ans['outcomes'])
# 			# print(ans)
# 			intent = ans['intent']
# 			confidence = ans['confidence']
# 			# print('Result {} at {:.2f}%'.format(intent, confidence*100.0))
# 		return (intent, confidence, ans['entities'])
