# Changelog
All major and minor version changes will be documented in this file. Details of
patch-level version changes can be found in [commit messages](../../commits/master).

## 2021.0.1 - 2021/03/31
- Fix bug with GitHub Graph causing post requests to not be cached
- Clean-up

## 2021 - 2021/03/04
- Use requests_cache to decrease the time per repeated API call
  from 0.25s to < 0.01s for GitHub REST


## 2020.7 - 2020/10/30
- Using `urllib3` instead of requests (tiny speed advantages)
- Type hinting
- Drop py < 3.7

## 2020.6.1 - 2020/04/29
- Use argparse for ReposTraffic.py
- Linting fixes
- Use catpandoc to process readme markdown

## 2020.6 - 2020/04/18
- Rename UserReposTraffic.py to ReposTraffic.py
- ReposTraffic.py can be used to get traffic info for organizations
- Swap out utils logprint for metprint because I can (Currently using
FHFormatter but this can be swapped out)
- githubGraph.py signature change (below) so a list of repos can be fetched
for organizations
```python
getListOfUserRepos(username, context="repositories", lifespan=520):
getListOfRepos(login, context="repositories", organization=False, lifespan=520):
```

## 2020.5 - 2020/02/26
- Updated ActiveGithub.py to use GitHub API v4

## 2020.4 - 2020/02/12
- Streamlining, use of GitHub API v4 as it offers significant speed improvements
(getGithubApiRequest 3.7s to 0.7s per call - 81% speed improvement when getting
a list of watched repos that are alive and newer than user starred repos)

## 2020.3 - 2020/01/22
- Optimisations to getPaginatedGithubApiRequest (12.49s to 8.94s per call) - 28%
  speed improvement when getting a list of forked repos that are alive and newer
  than user starred repos
- Changes to signatures and new functions are in bold
	- **printIssue**(issue)
	- **printUser**(user)
	- **printGist**(gist)
	- **printRepo**(repo)

## 2020.2 - 2020/01/21
- Added GitHubRepl.py with basic functionality - I aim for feature parity with
  github.com
- Changes to signatures and new functions are in bold
	- getGithubApiRequest(urlExcBase, **jsonOnly=True**)
	- sourceAlive(**repoData**, lifespan)
	- getListOfAliveForks(**repoData**, lifespan, enableNewer=True)
	- param "data" has been renamed to "**context**"
	- **getUser**(username)
	- **getRepo**(repoName)
	- **getReadme**(repoName)
	- **search**(searchTerm, context="repositories")
- Optimisations of lib and UserReposActive (UserReposActive.py:5(forEachRepo)
  originally took 10.92s and now takes 9.197s per call) - 15% speed improvement
  Using cProfile

## 2020.1 - 2020/01/17
- Updated ActiveGithub.py, gitrepo.py, UserReposActive.py. Added UserReposTraffic.py

## 2020.0 - 2020/01/05
- First release, works pretty well
