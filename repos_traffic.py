#!/usr/bin/env python3
"""Return a list of repos sorted by a score from a 'popularity contest'
can be used to get an indication of more popular repos and provides insight
on where to direct focus
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from metprint import LogType

from lib import github_graph
from lib.github_rest import getRepoTraffic
from lib.utils import getDatetime, getUsernameAndLifespan, printf


class CachedData:
	"""Cached data for repo traffic. Has a file (to read from on init and write
	back to with the writeBack function) and data - a py dict representing the
	json backed up to the cache file.
	"""

	def __init__(self) -> None:
		self.file = Path("userReposTraffic.json")
		self.data = json.loads(self.file.read_text(encoding="utf-8")) if self.file.exists() else {}

	def mergeData(self, repoName: str, trafficType: str):
		"""Merge traffic type for a repo with the traffic cache

		Args:
			repoName (str): name of the repo to get traffic info for
			trafficType (str): type of traffic. views | clones
		"""
		if repoName not in self.data:
			printf.logPrint(f"{repoName} does not exist - creating", LogType.WARNING)
			self.data[repoName] = {}
		if trafficType not in self.data[repoName]:
			printf.logPrint(f"{trafficType} does not exist - creating", LogType.WARNING)
			userRepoTrafficType = [{"timestamp": "2000-01-01T00:00:00Z", "uniques": 0}]
		else:
			userRepoTrafficType = self.data[repoName][trafficType]

		rawTraffic = getRepoTraffic(repoName, trafficType)
		days = (
			getRepoTraffic(repoName, trafficType)[trafficType] if trafficType in rawTraffic else []
		)
		for day in days:
			if getDatetime(userRepoTrafficType[-1]["timestamp"]) < getDatetime(day["timestamp"]):
				userRepoTrafficType.append(
					{"timestamp": day["timestamp"], "uniques": day["uniques"]}
				)

		self.data[repoName][trafficType] = userRepoTrafficType

	def writeBack(self):
		"""Write back to the cache file"""
		Path(self.file).write_text(json.dumps(self.data), encoding="utf-8")

	def getData(self, repoName: str, trafficType: str):
		"""Get data from the userReposTraffic JSON file to be used by the rest of the program"""
		userRepoTraffic = self.data[repoName][trafficType]
		returnData = 0
		for trafficEntity in userRepoTraffic:
			returnData += trafficEntity["uniques"]
		return returnData


parser = argparse.ArgumentParser("Get a list of repos with popularity score")
parser.add_argument(
	"-o",
	"--orgs",
	action="append",
	nargs="+",
	help="add an org to get traffic for",
)
parser.add_argument(
	"-u",
	"--user",
	action="store_true",
	help="return the list of user owned repos?",
)
args = parser.parse_args()
username, lifespan = getUsernameAndLifespan()

if args.orgs is None and not args.user:
	organization = input("Set the organisation name (hit enter if not applicable)\n>")
	if len(organization) == 0:
		printf.logPrint("Organization name not set", LogType.WARNING)
		sourceRepos = github_graph.getListOfRepos(username)
	else:
		sourceRepos = github_graph.getListOfRepos(organization, organization=True)
else:
	sourceRepos = []
	for organization in sum(args.orgs, []):
		sourceRepos += github_graph.getListOfRepos(organization, organization=True)
	if args.user:
		sourceRepos += github_graph.getListOfRepos(username)

sortRepos = []
cachedData = CachedData()
for repoData in sourceRepos:
	repositoryShortName = repoData["name"]
	repositoryName = repoData["owner"]["login"] + "/" + repositoryShortName
	"""Forks
	"""
	aliveForks, _ = github_graph.getListOfAliveForks(repoData, lifespan, enableNewer=False)
	"""Stars
	"""
	stars = github_graph.getStargazerCount(repoData["owner"]["login"], repoData["name"])
	"""Clones
	"""
	cachedData.mergeData(repositoryName, "clones")
	clones = cachedData.getData(repositoryName, "clones")
	"""Views
	"""
	cachedData.mergeData(repositoryName, "views")
	views = cachedData.getData(repositoryName, "views")
	score = len(aliveForks) * 8 + stars * 4 + clones * 2 + views
	sortRepos.append(
		(
			score,
			("[\033[91mArchived\033[00m] " if repoData["isArchived"] else "") + repositoryName,
			len(aliveForks),
			stars,
			clones,
			views,
		)
	)

cachedData.writeBack()


def getKey(item: list[Any]):
	"""Return the key"""
	return item[0]


sortedRepos = sorted(sortRepos, key=getKey, reverse=True)

for repoData in sortedRepos:
	printf.logPrint(
		f"{repoData[1]}: score={repoData[0]} ({repoData[2]}:{repoData[3]}:{repoData[4]}:{repoData[5]})",
		LogType.INFO,
	)
