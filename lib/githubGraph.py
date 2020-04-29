#!/usr/bin/env python3
"""Interface with git v4 api. Used by programs under 'main'
"""
import time
import datetime
import requests
from metprint import LogType
from utils import printf, getPassword, getDatetime

def getGithubApiRequest(query, variables=None, jsonOnly=True):
	"""use this to get json from api (returns some data to module variables)
	"""
	for key in variables:
		query = query.replace("$" + key, variables[key])
	request = requests.post(
	"https://api.github.com/graphql",
	json={
		"query": query},
		headers={
			"Authorization": "bearer " +
			 getPassword()})
	if int(request.headers["X-RateLimit-Remaining"]) < 1:
		printf.logPrint("Remaining rate limit is zero. Try again at {}"
		.format(str(time.ctime(request.headers["X-RateLimit-Reset"]))), "error")

	requestJson = request.json()
	if "message" in requestJson:
		printf.logPrint("Some error has occurred", "error")
		printf.logPrint(requestJson)

	return requestJson if jsonOnly else request



def getListOfForks(owner, repoName, lifespan=520):
	"""Get a list of forks within a certian lifespan (default=520 weeks)
	"""
	repos = []
	hasNextPage = True
	after = ""
	while hasNextPage:
		includeIfAfter = """after:"$after",""" if after != "" else ""
		repoPage = getGithubApiRequest("""
		query {
			repository(owner:"$owner", name:"$name") {
				forks(first:100, """ + includeIfAfter + """orderBy:{direction:DESC, field:PUSHED_AT}){
					pageInfo {
						hasNextPage
						endCursor
					}
					nodes{
						name
						owner{login}
						pushedAt
						url
						isArchived
						description
						primaryLanguage{name}
						licenseInfo{name}
						}
					}
				}
			}""",
		{"owner": owner, "name": repoName, "after": after})["data"]["repository"]["forks"]
		repos.extend(repoPage["nodes"])
		hasNextPage = repoPage["pageInfo"]["hasNextPage"] and sourceAlive(repoPage["nodes"][99], lifespan)
		after = repoPage["pageInfo"]["endCursor"]
	return repos

def getListOfAliveForks(repoData, lifespan, enableNewer=True):
	"""Get list of forked repos that are alive and newer than the source repo
	"""
	forkedRepos = getListOfForks(repoData["owner"]["login"], repoData["name"], lifespan=lifespan)
	aliveRepos = []
	for forkedRepo in forkedRepos:
		isAlive = sourceAlive(forkedRepo, lifespan)
		isNewer = getDatetime(forkedRepo["pushedAt"]) > getDatetime(repoData["pushedAt"])
		if (isAlive and isNewer) or (isAlive and not enableNewer):
			aliveRepos.append(forkedRepo)
	return aliveRepos, forkedRepos

def getStargazerCount(owner, repoName):
	"""Get a count of stargazers
	"""
	return getGithubApiRequest("""
	query {
		repository(owner:"$owner", name:"$name") {
			stargazers{
				totalCount
			}
		}
	}""",
	{"owner": owner, "name": repoName})["data"]["repository"]["stargazers"]["totalCount"]


def getUser(username):
	'''Get user login and url '''
	return getGithubApiRequest("""
		query {
			user(login:"$login") {
				login
				url
			}
		}
		""",
		{"login": username})["data"]["user"]


def getRepo(owner, repoName):
	'''Get repo name, owner, last pushed at and url '''
	return getGithubApiRequest("""
		query {
			repository(owner:"$owner", name:"$name") {
				name
				owner{login}
				pushedAt
				url
			}
		}""",
		{"owner": owner, "name": repoName})["data"]["repository"]



def search(_searchTerm, _context="repositories"):
	"""code, commits, issues, labels, repositories, users
	"""
	return

def getUserGists(username):
	'''Get a list of user gists '''
	return getGithubApiRequest("""
		query {
			user(login:"$login") {
				gists(first:100, orderBy:{direction:DESC, field:PUSHED_AT}){
					nodes{
						name
						description
						files{name}
						url
					}
				}
			}
		}
		""",
		{"login": username})["data"]["user"]["gists"]["nodes"]


def getListOfRepos(login, context="repositories", organization=False, lifespan=520):
	"""Get a list of repos using a username and type: "repositories" (user public repos),
	"watching" (user watching), "starredRepositories" (stars)
	"""
	repos = []
	hasNextPage = True
	after = ""
	starredOrPushed = "STARRED_AT" if context == "starredRepositories" else "PUSHED_AT"
	userOrOrg = "organization" if organization else "user"
	while hasNextPage:
		includeIfAfter = """after:"$after",""" if after != "" else ""
		repoPage = getGithubApiRequest("""
		query {
			""" + userOrOrg + """(login:"$login") {
				$context(first:100, """ + includeIfAfter +
				"""orderBy:{direction:DESC, field:""" + starredOrPushed + """}){
					pageInfo {
						hasNextPage
						endCursor
					}
					nodes{
						name
						owner{login}
						pushedAt
						url
						isArchived
						description
						primaryLanguage{name}
						licenseInfo{name}
						}
					}
				}
			}""",
		{"login": login, "context": context, "after": after})["data"][userOrOrg][context]
		repos.extend(repoPage["nodes"])
		hasNextPage = repoPage["pageInfo"]["hasNextPage"] and sourceAlive(repoPage["nodes"][99], lifespan)
		after = repoPage["pageInfo"]["endCursor"]
	return repos


def printIssue(issue):
	'''Print issue function '''
	printf.logPrint(("[\033[91mClosed\033[00m] " if issue["state"] == "closed" else "")
	+ issue["title"], LogType.BOLD)
	printf.logPrint(issue["pushedAt"])

def printUser(user):
	'''Print user function '''
	printf.logPrint(user["login"], LogType.BOLD)
	printf.logPrint(user["url"])

def printGist(gist):
	'''Print gist function '''
	printf.logPrint(gist["description"], LogType.BOLD)
	printf.logPrint("Files: {}" .format([gFile['name'] for gFile in gist["files"]]), LogType.BOLD)
	printf.logPrint(gist["url"])

def printRepo(repo):
	'''Print repo function '''
	if all(key in repo for key in ("isArchived", "name")):
		printf.logPrint("{}"
		.format(("[\033[91mArchived\033[00m] " if repo["isArchived"]
		else "") + repo["name"]), LogType.BOLD)
	else:
		return
	description = repo["description"] if "description" in repo else "[description]"
	language = repo["primaryLanguage"]["name"] if repo["primaryLanguage"] is not None else "[unknown]"
	licenseName = repo["licenseInfo"]["name"] if repo["licenseInfo"] is not None else "[unknown]"
	pushed = repo["pushedAt"] if "pushedAt" in repo else "[unknown]"
	printf.logPrint("{}\nLanguage: {}, License: {}, Last Pushed: {}"
	.format(description, language, licenseName, pushed))
	printf.logPrint("Link: {}" .format(repo["url"]))


def sourceAlive(repoData, lifespan):
	"""Is source repo alive?
	"""
	return getDatetime(repoData["pushedAt"]) > (datetime.datetime.now() -
	datetime.timedelta(weeks=lifespan))
