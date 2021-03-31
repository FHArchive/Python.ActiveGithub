"""Interface with git v3 api. Used by programs under 'main'.
"""
from __future__ import annotations

import datetime
import time
from typing import Any

import requests
import urllib3
from metprint import LogType
from requests_cache import install_cache

from lib.utils import AUTH, getDatetime, printf

install_cache(
	"github_api",
	"sqlite",
	60 * 60 * 12,
	allowable_codes=(200,),
	allowable_methods=("GET", "POST"),
)


def getGithubApiRequestJson(urlExcBase: str) -> dict[Any, Any]:  # yapf: disable
	"""Use this to get json from api (returns some data to module variables)."""
	requestJson = getGithubApiRequest(urlExcBase).json()
	if "message" in requestJson:
		printf.logPrint("Some error has occurred", LogType.ERROR)
		printf.logPrint(requestJson)
	return requestJson


def getGithubApiRequest(urlExcBase: str) -> requests.Response:
	"""Use this to get json from api (returns some data to module variables)."""
	fullUrl = "https://api.github.com/" + urlExcBase
	request = requests.get(url=fullUrl, auth=AUTH)

	if int(request.headers["X-RateLimit-Remaining"]) < 1:
		printf.logPrint(
			"Remaining rate limit is zero. Try again at {}".format(
				str(time.ctime(float(request.headers["X-RateLimit-Reset"])))
			),
			LogType.ERROR,
		)
	return request


def sourceAlive(repoData: dict[Any, Any], lifespan: int) -> bool:
	"""Is source repo alive?"""
	if "pushed_at" in repoData:
		pushedAt = repoData["pushed_at"]
	else:
		pushedAt = repoData["pushedAt"]
	return getDatetime(pushedAt) + datetime.timedelta(weeks=lifespan) > datetime.datetime.now()


def getListOfRepos(repoName: str, context: str = "forks") -> list[Any]:
	"""Get a list of repos of a certain type: "forks", "stargazers"."""
	return getPaginatedGithubApiRequest("repos/" + repoName + "/" + context)


def getListOfAliveForks(
	repoData: dict[Any, Any], lifespan: int, enableNewer: bool = True
) -> tuple[list[Any], list[Any]]:
	"""Get list of forked repos that are alive and newer than the source repo."""
	forkedRepos = getListOfRepos(repoData["full_name"])
	aliveRepos = []
	for forkedRepo in forkedRepos:
		forkedRepoPushedAt = getDatetime(forkedRepo["pushed_at"])
		isAlive = forkedRepoPushedAt + datetime.timedelta(weeks=lifespan) > datetime.datetime.now()
		isNewer = forkedRepoPushedAt > getDatetime(repoData["pushed_at"])
		if (isAlive and isNewer) or (isAlive and not enableNewer):
			aliveRepos.append(forkedRepo)
	return aliveRepos, forkedRepos


def getListOfUserRepos(username: str, context: str) -> list[Any]:
	"""Get a list of repos using a username and type: "repos" ...

	(user public repos), "subscriptions" (user watching), "stargazing" (stars)
	"""
	return getPaginatedGithubApiRequest("users/" + username + "/" + context)


def getPaginatedGithubApiRequest(apiUrl: str) -> list[Any]:
	"""Get a api request over multiple pages."""
	firstPage = getGithubApiRequest(apiUrl + "?per_page=100")
	iterable = firstPage.json()
	try:
		lastPage = int(firstPage.links["last"]["url"].split("&page=")[1])
	except IndexError:
		lastPage = 1
	pageLimit = 10
	if lastPage > pageLimit:
		printf.logPrint(
			"There are over {pageLimit} pages! Limiting to {pageLimit} pages".format(
				pageLimit=pageLimit
			),
			LogType.WARNING,
		)
		lastPage = pageLimit
	for page in range(2, lastPage + 1):
		iterationsInstance = getGithubApiRequestJson(apiUrl + "?per_page=100&page=" + str(page))
		iterable.extend(iterationsInstance)
	return iterable


def getRepoTraffic(repoName: str, traffic: str):
	"""Get a json of the repo traffic. Traffic can be "views", "clones"."""
	return getGithubApiRequestJson("repos/" + repoName + "/traffic/" + traffic)


def getUser(username: str):
	"""Get user login and url."""
	return getGithubApiRequestJson("users/" + username)


def getRepo(repoName: str):
	"""Get repo name, owner, last pushed at and url."""
	return getGithubApiRequestJson("repos/" + repoName)


def getReadme(repoName: str) -> str:
	"""Get the repo readme."""
	http = urllib3.PoolManager()
	head = urllib3.make_headers(user_agent="python.activegithub")
	response = http.request(
		"GET",
		getGithubApiRequestJson("repos/" + repoName + "/readme")["download_url"],
		headers=head,
	)
	return response.data.decode("utf-8")


def search(searchTerm: str, context: str = "repositories") -> list[Any]:
	"""Code, commits, issues, labels, repositories, users."""
	return getGithubApiRequestJson(
		"search/" + context + "?q=" + searchTerm + "&sort=stargazers&per_page=100"
	)["items"]


def getUserGists(username: str):
	"""Get a list of user gists."""
	return getPaginatedGithubApiRequest("users/" + username + "/gists")


def printIssue(issue: dict[Any, Any]):
	"""Print issue function."""
	printf.logPrint(
		("[\033[91mClosed\033[00m] " if issue["state"] == "closed" else "") + issue["title"],
		LogType.BOLD,
	)
	printf.logPrint(issue["updated_at"])


def printUser(user: dict[Any, Any]):
	"""Print user function."""
	printf.logPrint(user["login"], LogType.BOLD)
	printf.logPrint(user["html_url"])


def printGist(gist: dict[Any, Any]):
	"""Print gist function."""
	printf.logPrint(gist["description"], LogType.BOLD)
	printf.logPrint("Files: {}".format(list(gist["files"].keys())), LogType.BOLD)
	printf.logPrint(gist["html_url"])


def printRepo(repo: dict[Any, Any]):
	"""Print repo function."""
	if all(key in repo for key in ("archived", "name")):
		printf.logPrint(
			"{}".format(("[\033[91mArchived\033[00m] " if repo["archived"] else "") + repo["name"]),
			LogType.BOLD,
		)
	else:
		return
	description = repo["description"] if "description" in repo else "[description]"
	language = repo["language"] if "language" in repo else "[unknown]"
	try:
		licenseName = repo["license"]["name"]
	except (KeyError, TypeError):
		licenseName = "[unknown]"
	updated = repo["updated_at"] if "updated_at" in repo else "[unknown]"
	printf.logPrint(
		"{}\nLanguage: {}, License: {}, Last Updated: {}".format(
			description, language, licenseName, updated
		)
	)
	printf.logPrint("Link: {}".format(repo["html_url"]))
