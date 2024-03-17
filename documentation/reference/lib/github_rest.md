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
def getGithubApiRequestJson(urlExcBase: str) -> dict[Any, Any]: ...
```



## getListOfAliveForks

[Show source in github_rest.py:62](../../../lib/github_rest.py#L62)

Get list of forked repos that are alive and newer than the source repo.

#### Signature

```python
def getListOfAliveForks(
    repoData: dict[Any, Any], lifespan: int, enableNewer: bool = True
) -> tuple[list[Any], list[Any]]: ...
```



## getListOfRepos

[Show source in github_rest.py:57](../../../lib/github_rest.py#L57)

Get a list of repos of a certain type: "forks", "stargazers".

#### Signature

```python
def getListOfRepos(repoName: str, context: str = "forks") -> list[Any]: ...
```



## getListOfUserRepos

[Show source in github_rest.py:77](../../../lib/github_rest.py#L77)

Get a list of repos using a username and type: "repos"
(user public repos), "subscriptions" (user watching), "stargazing" (stars)

#### Signature

```python
def getListOfUserRepos(username: str, context: str) -> list[Any]: ...
```



## getPaginatedGithubApiRequest

[Show source in github_rest.py:84](../../../lib/github_rest.py#L84)

Get a api request over multiple pages.

#### Signature

```python
def getPaginatedGithubApiRequest(apiUrl: str) -> list[Any]: ...
```



## getReadme

[Show source in github_rest.py:120](../../../lib/github_rest.py#L120)

Get the repo readme.

#### Signature

```python
def getReadme(repoName: str) -> str: ...
```



## getRepo

[Show source in github_rest.py:115](../../../lib/github_rest.py#L115)

Get repo name, owner, last pushed at and url.

#### Signature

```python
def getRepo(repoName: str): ...
```



## getRepoTraffic

[Show source in github_rest.py:105](../../../lib/github_rest.py#L105)

Get a json of the repo traffic. Traffic can be "views", "clones".

#### Signature

```python
def getRepoTraffic(repoName: str, traffic: str): ...
```



## getUser

[Show source in github_rest.py:110](../../../lib/github_rest.py#L110)

Get user login and url.

#### Signature

```python
def getUser(username: str): ...
```



## getUserGists

[Show source in github_rest.py:139](../../../lib/github_rest.py#L139)

Get a list of user gists.

#### Signature

```python
def getUserGists(username: str): ...
```



## printGist

[Show source in github_rest.py:159](../../../lib/github_rest.py#L159)

Print gist function.

#### Signature

```python
def printGist(gist: dict[Any, Any]): ...
```



## printIssue

[Show source in github_rest.py:144](../../../lib/github_rest.py#L144)

Print issue function.

#### Signature

```python
def printIssue(issue: dict[Any, Any]): ...
```



## printRepo

[Show source in github_rest.py:166](../../../lib/github_rest.py#L166)

Print repo function.

#### Signature

```python
def printRepo(repo: dict[Any, Any]): ...
```



## printUser

[Show source in github_rest.py:153](../../../lib/github_rest.py#L153)

Print user function.

#### Signature

```python
def printUser(user: dict[Any, Any]): ...
```



## search

[Show source in github_rest.py:132](../../../lib/github_rest.py#L132)

Code, commits, issues, labels, repositories, users.

#### Signature

```python
def search(searchTerm: str, context: str = "repositories") -> list[Any]: ...
```



## sourceAlive

[Show source in github_rest.py:48](../../../lib/github_rest.py#L48)

Is source repo alive?

#### Signature

```python
def sourceAlive(repoData: dict[Any, Any], lifespan: int) -> bool: ...
```