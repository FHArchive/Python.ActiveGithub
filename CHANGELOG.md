# Changelog
All major and minor version changes will be documented in this file. Details of
patch-level version changes can be found in [commit messages](../../commits/master).

## 2020.0 - 2020/01/05
- First release, works pretty well

## 2020.1 - 2020/01/17
- Updated ActiveGithub.py, gitrepo.py, UserReposActive.py. Added UserReposTraffic.py


## 2020.2 - 2020/01/21
- Added GitHubRepl.py with basic functionality - I aim for feature parity with
  github.com
- Additions and optimisations to lib changes to signatures and new functions are
  in bold
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
