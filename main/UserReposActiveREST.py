#!/usr/bin/env python3
"""Quickly identify repos that are active and inactive from a user's personal
repos, starred and watching

Note that this is the REST version and is less optimised than the Graph version
This has been kept so a comparison can be made
"""
import sys
import os
from pathlib import Path
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR) + "/lib")

from metprint import LogType
import githubREST
from utils import printf, getUsernameAndLifespan

def forEachRepo(sourceRepo):
	"""Is source repo alive?
	"""
	printStr = ["dead", LogType.ERROR]
	if githubREST.sourceAlive(sourceRepo, death):
		printStr = ["alive", LogType.SUCCESS]
	printf.logPrint("Source repo is {}! Head to {}"
	.format(printStr[0], sourceRepo["html_url"]), printStr[1])

	"""Get list of forked repos that are alive and newer than the source repo
	"""
	aliveRepos, forkedRepos = githubREST.getListOfAliveForks(repo, death)

	printf.logPrint("{} out of {} Forked repos are alive and newer than the source!"
	.format(len(aliveRepos), len(forkedRepos)), LogType.BOLD)
	for aliveRepo in aliveRepos:
		githubREST.printRepo(aliveRepo)


username, death = getUsernameAndLifespan()


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
