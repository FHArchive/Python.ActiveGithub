import requests
import datetime
import sys
import json
import time


def logPrint(printText, printType="standard"):
	"""use this to print
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


def sourceData(repo):
	"""Get data for a repo (full data + pushed at time)
	"""
	sourceRepo = getGithubApiRequest("repos/"+repo)
	sourceRepoPushedAt = datetime.datetime.strptime(sourceRepo["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")
	return sourceRepo, sourceRepoPushedAt


def sourceAlive(repo, death):
	"""Is source repo alive?
	"""
	_sourceRepo, sourceRepoPushedAt = sourceData(repo)
	return sourceRepoPushedAt + datetime.timedelta(weeks=death) > datetime.datetime.now()


def forksAliveAndNewer(repo, death):
	"""Get list of forked repos that are alive and newer than the source repo
	"""
	sourceRepo, sourceRepoPushedAt = sourceData(repo)
	pages = sourceRepo["forks_count"] // 100 + 1
	if pages > 10:
		logPrint("There are {} forks - using top 1k only" .format(str(sourceRepo["forks_count"])), "warning")
		pages = 10
	forkedRepos = []
	for page in range(1, pages+1):
		forkedRepos.extend(getGithubApiRequest("repos/"+repo+"/forks?sort=stargazers&per_page=100&page="+str(page)))

	aliveRepos = []
	for forkedRepo in forkedRepos:
		forkedRepoPushedAt = datetime.datetime.strptime(forkedRepo["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")
		if forkedRepoPushedAt + datetime.timedelta(
			weeks=death) > datetime.datetime.now() and forkedRepoPushedAt > sourceRepoPushedAt:
			aliveRepos.append(forkedRepo)

	return aliveRepos, forkedRepos
