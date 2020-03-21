#!/usr/bin/env python3
"""Use this program to get a list of forked repos that are active
"""
import sys
import os
from pathlib import Path
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR) + "/lib")

import githubGraph
import utils

_username, death = utils.getUsernameAndLifespan()
author, repoName = input(
	"Enter the user and repo name in the form (user/repo - eg. fredhappyface/python.imageround)\n>"
	).split("/")


"""Is source repo alive?
"""
sourceRepo = githubGraph.getRepo(author, repoName)
if githubGraph.sourceAlive(sourceRepo, death):
	utils.logPrint("Source repo is alive! Head to {}" .format(sourceRepo["url"]), "success")

"""Get list of forked repos that are alive and newer than the source repo
"""
aliveRepos, forkedRepos = githubGraph.getListOfAliveForks(sourceRepo, death)

utils.logPrint("{} out of {} Forked repos are alive and newer than the source!"
.format(len(aliveRepos), len(forkedRepos)), "bold")
for aliveRepo in aliveRepos:
	githubGraph.printRepo(aliveRepo)
