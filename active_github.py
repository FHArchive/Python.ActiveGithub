#!/usr/bin/env python3
"""Use this program to get a list of forked repos that are active."""

from metprint import LogType

from lib import github_graph
from lib.utils import getUsernameAndLifespan, printf

_username, death = getUsernameAndLifespan()
author, repoName = input(
	"Enter the user and repo name in the form (user/repo - eg. fredhappyface/python.activegithub)\n>"
).split("/")
"""Is source repo alive?
"""
sourceRepo = github_graph.getRepo(author, repoName)
if github_graph.sourceAlive(sourceRepo, death):
	printf.logPrint(f"Source repo is alive! Head to {sourceRepo['url']}", LogType.SUCCESS)
"""Get list of forked repos that are alive and newer than the source repo
"""
aliveRepos, forkedRepos = github_graph.getListOfAliveForks(sourceRepo, death)

printf.logPrint(
	f"{len(aliveRepos)} out of {len(forkedRepos)} Forked repos are alive and newer than the source!",
	LogType.BOLD,
)
for aliveRepo in aliveRepos:
	github_graph.printRepo(aliveRepo)
