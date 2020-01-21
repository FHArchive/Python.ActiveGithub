#!/usr/bin/env python3
import gitrepo
import json
from os.path import exists

def mergeDataWithJson(repoName, trafficType):
	if exists("userReposTraffic.json"):
		userReposTraffic = json.loads(open("userReposTraffic.json", "r").read())
	else:
		gitrepo.logPrint("userReposTraffic.json does not exist - creating", "warning")
		userReposTraffic = {}
	if repoName not in userReposTraffic:
		gitrepo.logPrint("{} does not exist - creating" .format(repoName), "warning")
		userReposTraffic[repoName] = {}
	if trafficType not in userReposTraffic[repoName]:
		gitrepo.logPrint("{} does not exist - creating" .format(trafficType), "warning")
		userRepoTrafficType = [{'timestamp': '2000-01-01T00:00:00Z', 'uniques': 0}]
	else:
		userRepoTrafficType = userReposTraffic[repoName][trafficType]

	days = gitrepo.getRepoTraffic(repoName, trafficType)[trafficType]
	for day in days:
		if gitrepo.getDatetime(
			userRepoTrafficType[-1]["timestamp"]) < gitrepo.getDatetime(day["timestamp"]):
			userRepoTrafficType.append({'timestamp': day["timestamp"], 'uniques': day["uniques"]})

	userReposTraffic[repoName][trafficType] = userRepoTrafficType
	with open("userReposTraffic.json", "w") as f:
		json.dump(userReposTraffic, f)


def getJsonData(repoName, trafficType):
	userRepoTraffic = json.loads(open("userReposTraffic.json", "r").read())[repoName][trafficType]
	returnData = 0
	for trafficEntity in userRepoTraffic:
		returnData += trafficEntity["uniques"]
	return returnData



username, lifespan = gitrepo.getUsernameAndLifespan()
sourceRepos = gitrepo.getListOfUserRepos(username, "repos")
sortRepos = []
for repo in sourceRepos:
	repositoryName = repo["full_name"]
	"""Forks
	"""
	aliveForks, _ = gitrepo.getListOfAliveForks(repo, lifespan, enableNewer=False)
	"""Stars
	"""
	allStars = gitrepo.getListOfRepos(repositoryName, context="stargazers")
	"""Clones
	"""
	mergeDataWithJson(repositoryName, "clones")
	clones = getJsonData(repositoryName, "clones")
	"""Views
	"""
	mergeDataWithJson(repositoryName, "views")
	views = getJsonData(repositoryName, "views")
	score = len(aliveForks) * 8 + len(allStars) * 4 + clones * 2 + views
	sortRepos.append((score,
	("[\033[91mArchived\033[00m] " if repo["archived"] else "") + repositoryName,
	len(aliveForks), len(allStars), clones, views))


def getKey(item):
	return item[0]

sortedRepos = sorted(sortRepos, key=getKey, reverse=True)

for repo in sortedRepos:
	gitrepo.logPrint("{}: score={} ({}:{}:{}:{})"
	.format(repo[1], repo[0], repo[2], repo[3],
	repo[4], repo[5]), "info")
