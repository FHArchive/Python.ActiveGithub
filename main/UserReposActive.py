#!/usr/bin/env python3
"""Quickly identify repos that are active and inactive from a user's personal
repos, starred and watching
"""
import sys
import os
from pathlib import Path
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR) + "/lib")

import githubGraph
import utils

def forEachRepo(sourceRepo):
	"""Is source repo alive?
	"""
	printStr = ["dead", "error"]
	if githubGraph.sourceAlive(sourceRepo, death):
		printStr = ["alive", "success"]
	utils.logPrint("Source repo is {}! Head to {}"
	.format(printStr[0], sourceRepo["url"]), printStr[1])

	"""Get list of forked repos that are alive and newer than the source repo
	"""
	aliveRepos, forkedRepos = githubGraph.getListOfAliveForks(repo, death)

	utils.logPrint("{} out of {} Forked repos are alive and newer than the source!"
	.format(len(aliveRepos), len(forkedRepos)), "bold")
	for aliveRepo in aliveRepos:
		githubGraph.printRepo(aliveRepo)


username, death = utils.getUsernameAndLifespan()


choice = input("User repos, watched or starred (R/w/s)>")
if choice.lower() == "s":
	"""Get list of user starred
	"""
	starredRepos = githubGraph.getListOfUserRepos(username, "starredRepositories")
	for repo in starredRepos:
		forEachRepo(repo)

elif choice.lower() == "w":
	"""Get list of user watched
	"""
	watchedRepos = githubGraph.getListOfUserRepos(username, "watching")
	for repo in watchedRepos:
		forEachRepo(repo)

else:
	"""Get list of user repos
	"""
	sourceRepos = githubGraph.getListOfUserRepos(username, "repositories")
	for repo in sourceRepos:
		forEachRepo(repo)
