# Github Graph

[Python Index](../README.md#python-index) / [Lib](./index.md#lib) / Github Graph

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
    query: str, variables: dict[str, Any] | None = None
) -> requests.Response: ...
```



## getGithubApiRequestJson

[Show source in github_graph.py:25](../../../lib/github_graph.py#L25)

Use this to get json from api (returns some data to module variables).

#### Signature

```python
def getGithubApiRequestJson(
    query: str, variables: dict[str, Any] | None = None
) -> dict[str, Any]: ...
```



## getListOfAliveForks

[Show source in github_graph.py:95](../../../lib/github_graph.py#L95)

Get list of forked repos that are alive and newer than the source repo.

#### Signature

```python
def getListOfAliveForks(
    repoData: dict[str, Any], lifespan: int, enableNewer: bool = True
) -> tuple[list[Any], list[Any]]: ...
```



## getListOfForks

[Show source in github_graph.py:54](../../../lib/github_graph.py#L54)

Get a list of forks within a certian lifespan (default=520 weeks).

#### Signature

```python
def getListOfForks(owner: str, repoName: str, lifespan: int = 520) -> list: ...
```



## getListOfRepos

[Show source in github_graph.py:181](../../../lib/github_graph.py#L181)

Get a list of repos using a username and type: "repositories"
(user public repos), "watching" (user watching), "starredRepositories" (stars).

#### Signature

```python
def getListOfRepos(
    login: str,
    context: str = "repositories",
    organization: bool = False,
    lifespan: int = 520,
) -> list: ...
```



## getRepo

[Show source in github_graph.py:139](../../../lib/github_graph.py#L139)

Get repo name, owner, last pushed at and url.

#### Signature

```python
def getRepo(owner: str, repoName: str) -> dict[str, Any]: ...
```



## getStargazerCount

[Show source in github_graph.py:109](../../../lib/github_graph.py#L109)

Get a count of stargazers.

#### Signature

```python
def getStargazerCount(owner: str, repoName: str) -> int: ...
```



## getUser

[Show source in github_graph.py:124](../../../lib/github_graph.py#L124)

Get user login and url.

#### Signature

```python
def getUser(username: str) -> dict[str, Any]: ...
```



## getUserGists

[Show source in github_graph.py:160](../../../lib/github_graph.py#L160)

Get a list of user gists.

#### Signature

```python
def getUserGists(username: str) -> list[Any]: ...
```



## printGist

[Show source in github_graph.py:252](../../../lib/github_graph.py#L252)

Print gist function.

#### Signature

```python
def printGist(gist: dict[str, Any]) -> None: ...
```



## printIssue

[Show source in github_graph.py:237](../../../lib/github_graph.py#L237)

Print issue function.

#### Signature

```python
def printIssue(issue: dict[str, Any]) -> None: ...
```



## printRepo

[Show source in github_graph.py:259](../../../lib/github_graph.py#L259)

Print repo function.

#### Signature

```python
def printRepo(repo: dict[str, Any]) -> None: ...
```



## printUser

[Show source in github_graph.py:246](../../../lib/github_graph.py#L246)

Print user function.

#### Signature

```python
def printUser(user: dict[str, Any]) -> None: ...
```



## search

[Show source in github_graph.py:155](../../../lib/github_graph.py#L155)

code, commits, issues, labels, repositories, users.

#### Signature

```python
def search(_searchTerm, _context="repositories") -> None: ...
```



## sourceAlive

[Show source in github_graph.py:280](../../../lib/github_graph.py#L280)

Is source repo alive?.

#### Signature

```python
def sourceAlive(repoData: dict[str, Any], lifespan: int) -> bool: ...
```