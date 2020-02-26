#!/usr/bin/env python3
import requests
import time
import datetime
import utils

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
			 utils.getPassword()})
	if int(request.headers["X-RateLimit-Remaining"]) < 1:
		utils.logPrint("Remaining rate limit is zero. Try again at {}"
		.format(str(time.ctime(request.headers["X-RateLimit-Reset"]))), "error")

	requestJson = request.json()
	if "message" in requestJson:
		utils.logPrint("Some error has occurred", "error")
		utils.logPrint(requestJson)

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
		isNewer = utils.getDatetime(forkedRepo["pushedAt"]) > utils.getDatetime(repoData["pushedAt"])
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



def search(searchTerm, context="repositories"):
	"""code, commits, issues, labels, repositories, users
	"""
	return

def getUserGists(username):
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




def getListOfUserRepos(username, context="repositories", lifespan=520):
	"""Get a list of repos using a username and type: "repositories" (user public repos),
	"watching" (user watching), "starredRepositories" (stars)
	"""
	repos = []
	hasNextPage = True
	after = ""
	while hasNextPage:
		includeIfAfter = """after:"$after",""" if after != "" else ""
		starredAtIfStarred = "STARRED_AT" if context == "starredRepositories" else "PUSHED_AT"
		repoPage = getGithubApiRequest("""
		query {
			user(login:"$login") {
				$context(first:100, """ + includeIfAfter + """orderBy:{direction:DESC, field:""" + starredAtIfStarred + """}){
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
		{"login": username, "context": context, "after": after})["data"]["user"][context]
		repos.extend(repoPage["nodes"])
		hasNextPage = repoPage["pageInfo"]["hasNextPage"] and sourceAlive(repoPage["nodes"][99], lifespan)
		after = repoPage["pageInfo"]["endCursor"]
	return repos


def printIssue(issue):
	utils.logPrint(("[\033[91mClosed\033[00m] " if issue["state"] == "closed" else "")
	+ issue["title"], "bold")
	utils.logPrint(issue["pushedAt"])

def printUser(user):
	utils.logPrint(user["login"], "bold")
	utils.logPrint(user["url"])

def printGist(gist):
	utils.logPrint(gist["description"], "bold")
	utils.logPrint("Files: {}" .format([gFile['name'] for gFile in gist["files"]]), "bold")
	utils.logPrint(gist["url"])

def printRepo(repo):
	try:
		utils.logPrint("{}"
		.format(("[\033[91mArchived\033[00m] " if repo["isArchived"] else "") + repo["name"]), "bold")
	except:
		return
	description = repo["description"] if "description" in repo else "[description]"
	language = repo["primaryLanguage"]["name"] if repo["primaryLanguage"] is not None else "[unknown]"
	licenseName = repo["licenseInfo"]["name"] if repo["licenseInfo"] is not None else "[unknown]"
	pushed = repo["pushedAt"] if "pushedAt" in repo else "[unknown]"
	utils.logPrint("{}\nLanguage: {}, License: {}, Last Pushed: {}"
	.format(description, language, licenseName, pushed))
	utils.logPrint("Link: {}" .format(repo["url"]))


def sourceAlive(repoData, lifespan):
	"""Is source repo alive?
	"""
	return utils.getDatetime(repoData["pushedAt"]) > (datetime.datetime.now() - datetime.timedelta(weeks=lifespan))
