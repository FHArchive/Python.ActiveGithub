# github_rest

> Auto-generated documentation for [lib.github_rest](../../lib/github_rest.py) module.

Interface with git v3 api. Used by programs under 'main'.

- [Python](../README.md#python-index) / [Modules](../README.md#python-modules) / [lib](index.md#lib) / github_rest
    - [getGithubApiRequest](#getgithubapirequest)
    - [getGithubApiRequestJson](#getgithubapirequestjson)
    - [getListOfAliveForks](#getlistofaliveforks)
    - [getListOfRepos](#getlistofrepos)
    - [getListOfUserRepos](#getlistofuserrepos)
    - [getPaginatedGithubApiRequest](#getpaginatedgithubapirequest)
    - [getReadme](#getreadme)
    - [getRepo](#getrepo)
    - [getRepoTraffic](#getrepotraffic)
    - [getUser](#getuser)
    - [getUserGists](#getusergists)
    - [printGist](#printgist)
    - [printIssue](#printissue)
    - [printRepo](#printrepo)
    - [printUser](#printuser)
    - [search](#search)
    - [sourceAlive](#sourcealive)

## getGithubApiRequest

[[find in source code]](../../lib/github_rest.py#L34)

```python
def getGithubApiRequest(urlExcBase: str) -> requests.Response:
```

Use this to get json from api (returns some data to module variables).

## getGithubApiRequestJson

[[find in source code]](../../lib/github_rest.py#L25)

```python
def getGithubApiRequestJson(urlExcBase: str) -> dict[(Any, Any)]:
```

Use this to get json from api (returns some data to module variables).

## getListOfAliveForks

[[find in source code]](../../lib/github_rest.py#L62)

```python
def getListOfAliveForks(
    repoData: dict[(Any, Any)],
    lifespan: int,
    enableNewer: bool = True,
) -> tuple[(list[Any], list[Any])]:
```

Get list of forked repos that are alive and newer than the source repo.

## getListOfRepos

[[find in source code]](../../lib/github_rest.py#L57)

```python
def getListOfRepos(repoName: str, context: str = 'forks') -> list[Any]:
```

Get a list of repos of a certain type: "forks", "stargazers".

## getListOfUserRepos

[[find in source code]](../../lib/github_rest.py#L77)

```python
def getListOfUserRepos(username: str, context: str) -> list[Any]:
```

Get a list of repos using a username and type: "repos"
(user public repos), "subscriptions" (user watching), "stargazing" (stars)

## getPaginatedGithubApiRequest

[[find in source code]](../../lib/github_rest.py#L84)

```python
def getPaginatedGithubApiRequest(apiUrl: str) -> list[Any]:
```

Get a api request over multiple pages.

## getReadme

[[find in source code]](../../lib/github_rest.py#L120)

```python
def getReadme(repoName: str) -> str:
```

Get the repo readme.

## getRepo

[[find in source code]](../../lib/github_rest.py#L115)

```python
def getRepo(repoName: str):
```

Get repo name, owner, last pushed at and url.

## getRepoTraffic

[[find in source code]](../../lib/github_rest.py#L105)

```python
def getRepoTraffic(repoName: str, traffic: str):
```

Get a json of the repo traffic. Traffic can be "views", "clones".

## getUser

[[find in source code]](../../lib/github_rest.py#L110)

```python
def getUser(username: str):
```

Get user login and url.

## getUserGists

[[find in source code]](../../lib/github_rest.py#L139)

```python
def getUserGists(username: str):
```

Get a list of user gists.

## printGist

[[find in source code]](../../lib/github_rest.py#L159)

```python
def printGist(gist: dict[(Any, Any)]):
```

Print gist function.

## printIssue

[[find in source code]](../../lib/github_rest.py#L144)

```python
def printIssue(issue: dict[(Any, Any)]):
```

Print issue function.

## printRepo

[[find in source code]](../../lib/github_rest.py#L166)

```python
def printRepo(repo: dict[(Any, Any)]):
```

Print repo function.

## printUser

[[find in source code]](../../lib/github_rest.py#L153)

```python
def printUser(user: dict[(Any, Any)]):
```

Print user function.

## search

[[find in source code]](../../lib/github_rest.py#L132)

```python
def search(searchTerm: str, context: str = 'repositories') -> list[Any]:
```

Code, commits, issues, labels, repositories, users.

## sourceAlive

[[find in source code]](../../lib/github_rest.py#L48)

```python
def sourceAlive(repoData: dict[(Any, Any)], lifespan: int) -> bool:
```

Is source repo alive?
