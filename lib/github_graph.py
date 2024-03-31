"""Interface with git v4 api. Used by programs under 'main'."""

from __future__ import annotations

import datetime
import time
from typing import Any

import requests
from requests_cache import install_cache

from lib.metprint import LogType
from lib.utils import getDatetime, getPassword, printf

install_cache(
	"github_api",
	"sqlite",
	expire_after=60 * 60 * 12,
	allowable_codes=(200,),
	allowable_methods=("GET", "POST"),
)


def getGithubApiRequestJson(query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
	"""Use this to get json from api (returns some data to module variables)."""
	requestJson = getGithubApiRequest(query, variables).json()
	if "message" in requestJson or "errors" in requestJson:
		printf.logPrint("[GRAPHQL] Some error has occurred", LogType.ERROR)
		printf.logPrint(requestJson)
	return requestJson


def getGithubApiRequest(query: str, variables: dict[str, Any] | None = None) -> requests.Response:
	"""Use this to get raw from api (returns some data to module variables)."""
	variables = variables or {}
	for key in variables:
		query = query.replace("$" + key, variables[key])
	request = requests.post(
		"https://api.github.com/graphql",
		json={"query": query},
		headers={"Authorization": "bearer " + getPassword()},
		timeout=30,
	)
	if int(request.headers["X-RateLimit-Remaining"]) < 1:
		printf.logPrint(
			"Remaining rate limit is zero. "
			f"Try again at {time.ctime(float(request.headers['X-RateLimit-Reset']))}",
			LogType.ERROR,
		)
	return request


def getListOfForks(owner: str, repoName: str, lifespan: int = 520) -> list:
	"""Get a list of forks within a certian lifespan (default=520 weeks)."""
	repos = []
	hasNextPage = True
	after = ""
	while hasNextPage:
		includeIfAfter = """after:"$after",""" if after != "" else ""
		repoPage = getGithubApiRequestJson(
			"""
		query {
			repository(owner:"$owner", name:"$name") {
				forks(first:100,"""
			+ includeIfAfter
			+ """orderBy:{direction:DESC, field:PUSHED_AT}){
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
			{"owner": owner, "name": repoName, "after": after},
		)["data"]["repository"]["forks"]
		repos.extend(repoPage["nodes"])
		hasNextPage = repoPage["pageInfo"]["hasNextPage"] and sourceAlive(
			repoPage["nodes"][99], lifespan
		)
		after = repoPage["pageInfo"]["endCursor"]
	return repos


def getListOfAliveForks(
	repoData: dict[str, Any], lifespan: int, *, enableNewer: bool = True
) -> tuple[list[Any], list[Any]]:
	"""Get list of forked repos that are alive and newer than the source repo."""
	forkedRepos = getListOfForks(repoData["owner"]["login"], repoData["name"], lifespan=lifespan)
	aliveRepos = []
	for forkedRepo in forkedRepos:
		isAlive = sourceAlive(forkedRepo, lifespan)
		isNewer = getDatetime(forkedRepo["pushedAt"]) > getDatetime(repoData["pushedAt"])
		if (isAlive and isNewer) or (isAlive and not enableNewer):
			aliveRepos.append(forkedRepo)
	return aliveRepos, forkedRepos


def getStargazerCount(owner: str, repoName: str) -> int:
	"""Get a count of stargazers."""
	return getGithubApiRequestJson(
		"""
	query {
		repository(owner:"$owner", name:"$name") {
			stargazers{
				totalCount
			}
		}
	}""",
		{"owner": owner, "name": repoName},
	)["data"]["repository"]["stargazers"]["totalCount"]


def getUser(username: str) -> dict[str, Any]:
	"""Get user login and url."""
	return getGithubApiRequestJson(
		"""
		query {
			user(login:"$login") {
				login
				url
			}
		}
		""",
		{"login": username},
	)["data"]["user"]


def getRepo(owner: str, repoName: str) -> dict[str, Any]:
	"""Get repo name, owner, last pushed at and url."""
	return getGithubApiRequestJson(
		"""
		query {
			repository(owner:"$owner", name:"$name") {
				name
				owner{login}
				pushedAt
				url
			}
		}""",
		{"owner": owner, "name": repoName},
	)["data"]["repository"]


def search(_searchTerm, _context="repositories") -> None:
	"""code, commits, issues, labels, repositories, users."""
	return


def getUserGists(username: str) -> list[Any]:
	"""Get a list of user gists."""
	return getGithubApiRequestJson(
		"""
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
		{"login": username},
	)["data"]["user"]["gists"]["nodes"]


def getListOfRepos(
	login: str,
	context: str = "repositories",
	organization: bool = False,
	lifespan: int = 520,
) -> list:
	"""Get a list of repos using a username and type: "repositories"
	(user public repos), "watching" (user watching), "starredRepositories" (stars).
	"""
	repos = []
	hasNextPage = True
	after = ""
	starredOrPushed = "STARRED_AT" if context == "starredRepositories" else "PUSHED_AT"
	userOrOrg = "organization" if organization else "user"
	while hasNextPage:
		includeIfAfter = """after:"$after",""" if after != "" else ""

		raw_data = getGithubApiRequestJson(
			"""
		query {
			"""
			+ userOrOrg
			+ """(login:"$login") {
				$context(first:100,"""
			+ includeIfAfter
			+ """orderBy:{direction:DESC, field:"""
			+ starredOrPushed
			+ """}){
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
			{"login": login, "context": context, "after": after},
		)
		repoPage = raw_data["data"][userOrOrg][context]
		repos.extend(repoPage["nodes"])
		hasNextPage = repoPage["pageInfo"]["hasNextPage"] and sourceAlive(
			repoPage["nodes"][99], lifespan
		)
		after = repoPage["pageInfo"]["endCursor"]
	return repos


def printIssue(issue: dict[str, Any]) -> None:
	"""Print issue function."""
	printf.logPrint(
		("[\033[91mClosed\033[00m] " if issue["state"] == "closed" else "") + issue["title"],
		LogType.BOLD,
	)
	printf.logPrint(issue["pushedAt"])


def printUser(user: dict[str, Any]) -> None:
	"""Print user function."""
	printf.logPrint(user["login"], LogType.BOLD)
	printf.logPrint(user["url"])


def printGist(gist: dict[str, Any]) -> None:
	"""Print gist function."""
	printf.logPrint(gist["description"], LogType.BOLD)
	printf.logPrint(f"Files: {[gFile['name'] for gFile in gist['files']]}", LogType.BOLD)
	printf.logPrint(gist["url"])


def printRepo(repo: dict[str, Any]) -> None:
	"""Print repo function."""
	if all(key in repo for key in ("isArchived", "name")):
		printf.logPrint(
			("[\033[91mArchived\033[00m] " if repo["isArchived"] else "") + repo["name"],
			LogType.BOLD,
		)
	else:
		return
	description = repo.get("description", "[description]")
	language = (
		repo["primaryLanguage"]["name"] if repo["primaryLanguage"] is not None else "[unknown]"
	)
	licenseName = repo["licenseInfo"]["name"] if repo["licenseInfo"] is not None else "[unknown]"
	pushed = repo.get("pushedAt", "[unknown]")
	printf.logPrint(
		f"{description}\nLanguage: {language}, License: {licenseName}, Last Pushed: {pushed}"
	)
	printf.logPrint(f"Link: {repo['url']}")


def sourceAlive(repoData: dict[str, Any], lifespan: int) -> bool:
	"""Is source repo alive?."""
	return getDatetime(repoData["pushedAt"]) > (
		datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(weeks=lifespan)
	)
