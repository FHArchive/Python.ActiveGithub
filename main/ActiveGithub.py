#!/usr/bin/env python3
"""Use this program to get a list of forked repos that are active
"""
import sys
import os
from pathlib import Path
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR) + "/lib")

from metprint import LogType
import githubGraph
from utils import printf, getUsernameAndLifespan

_username, death = getUsernameAndLifespan()
author, repoName = input(
	"Enter the user and repo name in the form (user/repo - eg. fredhappyface/python.activegithub)\n>"
	).split("/")


"""Is source repo alive?
"""
sourceRepo = githubGraph.getRepo(author, repoName)
if githubGraph.sourceAlive(sourceRepo, death):
	printf.logPrint("Source repo is alive! Head to {}" .format(sourceRepo["url"]), LogType.SUCCESS)

"""Get list of forked repos that are alive and newer than the source repo
"""
aliveRepos, forkedRepos = githubGraph.getListOfAliveForks(sourceRepo, death)

printf.logPrint("{} out of {} Forked repos are alive and newer than the source!"
.format(len(aliveRepos), len(forkedRepos)), LogType.BOLD)
for aliveRepo in aliveRepos:
	githubGraph.printRepo(aliveRepo)
