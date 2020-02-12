#!/usr/bin/env python3
import sys
import os
from pathlib import Path
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR) + "/lib")

import githubREST
import utils

_username, death = utils.getUsernameAndLifespan()
repoName = input("Enter the user and repo name in the form (user/repo - eg. fredhappyface/python.imageround)\n>")


"""Is source repo alive?
"""
sourceRepo = githubREST.getRepo(repoName)
if githubREST.sourceAlive(sourceRepo, death):
	utils.logPrint("Source repo is alive! Head to {}" .format(sourceRepo["html_url"]), "success")

"""Get list of forked repos that are alive and newer than the source repo
"""
aliveRepos, forkedRepos = githubREST.getListOfAliveForks(sourceRepo, death)

utils.logPrint("{} out of {} Forked repos are alive and newer than the source!"
.format(len(aliveRepos), len(forkedRepos)), "bold")
for aliveRepo in aliveRepos:
	githubREST.printRepo(aliveRepo)
