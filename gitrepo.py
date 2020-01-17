import requests
import datetime
import sys
import json
import time


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


AUTH = None
try:
	authJson = json.loads(open("env.json", "r").read())
	AUTH = (authJson["username"], authJson["password"])
	logPrint("Authenticated user {}" .format(authJson["username"]), "success")
except:
	logPrint("Not authenticated - rate limit is 60 requests per hour", "warning")



def getGithubApiRequest(urlExcBase):
	"""use this to get json from api (returns some data to module variables)
	"""
	fullUrl = "https://api.github.com/"+urlExcBase
	request = requests.get(url=fullUrl,
		auth=AUTH)

	if int(request.headers["X-RateLimit-Remaining"]) < 1:
		logPrint("Remaining rate limit is zero. Try again at {}"
		.format(str(time.ctime(request.headers["X-RateLimit-Reset"]))), "error")
		sys.exit(1)

	requestJson = request.json()
	if "message" in requestJson:
		logPrint("Some error has occurred for {}" .format(fullUrl), "error")
		logPrint(requestJson)
		sys.exit(1)

	return requestJson


def sourceData(repoName):
	"""Get data for a repo (full data + pushed at time)
	"""
	sourceRepo = getGithubApiRequest("repos/"+repoName)
	sourceRepoPushedAt = getDatetime(sourceRepo["pushed_at"])
	return sourceRepo, sourceRepoPushedAt


def sourceAlive(repoName, lifespan):
	"""Is source repo alive?
	"""
	_sourceRepo, sourceRepoPushedAt = sourceData(repoName)
	return sourceRepoPushedAt + datetime.timedelta(weeks=lifespan) > datetime.datetime.now()


def getListOfRepos(repoName, data="forks"):
	"""Get a list of repos of a certain type: "forks", "stargazers"
	"""
	sourceRepo, _sourceRepoPushedAt = sourceData(repoName)
	pages = sourceRepo[data+"_count"] // 100 + 1
	if pages > 10:
		logPrint("There are {} {} - using top 1k only"
		.format(str(sourceRepo[data+"_count"]), data), "warning")
		pages = 10
	returnRepos = []
	for page in range(1, pages+1):
		returnRepos.extend(getGithubApiRequest(
			"repos/"+repoName+"/"+data+"?sort=stargazers&per_page=100&page="+str(page)))
	return returnRepos


def getListOfAliveForks(repoName, lifespan, enableNewer=True):
	"""Get list of forked repos that are alive and newer than the source repo
	"""
	_sourceRepo, sourceRepoPushedAt = sourceData(repoName)
	forkedRepos = getListOfRepos(repoName)
	aliveRepos = []
	for forkedRepo in forkedRepos:
		forkedRepoPushedAt = getDatetime(forkedRepo["pushed_at"])
		isAlive = forkedRepoPushedAt + datetime.timedelta(weeks=lifespan) > datetime.datetime.now()
		isNewer = forkedRepoPushedAt > sourceRepoPushedAt
		if (isAlive and isNewer) or (isAlive and not enableNewer):
			aliveRepos.append(forkedRepo)
	return aliveRepos, forkedRepos


def getListOfUserRepos(username, data):
	"""Get a list of repos using a username and type: "repos" (user public repos),
	"subscriptions" (user watching), "stargazing" (stars)
	"""
	returnRepos = []
	hasRepos = True
	page = 1
	while hasRepos:
		repos = getGithubApiRequest("users/"+username+"/"+data+"?per_page=100&page="+str(page))
		if len(repos) < 1:
			hasRepos = False
		returnRepos.extend(repos)
		page += 1
	return returnRepos



def getUsernameAndLifespan():
	"""Return the username from env.json and lifespan from user input
	"""
	username = None
	try:
		authJson = json.loads(open("env.json", "r").read())
		username = authJson["username"]
		logPrint("Hello {}!" .format(username), "success")
	except:
		username = input("Enter your username>")

	lifespan = 36
	try:
		lifespan = int(input("Set the repo lifespan (weeks - eg. 1 - default=36)>"))
	except:
		logPrint("Invalid input - using default", "warning")
	return username, lifespan


def getRepoTraffic(repoName, traffic):
	"""gets a json of the repo traffic. Traffic can be "views", "clones"
	"""
	return getGithubApiRequest("repos/"+repoName+"/traffic/"+traffic)
