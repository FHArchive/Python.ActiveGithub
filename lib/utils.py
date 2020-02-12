import os
import datetime
import json


def clear():
	os.system('cls' if os.name == 'nt' else 'clear')


def getDatetime(datetimeIn):
	"""Get the datetime from a date in the format YYYY-MM-DDThh:mm:ssZ e.g. 2000-01-01T00:00:00Z
	"""
	return datetime.datetime.strptime(datetimeIn, "%Y-%m-%dT%H:%M:%SZ")


def logPrint(printText, printType="standard"):
	"""use this to print. standard, success, warning, error, info, bold
	"""
	types = {"standard": "{}", "success": "[\033[92m+ Success\033[00m] {}",
	"warning": "[\033[93m/ Warning\033[00m] {}", "error": "[\033[91m- Error\033[00m] {}",
	"info": "[\033[96m* Info\033[00m] {}", "bold": "\033[01m{}\033[00m"}
	print(types[printType.lower()] .format(printText))


def getUsername():
	return AUTH[0]

def getPassword():
	return AUTH[1]

def getUsernameAndLifespan():
	"""Return the username from env.json and lifespan from user input
	"""
	username = getUsername()
	lifespan = 36
	try:
		lifespan = int(input("Set the repo lifespan (weeks - eg. 1 - default=36)\n>"))
	except:
		logPrint("Invalid input - using default", "warning")
	return username, lifespan


if 'AUTH' not in locals():
	try:
		authJson = json.loads(open("env.json", "r").read())
		AUTH = (authJson["username"], authJson["password"])
		logPrint("Authenticated user {}" .format(authJson["username"]), "success")
	except:
		logPrint(
		"Not authenticated - Do you want to log in? (just hit enter if not)",
		"warning")
		try:
			AUTH = (
		USERNAME,
		_) = (
			input("Enter your username\n>"),
			input("Enter your password\n>"))
		except:
			logPrint("Not authenticated - rate limit is 60 requests per hour", "warning")
