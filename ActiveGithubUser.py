#!/usr/bin/env python3
import gitrepo
import json

def forEachRepo(sourceRepo):
	"""Is source repo alive?
	"""
	repo = sourceRepo["full_name"]
	printStr = ["dead", "error"]
	if gitrepo.sourceAlive(repo, death):
		printStr = ["alive", "success"]
	gitrepo.logPrint("Source repo is {}! Head to {}" .format(printStr[0], sourceRepo["html_url"]), printStr[1])

	"""Get list of forked repos that are alive and newer than the source repo
	"""
	aliveRepos, forkedRepos = gitrepo.forksAliveAndNewer(repo, death)

	gitrepo.logPrint("{} out of {} Forked repos are alive and newer than the source!" .format(len(aliveRepos), len(forkedRepos)), "bold")
	for aliveRepo in aliveRepos:
		gitrepo.logPrint("Name: {}\n- Latest update: {}\n- Link: {}\n- Stars: {}"
		.format(aliveRepo["full_name"], aliveRepo["pushed_at"], aliveRepo["html_url"],
		aliveRepo["stargazers_count"]))


USERNAME = None
try:
	authJson = json.loads(open("env.json", "r").read())
	USERNAME = authJson["username"]
	gitrepo.logPrint("Hello {}!" .format(USERNAME), "success")
except:
	USERNAME = input("Enter your username>")

death = 36
try:
	death = int(input("Set time considered to be dead (weeks - eg. 1 - default=36)>"))
except:
	gitrepo.logPrint("Invalid input - using default", "warning")


choice = input("User repos or watched (R/w)>")

if choice.lower() == "w":
	"""Get list of user watched
	"""
	starredRepos = []
	hasRepos = True
	page = 1
	while hasRepos:
		repos = gitrepo.getGithubApiRequest("users/"+USERNAME+"/subscriptions?per_page=100&page="+str(page))
		if len(repos) < 1:
			hasRepos = False
		starredRepos.extend(repos)
		page += 1
	for repo in starredRepos:
		forEachRepo(repo)

else:
	"""Get list of user repos
	"""
	pages = gitrepo.getGithubApiRequest("users/"+USERNAME)["public_repos"] % 100 + 1
	sourceRepos = []
	for page in range(1, pages+1):
		sourceRepos.extend(gitrepo.getGithubApiRequest("users/"+USERNAME+"/repos?per_page=100&page="+str(page)))
	for repo in sourceRepos:
		forEachRepo(repo)
