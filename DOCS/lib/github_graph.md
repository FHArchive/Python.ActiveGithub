# github_graph

> Auto-generated documentation for [lib.github_graph](../../lib/github_graph.py) module.

Interface with git v4 api. Used by programs under 'main'.

- [Python](../README.md#python-index) / [Modules](../README.md#python-modules) / [lib](index.md#lib) / github_graph
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

[[find in source code]](../../lib/github_graph.py#L34)

```python
def getGithubApiRequest(
    query: str,
    variables: dict[(Any, Any)] | None = None,
) -> requests.Response:
```

Use this to get raw from api (returns some data to module variables).

## getGithubApiRequestJson

[[find in source code]](../../lib/github_graph.py#L25)

```python
def getGithubApiRequestJson(
    query: str,
    variables: dict[(Any, Any)] | None = None,
) -> dict[(Any, Any)]:
```

Use this to get json from api (returns some data to module variables).

## getListOfAliveForks

[[find in source code]](../../lib/github_graph.py#L94)

```python
def getListOfAliveForks(
    repoData: dict[(Any, Any)],
    lifespan: int,
    enableNewer: bool = True,
) -> tuple[(list[Any], list[Any])]:
```

Get list of forked repos that are alive and newer than the source repo.

## getListOfForks

[[find in source code]](../../lib/github_graph.py#L53)

```python
def getListOfForks(owner: str, repoName: str, lifespan: int = 520):
```

Get a list of forks within a certian lifespan (default=520 weeks).

## getListOfRepos

[[find in source code]](../../lib/github_graph.py#L180)

```python
def getListOfRepos(
    login: str,
    context: str = 'repositories',
    organization: bool = False,
    lifespan: int = 520,
):
```

Get a list of repos using a username and type: "repositories"
(user public repos), "watching" (user watching), "starredRepositories" (stars)

## getRepo

[[find in source code]](../../lib/github_graph.py#L138)

```python
def getRepo(owner: str, repoName: str) -> dict[(Any, Any)]:
```

Get repo name, owner, last pushed at and url.

## getStargazerCount

[[find in source code]](../../lib/github_graph.py#L108)

```python
def getStargazerCount(owner: str, repoName: str) -> int:
```

Get a count of stargazers.

## getUser

[[find in source code]](../../lib/github_graph.py#L123)

```python
def getUser(username: str) -> dict[(Any, Any)]:
```

Get user login and url.

## getUserGists

[[find in source code]](../../lib/github_graph.py#L159)

```python
def getUserGists(username: str) -> list[Any]:
```

Get a list of user gists.

## printGist

[[find in source code]](../../lib/github_graph.py#L246)

```python
def printGist(gist: dict[(Any, Any)]):
```

Print gist function.

## printIssue

[[find in source code]](../../lib/github_graph.py#L231)

```python
def printIssue(issue: dict[(Any, Any)]):
```

Print issue function.

## printRepo

[[find in source code]](../../lib/github_graph.py#L253)

```python
def printRepo(repo: dict[(Any, Any)]):
```

Print repo function.

## printUser

[[find in source code]](../../lib/github_graph.py#L240)

```python
def printUser(user: dict[(Any, Any)]):
```

Print user function.

## search

[[find in source code]](../../lib/github_graph.py#L154)

```python
def search(_searchTerm, _context='repositories'):
```

code, commits, issues, labels, repositories, users.

## sourceAlive

[[find in source code]](../../lib/github_graph.py#L274)

```python
def sourceAlive(repoData: dict[(Any, Any)], lifespan: int) -> bool:
```

Is source repo alive?
