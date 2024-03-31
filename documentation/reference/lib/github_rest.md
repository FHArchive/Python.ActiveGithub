# Github Rest

[Python Index](../README.md#python-index) / [Lib](./index.md#lib) / Github Rest

> Auto-generated documentation for [lib.github_rest](../../../lib/github_rest.py) module.

- [Github Rest](#github-rest)
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

[Show source in github_rest.py:34](../../../lib/github_rest.py#L34)

Use this to get json from api (returns some data to module variables).

#### Signature

```python
def getGithubApiRequest(urlExcBase: str) -> requests.Response: ...
```



## getGithubApiRequestJson

[Show source in github_rest.py:25](../../../lib/github_rest.py#L25)

Use this to get json from api (returns some data to module variables).

#### Signature

```python
def getGithubApiRequestJson(urlExcBase: str) -> dict[str, Any]: ...
```



## getListOfAliveForks

[Show source in github_rest.py:61](../../../lib/github_rest.py#L61)

Get list of forked repos that are alive and newer than the source repo.

#### Signature

```python
def getListOfAliveForks(
    repoData: dict[str, Any], lifespan: int, enableNewer: bool = True
) -> tuple[list[Any], list[Any]]: ...
```



## getListOfRepos

[Show source in github_rest.py:56](../../../lib/github_rest.py#L56)

Get a list of repos of a certain type: "forks", "stargazers".

#### Signature

```python
def getListOfRepos(repoName: str, context: str = "forks") -> list[Any]: ...
```



## getListOfUserRepos

[Show source in github_rest.py:78](../../../lib/github_rest.py#L78)

Get a list of repos using a username and type: "repos"
(user public repos), "subscriptions" (user watching), "stargazing" (stars).

#### Signature

```python
def getListOfUserRepos(username: str, context: str) -> list[Any]: ...
```



## getPaginatedGithubApiRequest

[Show source in github_rest.py:85](../../../lib/github_rest.py#L85)

Get a api request over multiple pages.

#### Signature

```python
def getPaginatedGithubApiRequest(apiUrl: str) -> list[Any]: ...
```



## getReadme

[Show source in github_rest.py:121](../../../lib/github_rest.py#L121)

Get the repo readme.

#### Signature

```python
def getReadme(repoName: str) -> str: ...
```



## getRepo

[Show source in github_rest.py:116](../../../lib/github_rest.py#L116)

Get repo name, owner, last pushed at and url.

#### Signature

```python
def getRepo(repoName: str) -> dict[str, Any]: ...
```



## getRepoTraffic

[Show source in github_rest.py:106](../../../lib/github_rest.py#L106)

Get a json of the repo traffic. Traffic can be "views", "clones".

#### Signature

```python
def getRepoTraffic(repoName: str, traffic: str) -> dict[str, Any]: ...
```



## getUser

[Show source in github_rest.py:111](../../../lib/github_rest.py#L111)

Get user login and url.

#### Signature

```python
def getUser(username: str) -> dict[str, Any]: ...
```



## getUserGists

[Show source in github_rest.py:140](../../../lib/github_rest.py#L140)

Get a list of user gists.

#### Signature

```python
def getUserGists(username: str): ...
```



## printGist

[Show source in github_rest.py:160](../../../lib/github_rest.py#L160)

Print gist function.

#### Signature

```python
def printGist(gist: dict[str, Any]) -> None: ...
```



## printIssue

[Show source in github_rest.py:145](../../../lib/github_rest.py#L145)

Print issue function.

#### Signature

```python
def printIssue(issue: dict[str, Any]) -> None: ...
```



## printRepo

[Show source in github_rest.py:167](../../../lib/github_rest.py#L167)

Print repo function.

#### Signature

```python
def printRepo(repo: dict[str, Any]) -> None: ...
```



## printUser

[Show source in github_rest.py:154](../../../lib/github_rest.py#L154)

Print user function.

#### Signature

```python
def printUser(user: dict[str, Any]) -> None: ...
```



## search

[Show source in github_rest.py:133](../../../lib/github_rest.py#L133)

Code, commits, issues, labels, repositories, users.

#### Signature

```python
def search(searchTerm: str, context: str = "repositories") -> list[Any]: ...
```



## sourceAlive

[Show source in github_rest.py:48](../../../lib/github_rest.py#L48)

Is source repo alive?.

#### Signature

```python
def sourceAlive(repoData: dict[str, Any], lifespan: int) -> bool: ...
```