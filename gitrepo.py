import requests
import datetime
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
	logPrint("Not authenticated - Do you want to log in? (just hit enter if not)", "warning")
	try:
		AUTH = (input("Enter your username\n>"), input("Enter your password\n>"))
	except:
		logPrint("Not authenticated - rate limit is 60 requests per hour", "warning")


def getGithubApiRequest(urlExcBase, jsonOnly=True):
	"""use this to get json from api (returns some data to module variables)
	"""
	fullUrl = "https://api.github.com/"+urlExcBase
	request = requests.get(url=fullUrl, auth=AUTH)

	if int(request.headers["X-RateLimit-Remaining"]) < 1:
		logPrint("Remaining rate limit is zero. Try again at {}"
		.format(str(time.ctime(request.headers["X-RateLimit-Reset"]))), "error")

	requestJson = request.json()
	if "message" in requestJson:
		logPrint("Some error has occurred for {}" .format(fullUrl), "error")
		logPrint(requestJson)

	return requestJson if jsonOnly else request


def sourceAlive(repoData, lifespan):
	"""Is source repo alive?
	"""
	return getDatetime(
		repoData["pushed_at"]) + datetime.timedelta(weeks=lifespan) > datetime.datetime.now()


def getListOfRepos(repoName, context="forks"):
	"""Get a list of repos of a certain type: "forks", "stargazers"
	"""
	return getPaginatedGithubApiRequest("repos/"+repoName+"/"+context)



def getListOfAliveForks(repoData, lifespan, enableNewer=True):
	"""Get list of forked repos that are alive and newer than the source repo
	"""
	forkedRepos = getListOfRepos(repoData["full_name"])
	aliveRepos = []
	for forkedRepo in forkedRepos:
		forkedRepoPushedAt = getDatetime(forkedRepo["pushed_at"])
		isAlive = forkedRepoPushedAt + datetime.timedelta(weeks=lifespan) > datetime.datetime.now()
		isNewer = forkedRepoPushedAt > getDatetime(repoData["pushed_at"])
		if (isAlive and isNewer) or (isAlive and not enableNewer):
			aliveRepos.append(forkedRepo)
	return aliveRepos, forkedRepos


def getListOfUserRepos(username, context):
	"""Get a list of repos using a username and type: "repos" (user public repos),
	"subscriptions" (user watching), "stargazing" (stars)
	"""
	return getPaginatedGithubApiRequest("users/"+username+"/"+context)


def getPaginatedGithubApiRequest(apiUrl):
	firstPage = getGithubApiRequest(apiUrl+"?per_page=100", False)
	iterable = firstPage.json()
	try:
		lastPage = int(firstPage.links['last']['url'].split("&page=")[1])
	except:
		lastPage = 1
	pageLimit = 5
	if lastPage > pageLimit:
		logPrint("There are over {} pages! Limiting to {} pages" .format(pageLimit, pageLimit), "warning")
		lastPage = pageLimit
	for page in range(2, lastPage + 1):
		iterationsInstance = getGithubApiRequest(apiUrl+"?per_page=100&page="+str(page))
		iterable.extend(iterationsInstance)
	return iterable

def getUsername():
	username = None
	try:
		authJson = json.loads(open("env.json", "r").read())
		username = authJson["username"]
		logPrint("Hello {}!" .format(username), "success")
	except:
		username = input("Enter your username\n>")
	return username


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


def getRepoTraffic(repoName, traffic):
	"""gets a json of the repo traffic. Traffic can be "views", "clones"
	"""
	return getGithubApiRequest("repos/"+repoName+"/traffic/"+traffic)


def getUser(username):
	return getGithubApiRequest("users/"+username)


def getRepo(repoName):
	return getGithubApiRequest("repos/"+repoName)


def getReadme(repoName):
	return requests.get(url=getGithubApiRequest("repos/"+repoName+"/readme")["download_url"]).text


def search(searchTerm, context="repositories"):
	"""code, commits, issues, labels, repositories, users
	"""
	return getGithubApiRequest(
		"search/"+context+"?q="+searchTerm+"&sort=stargazers&per_page=100")["items"]

def getUserGists(username):
	return getPaginatedGithubApiRequest("users/"+username+"/gists")


def printIssue(issue):
	logPrint(("[\033[91mClosed\033[00m] " if issue["state"] == "closed" else "")
	+ issue["title"], "bold")
	logPrint(issue["updated_at"])

def printUser(user):
	logPrint(user["login"], "bold")
	logPrint(user["html_url"])

def printGist(gist):
	logPrint(gist["description"], "bold")
	logPrint("Files: {}" .format(list(gist["files"].keys())), "bold")
	logPrint(gist["html_url"])

def printRepo(repo):
	try:
		logPrint("{}"
		.format(("[\033[91mArchived\033[00m] " if repo["archived"] else "") + repo["name"]), "bold")
	except:
		return
	description = repo["description"] if "description" in repo else "[description]"
	language = repo["language"] if "language" in repo else "[unknown]"
	try:
		licenseName = repo["license"]["name"]
	except:
		licenseName = "[unknown]"
	updated = repo["updated_at"] if "updated_at" in repo else "[unknown]"
	logPrint("{}\nLanguage: {}, License: {}, Last Updated: {}"
	.format(description, language, licenseName, updated))
	logPrint("Link: {}" .format(repo["html_url"]))
