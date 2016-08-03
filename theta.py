#! -*- coding: utf-8 -*-

import json
import time

from PIL import Image
from os import system
from requests import get
from requests import post

INFO_URL = "http://192.168.1.1/osc/info"
EXECUTE_URL = "http://192.168.1.1/osc/commands/execute"
STATE_URL = "http://192.168.1.1/osc/state"

SET_OPTIONS = "camera.setOptions"
GET_OPTIONS = "camera.getOptions"
START_SESSION = "camera.startSession"
TAKE_PICTURE = "camera.takePicture"
START_SESSION = "camera.startSession"
CLOSE_SESSION = "camera.closeSession"
GET_IMAGE = "camera.getImage"


# info = get(INFO_URL).text
# info = json.loads(info)
# info = json.dumps(info, indent=4, separators=(",", ": "))

# print info

# data = json.dumps({"name": START_SESSION})
# res = post(EXECUTE_URL, data)
# sessionId = json.loads(res.text)["results"]["sessionId"]
# print res.text
# print "Start session: " + str(sessionId)

def print_json(text):
	text = json.loads(text)
	text = json.dumps(text, indent=4, separators=(",", ": "))
	print text


class Theta(object):
	def __init__(self, verbose=False, ver=2):
		self.ver = ver
		info = get(INFO_URL).text
		info = json.loads(info)
		info = json.dumps(info, indent=4, separators=(",", ": "))
		if verbose:
			print info

	def start_session(self):
		data = json.dumps({"name": START_SESSION})
		res = post(EXECUTE_URL, data)
		# print_json(res.text)
		self.session_id = json.loads(res.text)["results"]["sessionId"]
		print "Start session: " + str(self.session_id)

		data = {"name": SET_OPTIONS}
		data["parameters"] = {}
		data["parameters"]["sessionId"] = self.session_id
		data["parameters"]["options"] = {}
		data["parameters"]["options"]["clientVersion"] = self.ver

		data = json.dumps(data)
		res = post(EXECUTE_URL, data)

		data = {"name": GET_OPTIONS}
		data["parameters"] = {"sessionId":self.session_id,"optionNames":["clientVersion", "_shutterVolume"]}
		data = json.dumps(data)
		res = post(EXECUTE_URL, data)
		print_json(res.text)
		# data = {"name": GET_OPTIONS}
		# data["parameters"] = {}
		# data["parameters"]["optionNames"] = ["clientVersion"]
		# data = json.dumps(data)
		# res = post(EXECUTE_URL, data)
		# print_json(res.text)
		# print res

		return self
	def set_volume(self, value):
		data = {}
		data["name"] = SET_OPTIONS
		data["parameters"] = {}
		data["parameters"]["options"] = {}
		data["parameters"]["options"]["_shutterVolume"] = value
		data = json.dumps(data)
		res = post(EXECUTE_URL, data)

		data = {}
		data["name"] = GET_OPTIONS
		data["parameters"] = {}
		data["parameters"]["optionNames"] = ["_shutterVolume"]
		data = json.dumps(data)
		res = post(EXECUTE_URL, data)
		print_json(res.text)

	def take_picture(self):
		data = {"name": TAKE_PICTURE}
		# params = {"sessionId": self.session_id}
		# data["parameters"] = params
		data = json.dumps(data)
		res = post(EXECUTE_URL, data)
		time.sleep(8)
		file_uri = ""
		while not file_uri:
			res = post(STATE_URL)
			file_uri = json.loads(res.text)["state"]["_latestFileUrl"]
		# print file_uri
		# data = json.dumps({"name": GET_IMAGE, "parameters": {"fileUri": file_uri}})
		# res = post(EXECUTE_URL, data)
		# with open("image.jpg", "wb") as file:
			# file.write(res.text)
		return file_uri


		# return file_uri
		# print "taking piture: " + json.loads(res.text)["fileUrl"]

theta = Theta()
try:
	theta.start_session()
except Exception, e:
	pass
theta.set_volume(0)
a = theta.take_picture()
system("wget " + a)
file = a.split("/")[-1]
image = Image.open(file)
image.show()













# data = json.dumps({"name": CLOSE_SESSION, "sessionId":sessionId})
# res = post(EXECUTE_URL, data)
# print res.text
# print "Close session: " + str(sessionId)