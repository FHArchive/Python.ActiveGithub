"""Interface with git v3 api. Used by programs under 'main'
"""
import datetime
import time
import requests
from metprint import LogType
from utils import printf, AUTH, getDatetime

def getGithubApiRequest(urlExcBase, jsonOnly=True):
	"""use this to get json from api (returns some data to module variables)
	"""
	fullUrl = "https://api.github.com/"+urlExcBase
	request = requests.get(url=fullUrl, auth=AUTH)

	if int(request.headers["X-RateLimit-Remaining"]) < 1:
		printf.logPrint("Remaining rate limit is zero. Try again at {}"
		.format(str(time.ctime(request.headers["X-RateLimit-Reset"]))), "error")

	requestJson = request.json()
	if "message" in requestJson:
		printf.logPrint("Some error has occurred for {}" .format(fullUrl), "error")
		printf.logPrint(requestJson)

	return requestJson if jsonOnly else request


def sourceAlive(repoData, lifespan):
	"""Is source repo alive?
	"""
	if "pushed_at" in repoData:
		pushedAt = repoData["pushed_at"]
	else:
		pushedAt = repoData["pushedAt"]
	return getDatetime(
		pushedAt) + datetime.timedelta(weeks=lifespan) > datetime.datetime.now()


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
	'''Get a api request over multiple pages '''
	firstPage = getGithubApiRequest(apiUrl+"?per_page=100", False)
	iterable = firstPage.json()
	try:
		lastPage = int(firstPage.links['last']['url'].split("&page=")[1])
	except IndexError:
		lastPage = 1
	pageLimit = 10
	if lastPage > pageLimit:
		printf.logPrint("There are over {pageLimit} pages! Limiting to {pageLimit} pages"
		.format(pageLimit=pageLimit), "warning")
		lastPage = pageLimit
	for page in range(2, lastPage + 1):
		iterationsInstance = getGithubApiRequest(apiUrl+"?per_page=100&page="+str(page))
		iterable.extend(iterationsInstance)
	return iterable


def getRepoTraffic(repoName, traffic):
	"""gets a json of the repo traffic. Traffic can be "views", "clones"
	"""
	return getGithubApiRequest("repos/"+repoName+"/traffic/"+traffic)


def getUser(username):
	'''Get user login and url '''
	return getGithubApiRequest("users/"+username)


def getRepo(repoName):
	'''Get repo name, owner, last pushed at and url '''
	return getGithubApiRequest("repos/"+repoName)


def getReadme(repoName):
	'''Get the repo readme '''
	return requests.get(url=getGithubApiRequest("repos/"+repoName+"/readme")["download_url"]).text


def search(searchTerm, context="repositories"):
	"""code, commits, issues, labels, repositories, users
	"""
	return getGithubApiRequest(
		"search/"+context+"?q="+searchTerm+"&sort=stargazers&per_page=100")["items"]

def getUserGists(username):
	'''Get a list of user gists '''
	return getPaginatedGithubApiRequest("users/"+username+"/gists")


def printIssue(issue):
	'''Print issue function '''
	printf.logPrint(("[\033[91mClosed\033[00m] " if issue["state"] == "closed" else "")
	+ issue["title"], LogType.BOLD)
	printf.logPrint(issue["updated_at"])

def printUser(user):
	'''Print user function '''
	printf.logPrint(user["login"], LogType.BOLD)
	printf.logPrint(user["html_url"])

def printGist(gist):
	'''Print gist function '''
	printf.logPrint(gist["description"], LogType.BOLD)
	printf.logPrint("Files: {}" .format(list(gist["files"].keys())), LogType.BOLD)
	printf.logPrint(gist["html_url"])

def printRepo(repo):
	'''Print repo function '''
	if all(key in repo for key in ("archived", "name")):
		printf.logPrint("{}"
		.format(("[\033[91mArchived\033[00m] " if repo["archived"] else "") + repo["name"]), LogType.BOLD)
	else:
		return
	description = repo["description"] if "description" in repo else "[description]"
	language = repo["language"] if "language" in repo else "[unknown]"
	try:
		licenseName = repo["license"]["name"]
	except (KeyError, TypeError):
		licenseName = "[unknown]"
	updated = repo["updated_at"] if "updated_at" in repo else "[unknown]"
	printf.logPrint("{}\nLanguage: {}, License: {}, Last Updated: {}"
	.format(description, language, licenseName, updated))
	printf.logPrint("Link: {}" .format(repo["html_url"]))
