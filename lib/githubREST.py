import requests
import datetime
import json
import time
import utils

def getGithubApiRequest(urlExcBase, jsonOnly=True):
	"""use this to get json from api (returns some data to module variables)
	"""
	fullUrl = "https://api.github.com/"+urlExcBase
	request = requests.get(url=fullUrl, auth=utils.AUTH)

	if int(request.headers["X-RateLimit-Remaining"]) < 1:
		utils.logPrint("Remaining rate limit is zero. Try again at {}"
		.format(str(time.ctime(request.headers["X-RateLimit-Reset"]))), "error")

	requestJson = request.json()
	if "message" in requestJson:
		utils.logPrint("Some error has occurred for {}" .format(fullUrl), "error")
		utils.logPrint(requestJson)

	return requestJson if jsonOnly else request


def sourceAlive(repoData, lifespan):
	"""Is source repo alive?
	"""
	try:
		pushedAt = repoData["pushed_at"]
	except:
		pushedAt = repoData["pushedAt"]
	return utils.getDatetime(
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
		forkedRepoPushedAt = utils.getDatetime(forkedRepo["pushed_at"])
		isAlive = forkedRepoPushedAt + datetime.timedelta(weeks=lifespan) > datetime.datetime.now()
		isNewer = forkedRepoPushedAt > utils.getDatetime(repoData["pushed_at"])
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
	pageLimit = 10
	if lastPage > pageLimit:
		utils.logPrint("There are over {} pages! Limiting to {} pages" .format(pageLimit, pageLimit), "warning")
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
	utils.logPrint(("[\033[91mClosed\033[00m] " if issue["state"] == "closed" else "")
	+ issue["title"], "bold")
	utils.logPrint(issue["updated_at"])

def printUser(user):
	utils.logPrint(user["login"], "bold")
	utils.logPrint(user["html_url"])

def printGist(gist):
	utils.logPrint(gist["description"], "bold")
	utils.logPrint("Files: {}" .format(list(gist["files"].keys())), "bold")
	utils.logPrint(gist["html_url"])

def printRepo(repo):
	try:
		utils.logPrint("{}"
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
	utils.logPrint("{}\nLanguage: {}, License: {}, Last Updated: {}"
	.format(description, language, licenseName, updated))
	utils.logPrint("Link: {}" .format(repo["html_url"]))
