# Github Graph

[Python Index](../README.md#python-index) /
[Lib](./index.md#lib) /
Github Graph

> Auto-generated documentation for [lib.github_graph](../../../lib/github_graph.py) module.

- [Github Graph](#github-graph)
  - [getGithubApiRequest](#getgithubapirequest)
  - [getGithubApiRequestJson](#getgithubapirequestjson)
  - [getListOfAliveForks](#getlistofaliveforks)
  - [getListOfForks](#getlistofforks)
  - [getListOfRepos](#getlistofrepos)
  - [getRepo](#getrepo)
  - [getStargazerCount](#getstargazercount)
  - [getUser](#getuser)
  - [getUserGists](#getusergists)
  - [printGist](#printgist)
  - [printIssue](#printissue)
  - [printRepo](#printrepo)
  - [printUser](#printuser)
  - [search](#search)
  - [sourceAlive](#sourcealive)

## getGithubApiRequest

[Show source in github_graph.py:34](../../../lib/github_graph.py#L34)

Use this to get raw from api (returns some data to module variables).

#### Signature

```python
def getGithubApiRequest(
    query: str, variables: dict[Any, Any] | None = None
) -> requests.Response:
    ...
```



## getGithubApiRequestJson

[Show source in github_graph.py:25](../../../lib/github_graph.py#L25)

Use this to get json from api (returns some data to module variables).

#### Signature

```python
def getGithubApiRequestJson(
    query: str, variables: dict[Any, Any] | None = None
) -> dict[Any, Any]:
    ...
```



## getListOfAliveForks

[Show source in github_graph.py:94](../../../lib/github_graph.py#L94)

Get list of forked repos that are alive and newer than the source repo.

#### Signature

```python
def getListOfAliveForks(
    repoData: dict[Any, Any], lifespan: int, enableNewer: bool = True
) -> tuple[list[Any], list[Any]]:
    ...
```



## getListOfForks

[Show source in github_graph.py:53](../../../lib/github_graph.py#L53)

Get a list of forks within a certian lifespan (default=520 weeks).

#### Signature

```python
def getListOfForks(owner: str, repoName: str, lifespan: int = 520):
    ...
```



## getListOfRepos

[Show source in github_graph.py:180](../../../lib/github_graph.py#L180)

Get a list of repos using a username and type: "repositories"
(user public repos), "watching" (user watching), "starredRepositories" (stars)

#### Signature

```python
def getListOfRepos(
    login: str,
    context: str = "repositories",
    organization: bool = False,
    lifespan: int = 520,
):
    ...
```



## getRepo

[Show source in github_graph.py:138](../../../lib/github_graph.py#L138)

Get repo name, owner, last pushed at and url.

#### Signature

```python
def getRepo(owner: str, repoName: str) -> dict[Any, Any]:
    ...
```



## getStargazerCount

[Show source in github_graph.py:108](../../../lib/github_graph.py#L108)

Get a count of stargazers.

#### Signature

```python
def getStargazerCount(owner: str, repoName: str) -> int:
    ...
```



## getUser

[Show source in github_graph.py:123](../../../lib/github_graph.py#L123)

Get user login and url.

#### Signature

```python
def getUser(username: str) -> dict[Any, Any]:
    ...
```



## getUserGists

[Show source in github_graph.py:159](../../../lib/github_graph.py#L159)

Get a list of user gists.

#### Signature

```python
def getUserGists(username: str) -> list[Any]:
    ...
```



## printGist

[Show source in github_graph.py:246](../../../lib/github_graph.py#L246)

Print gist function.

#### Signature

```python
def printGist(gist: dict[Any, Any]):
    ...
```



## printIssue

[Show source in github_graph.py:231](../../../lib/github_graph.py#L231)

Print issue function.

#### Signature

```python
def printIssue(issue: dict[Any, Any]):
    ...
```



## printRepo

[Show source in github_graph.py:253](../../../lib/github_graph.py#L253)

Print repo function.

#### Signature

```python
def printRepo(repo: dict[Any, Any]):
    ...
```



## printUser

[Show source in github_graph.py:240](../../../lib/github_graph.py#L240)

Print user function.

#### Signature

```python
def printUser(user: dict[Any, Any]):
    ...
```



## search

[Show source in github_graph.py:154](../../../lib/github_graph.py#L154)

code, commits, issues, labels, repositories, users.

#### Signature

```python
def search(_searchTerm, _context="repositories"):
    ...
```



## sourceAlive

[Show source in github_graph.py:274](../../../lib/github_graph.py#L274)

Is source repo alive?

#### Signature

```python
def sourceAlive(repoData: dict[Any, Any], lifespan: int) -> bool:
    ...
```


