#!/usr/bin/env python3
import gitrepo
import json

def forEachRepo(sourceRepo):
	"""Is source repo alive?
	"""
	printStr = ["dead", "error"]
	if gitrepo.sourceAlive(sourceRepo, death):
		printStr = ["alive", "success"]
	gitrepo.logPrint("Source repo is {}! Head to {}"
	.format(printStr[0], sourceRepo["html_url"]), printStr[1])

	"""Get list of forked repos that are alive and newer than the source repo
	"""
	aliveRepos, forkedRepos = gitrepo.getListOfAliveForks(repo, death)

	gitrepo.logPrint("{} out of {} Forked repos are alive and newer than the source!"
	.format(len(aliveRepos), len(forkedRepos)), "bold")
	for aliveRepo in aliveRepos:
		gitrepo.logPrint("Name: {}\n- Latest update: {}\n- Link: {}\n- Stars: {}"
		.format(aliveRepo["full_name"], aliveRepo["pushed_at"], aliveRepo["html_url"],
		aliveRepo["stargazers_count"]))


username, death = gitrepo.getUsernameAndLifespan()


choice = input("User repos, watched or starred (R/w/s)>")
if choice.lower() == "s":
	"""Get list of user starred
	"""
	starredRepos = gitrepo.getListOfUserRepos(username, "starred")
	for repo in starredRepos:
		forEachRepo(repo)

elif choice.lower() == "w":
	"""Get list of user watched
	"""
	watchedRepos = gitrepo.getListOfUserRepos(username, "subscriptions")
	for repo in watchedRepos:
		forEachRepo(repo)

else:
	"""Get list of user repos
	"""
	sourceRepos = gitrepo.getListOfUserRepos(username, "repos")
	for repo in sourceRepos:
		forEachRepo(repo)
