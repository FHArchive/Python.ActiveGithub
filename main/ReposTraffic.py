#!/usr/bin/env python3
"""Return a list of repos sorted by a score from a 'popularity contest'
can be used to get an indication of more popular repos and provides insight
on where to direct focus
"""
import sys
import os
import argparse
from pathlib import Path
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR) + "/lib")

import json
from os.path import exists
from metprint import LogType
#pylint: disable=import-error
from githubREST import getRepoTraffic
import githubGraph
from utils import printf, getDatetime, getUsernameAndLifespan
#pylint: enable=import-error

def mergeDataWithJson(repoName, trafficType):
	'''Merge data with the userReposTraffic JSON file '''
	if exists("userReposTraffic.json"):
		userReposTraffic = json.loads(open("userReposTraffic.json", "r").read())
	else:
		printf.logPrint("userReposTraffic.json does not exist - creating", LogType.WARNING)
		userReposTraffic = {}
	if repoName not in userReposTraffic:
		printf.logPrint("{} does not exist - creating" .format(repoName), LogType.WARNING)
		userReposTraffic[repoName] = {}
	if trafficType not in userReposTraffic[repoName]:
		printf.logPrint("{} does not exist - creating" .format(trafficType), LogType.WARNING)
		userRepoTrafficType = [{'timestamp': '2000-01-01T00:00:00Z', 'uniques': 0}]
	else:
		userRepoTrafficType = userReposTraffic[repoName][trafficType]

	days = getRepoTraffic(repoName, trafficType)[trafficType]
	for day in days:
		if getDatetime(
			userRepoTrafficType[-1]["timestamp"]) < getDatetime(day["timestamp"]):
			userRepoTrafficType.append({'timestamp': day["timestamp"], 'uniques': day["uniques"]})

	userReposTraffic[repoName][trafficType] = userRepoTrafficType
	with open("userReposTraffic.json", "w") as f:
		json.dump(userReposTraffic, f)


def getJsonData(repoName, trafficType):
	'''Get data from the userReposTraffic JSON file to be used by the rest of
	the program '''
	userRepoTraffic = json.loads(open("userReposTraffic.json", "r").read())[repoName][trafficType]
	returnData = 0
	for trafficEntity in userRepoTraffic:
		returnData += trafficEntity["uniques"]
	return returnData

# ARGPARSE
parser = argparse.ArgumentParser("Get a list of repos with poularity score")
parser.add_argument("-o", "--orgs", action="append",
help="add an org to get traffic for")
parser.add_argument("-u", "--user", action="store_true",
help="return the list of user owned repos?")
args = parser.parse_args()

username, lifespan = getUsernameAndLifespan()

if not args.orgs or not args.user:
	organization = input("Set the organisation name (hit enter if not applicable)\n>")
	if len(organization) == 0:
		printf.logPrint("Organization name not set", LogType.WARNING)
		sourceRepos = githubGraph.getListOfRepos(username)
	else:
		sourceRepos = githubGraph.getListOfRepos(organization, organization=True)
else:
	sourceRepos = []
	for organization in args.orgs:
		sourceRepos += githubGraph.getListOfRepos(organization, organization=True)
	if args.user:
		sourceRepos += githubGraph.getListOfRepos(username)


sortRepos = []
for repoData in sourceRepos:
	repositoryShortName = repoData["name"]
	repositoryName = repoData["owner"]["login"]+"/"+repositoryShortName
	"""Forks
	"""
	aliveForks, _ = githubGraph.getListOfAliveForks(repoData, lifespan, enableNewer=False)
	"""Stars
	"""
	stars = githubGraph.getStargazerCount(repoData["owner"]["login"], repoData["name"])
	"""Clones
	"""
	mergeDataWithJson(repositoryName, "clones")
	clones = getJsonData(repositoryName, "clones")
	"""Views
	"""
	mergeDataWithJson(repositoryName, "views")
	views = getJsonData(repositoryName, "views")
	score = len(aliveForks) * 8 + stars * 4 + clones * 2 + views
	sortRepos.append((score,
	("[\033[91mArchived\033[00m] " if repoData["isArchived"] else "") + repositoryName,
	len(aliveForks), stars, clones, views))


def getKey(item):
	''' Return the key '''
	return item[0]

sortedRepos = sorted(sortRepos, key=getKey, reverse=True)

for repoData in sortedRepos:
	printf.logPrint("{}: score={} ({}:{}:{}:{})"
	.format(repoData[1], repoData[0], repoData[2], repoData[3],
	repoData[4], repoData[5]), LogType.INFO)
