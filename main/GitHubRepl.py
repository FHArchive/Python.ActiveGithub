#!/usr/bin/env python3
"""Use this program to interact with your repos (note that there are better
solutions out there)
"""
import sys
import os
from pathlib import Path
THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, os.path.dirname(THISDIR) + "/lib")

from metprint import LogType
#pylint: disable=import-error
import githubREST
import utils
#pylint: enable=import-error

def clear():
	'''Clear the terminal '''
	os.system('cls' if os.name == 'nt' else 'clear')


def printMarkdown(raw, maxpages=0):
	'''Pretty print markdown '''
	try:
		from catpandoc import pandoc2ansi, processpandoc
		import pypandoc
		import json
		output = json.loads(pypandoc.convert_text(raw, 'json', 'md'))
		pandoc = pandoc2ansi.Pandoc2Ansi(80, 0, (4, 0, 0))
		md = ""
		for block in output["blocks"]:
			processpandoc.processBlock(block, pandoc)
		md = pandoc.genOutput()
	except ModuleNotFoundError:
		md = raw
	paginatedList(md.split("\n"), 30, print, maxpages)



def listRepos(data, user):
	'''List the user repos '''
	userRepos = githubREST.getListOfUserRepos(user, data)
	paginatedList(userRepos, 8, githubREST.printRepo)



def paginatedList(iterable, perPage, printFunc, maxpages=0):
	'''Print a paginated list '''
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
	'''Return help text for the REPL '''
	clear()
	utils.printf.logPrint("Most of the time the 'user' arg can be omitted", LogType.INFO)
	utils.printf.logPrint("Functions: ", LogType.BOLD)
	for function in functions:
		utils.printf.logPrint("- {} : {}" .format(function,
		list(functions[function].__code__.co_varnames[:functions[function].__code__.co_argcount])))

def replexit():
	'''Exit the REPL '''
	sys.exit(0)

def repos(user=None):
	'''List repos '''
	user = username if user is None else user
	listRepos("repos", user)

def stars(user=None):
	'''List repos the user has starred '''
	user = username if user is None else user
	listRepos("stargazing", user)

def watching(user=None):
	'''List repos the user is watching '''
	user = username if user is None else user
	listRepos("subscriptions", user)

def profile(user=None):
	'''Print user profile info '''
	user = username if user is None else user
	clear()
	user = githubREST.getUser(user)
	utils.printf.logPrint("{}".format(user["name"]), LogType.BOLD)
	utils.printf.logPrint("{}\nAvatar: {} \nCompany: {} \nLocation: {} \nEmail: {} \nFollowers: {} Following: {}"
	.format(user["login"], user["avatar_url"],	user["company"], user["location"],
	user["email"], user["followers"], user["following"]))


def gists(user=None):
	'''Print paginated list of user gists '''
	user = username if user is None else user
	userGists = githubREST.getUserGists(user)
	paginatedList(userGists, 30, githubREST.printGist)

def showrepo(repo, user=None):
	'''Print user repo data for a given repo '''
	clear()
	user = username if user is None else user
	rawMarkdown = githubREST.getReadme(user+"/"+repo)
	repoText = githubREST.getRepo(user+"/"+repo)
	githubREST.printRepo(repoText)
	utils.printf.logPrint("README", LogType.BOLD)
	printMarkdown(rawMarkdown, 1)

def showreadme(repo, user=None):
	'''Print the readme for a given repo '''
	clear()
	user = username if user is None else user
	printMarkdown(githubREST.getReadme(user+"/"+repo))


def searchissues(searchTerm):
	'''Search function for issues '''
	issues = githubREST.search(searchTerm, context="issues")
	paginatedList(issues, 30, githubREST.printIssue)


def searchrepos(searchTerm):
	'''Search function for repos '''
	searchRepos = githubREST.search(searchTerm, context="repositories")
	paginatedList(searchRepos, 10, githubREST.printRepo)


def searchusers(searchTerm):
	'''Search function for users '''
	users = githubREST.search(searchTerm, context="users")
	paginatedList(users, 30, githubREST.printUser)


functions = {"exit": replexit, "help": replhelp, "repos": repos, "stars": stars,
"watching": watching, "profile": profile, "showrepo": showrepo,
"showreadme": showreadme, "searchissues": searchissues, "searchrepos": searchrepos,
"searchusers": searchusers, "gists": gists}
def repl():
	'''Read Eval Print Loop '''
	while True:
		command = input(">")
		try:
			func, *params = command.split()
			functions[func.lower()](*params)
		except TypeError as error:
			utils.printf.logPrint(str(error), "error")
		except KeyError as error:
			utils.printf.logPrint(str(error) + " is not a function", "error")
		except ValueError:
			pass

username = utils.getUsername()
replhelp()
repl()
