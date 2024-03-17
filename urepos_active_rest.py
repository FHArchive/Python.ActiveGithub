#!/usr/bin/env python3
"""Quickly identify repos that are active and inactive from a user's personal...

repos, starred and watching

Note that this is the REST version and is less optimised than the Graph version
This has been kept so a comparison can be made
"""

from __future__ import annotations

from typing import Any

from metprint import LogType

from lib import github_rest
from lib.utils import getUsernameAndLifespan, printf


def forEachRepo(sourceRepo: dict[Any, Any]) -> None:
	"""Is source repo alive?."""
	printStr = ["dead", LogType.ERROR]
	if github_rest.sourceAlive(sourceRepo, death):
		printStr = ["alive", LogType.SUCCESS]
	printf.logPrint(f"Source repo is {printStr[0]}! Head to {sourceRepo['html_url']}", printStr[1])
	"""Get list of forked repos that are alive and newer than the source repo
	"""
	aliveRepos, forkedRepos = github_rest.getListOfAliveForks(repo, death)

	printf.logPrint(
		f"{len(aliveRepos)} out of {len(forkedRepos)} Forked repos are alive and newer than the source!",
		LogType.BOLD,
	)
	for aliveRepo in aliveRepos:
		github_rest.printRepo(aliveRepo)


username, death = getUsernameAndLifespan()

choice = input("User repos, watched or starred (R/w/s)>")
if choice.lower() == "s":
	"""Get list of user starred"""
	starredRepos = github_rest.getListOfUserRepos(username, "starred")
	for repo in starredRepos:
		forEachRepo(repo)

elif choice.lower() == "w":
	"""Get list of user watched"""
	watchedRepos = github_rest.getListOfUserRepos(username, "subscriptions")
	for repo in watchedRepos:
		forEachRepo(repo)

else:
	"""Get list of user repos"""
	sourceRepos = github_rest.getListOfUserRepos(username, "repos")
	for repo in sourceRepos:
		forEachRepo(repo)
