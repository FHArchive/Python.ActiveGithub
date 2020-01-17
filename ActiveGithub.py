#!/usr/bin/env python3
import gitrepo

_username, death = gitrepo.getUsernameAndLifespan()
repo = input("Enter the user and repo name in the form (user/repo - eg. fredhappyface/python.imageround)>")


"""Is source repo alive?
"""
sourceRepo, _ = gitrepo.sourceData(repo)
if gitrepo.sourceAlive(repo, death):
	gitrepo.logPrint("Source repo is alive! Head to {}" .format(sourceRepo["html_url"]), "success")

"""Get list of forked repos that are alive and newer than the source repo
"""
aliveRepos, forkedRepos = gitrepo.getListOfAliveForks(repo, death)

gitrepo.logPrint("{} out of {} Forked repos are alive and newer than the source!" .format(len(aliveRepos), len(forkedRepos)), "bold")
for aliveRepo in aliveRepos:
	gitrepo.logPrint("Name: {}\n- Latest update: {}\n- Link: {}\n- Stars: {}"
	.format(aliveRepo["full_name"], aliveRepo["pushed_at"], aliveRepo["html_url"],
	aliveRepo["stargazers_count"]))
