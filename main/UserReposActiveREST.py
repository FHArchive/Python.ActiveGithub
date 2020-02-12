#!/usr/bin/env python3

import sys
import os
from pathlib import Path
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR) + "/lib")

import githubREST
import json
import utils

def forEachRepo(sourceRepo):
	"""Is source repo alive?
	"""
	printStr = ["dead", "error"]
	if githubREST.sourceAlive(sourceRepo, death):
		printStr = ["alive", "success"]
	utils.logPrint("Source repo is {}! Head to {}"
	.format(printStr[0], sourceRepo["html_url"]), printStr[1])

	"""Get list of forked repos that are alive and newer than the source repo
	"""
	aliveRepos, forkedRepos = githubREST.getListOfAliveForks(repo, death)

	utils.logPrint("{} out of {} Forked repos are alive and newer than the source!"
	.format(len(aliveRepos), len(forkedRepos)), "bold")
	for aliveRepo in aliveRepos:
		githubREST.printRepo(aliveRepo)


username, death = utils.getUsernameAndLifespan()


choice = input("User repos, watched or starred (R/w/s)>")
if choice.lower() == "s":
	"""Get list of user starred
	"""
	starredRepos = githubREST.getListOfUserRepos(username, "starred")
	for repo in starredRepos:
		forEachRepo(repo)

elif choice.lower() == "w":
	"""Get list of user watched
	"""
	watchedRepos = githubREST.getListOfUserRepos(username, "subscriptions")
	for repo in watchedRepos:
		forEachRepo(repo)

else:
	"""Get list of user repos
	"""
	sourceRepos = githubREST.getListOfUserRepos(username, "repos")
	for repo in sourceRepos:
		forEachRepo(repo)
