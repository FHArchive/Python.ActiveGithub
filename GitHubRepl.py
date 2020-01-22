#!/usr/bin/env python3
import sys
import gitrepo
import os
import mdv

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')


def printMarkdown(raw, maxpages=0):
	md = mdv.main(raw, c_theme="995.1179").split("\n")
	paginatedList(md, 30, print, maxpages)



def listRepos(data, user):
	userRepos = gitrepo.getListOfUserRepos(user, data)
	paginatedList(userRepos, 8, gitrepo.printRepo)



def paginatedList(iterable, perPage, printFunc, maxpages=0):
	totalPages = len(iterable) // perPage + 1
	for index, iteration in enumerate(iterable):
		page = index // perPage
		if maxpages != 0 and page >= maxpages:
			return
		if index > 0 and index % perPage == 0:
			input("Page {} of {} (Next)>" .format(index // perPage, totalPages))
		printFunc(iteration)



"""REPL functions
"""
def replhelp():
	clear()

	gitrepo.logPrint("Most of the time the 'user' arg can be omitted", "info")
	gitrepo.logPrint("Functions: ", "bold")
	for function in functions.keys():
		gitrepo.logPrint("- {} : {}" .format(function,
		list(functions[function].__code__.co_varnames[:functions[function].__code__.co_argcount])))

def replexit():
	sys.exit(0)

def repos(user=None):
	user = username if user is None else user
	listRepos("repos", user)

def stars(user=None):
	user = username if user is None else user
	listRepos("stargazing", user)

def watchng(user=None):
	user = username if user is None else user
	listRepos("subscriptions", user)

def profile(user=None):
	user = username if user is None else user
	clear()
	user = gitrepo.getUser(user)
	gitrepo.logPrint("{}".format(user["name"]), "bold")
	gitrepo.logPrint("{}\nAvatar: {} \nCompany: {} \nLocation: {} \nEmail: {} \nFollowers: {} Following: {}"
	.format(user["login"], user["avatar_url"],	user["company"], user["location"],
	user["email"], user["followers"], user["following"]))


def gists(user=None):
	user = username if user is None else user
	userGists = gitrepo.getUserGists(user)
	paginatedList(userGists, 30, gitrepo.printGist)

def showrepo(repo, user=None):
	clear()
	user = username if user is None else user
	rawMarkdown = gitrepo.getReadme(user+"/"+repo)
	repoText = gitrepo.getRepo(user+"/"+repo)
	gitrepo.printRepo(repoText)
	gitrepo.logPrint("README", "bold")
	printMarkdown(rawMarkdown, 1)

def showreadme(repo, user=None):
	clear()
	user = username if user is None else user
	printMarkdown(gitrepo.getReadme(user+"/"+repo))


def searchissues(searchTerm):
	issues = gitrepo.search(searchTerm, context="issues")
	paginatedList(issues, 30, gitrepo.printIssue)


def searchrepos(searchTerm):
	searchRepos = gitrepo.search(searchTerm, context="repositories")
	paginatedList(searchRepos, 10, gitrepo.printRepo)


def searchusers(searchTerm):
	users = gitrepo.search(searchTerm, context="users")
	paginatedList(users, 30, gitrepo.printUser)


functions = {"exit": replexit, "help": replhelp, "repos": repos, "stars": stars,
"watchng": watchng, "profile": profile, "showrepo": showrepo,
"showreadme": showreadme, "searchissues": searchissues, "searchrepos": searchrepos,
"searchusers": searchusers, "gists": gists}
def repl():
	while True:
		command = input(">")
		try:
			func, *params = command.split()
			functions[func.lower()](*params)
		except TypeError as error:
			gitrepo.logPrint(str(error), "error")
		except KeyError as error:
			gitrepo.logPrint(str(error) + " is not a function", "error")
		except ValueError:
			pass

username = gitrepo.getUsername()
replhelp()
repl()
