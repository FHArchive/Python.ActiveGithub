"""Quickly identify repos that are active and inactive from a user's personal
repos, starred and watching.
"""

from __future__ import annotations

from typing import Any

from lib import github_graph
from lib.metprint import LogType
from lib.utils import getUsernameAndLifespan, printf


def forEachRepo(sourceRepo: dict[str, Any]) -> None:
	"""Is source repo alive?."""
	printStr = ["dead", LogType.ERROR]
	if github_graph.sourceAlive(sourceRepo, death):
		printStr = ["alive", LogType.SUCCESS]
	printf.logPrint(f"Source repo is {printStr[0]}! Head to {sourceRepo['url']}", printStr[1])

	"""Get list of forked repos that are alive and newer than the source repo.
	"""
	aliveRepos, forkedRepos = github_graph.getListOfAliveForks(repo, death)

	printf.logPrint(
		f"{len(aliveRepos)} out of {len(forkedRepos)} Forked repos are "
		"alive and newer than the source!",
		LogType.BOLD,
	)
	for aliveRepo in aliveRepos:
		github_graph.printRepo(aliveRepo)


username, death = getUsernameAndLifespan()

choice = input("User repos, watched or starred (R/w/s)>")
if choice.lower() == "s":
	"""Get list of user starred."""
	starredRepos = github_graph.getListOfRepos(username, "starredRepositories")
	for repo in starredRepos:
		forEachRepo(repo)

elif choice.lower() == "w":
	"""Get list of user watched."""
	watchedRepos = github_graph.getListOfRepos(username, "watching")
	for repo in watchedRepos:
		forEachRepo(repo)

else:
	"""Get list of user repos."""
	sourceRepos = github_graph.getListOfRepos(username, "repositories")
	for repo in sourceRepos:
		forEachRepo(repo)
