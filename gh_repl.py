#!/usr/bin/env python3
"""Use this program to interact with your repos (note that there are better
solutions out there)
"""
from __future__ import annotations

import json
import sys
from typing import Any, Callable

from metprint import LogType

from lib import github_rest, utils

# pylint:disable=import-outside-toplevel


def printMarkdown(raw: str, maxpages: int = 0):
	"""Pretty print markdown."""
	try:
		import pypandoc
		from catpandoc import pandoc2ansi, processpandoc

		output = json.loads(pypandoc.convert_text(raw, "json", "md"))
		pandoc = pandoc2ansi.Pandoc2Ansi(80, 0, (4, 0, 0))
		markdown = ""
		for block in output["blocks"]:
			processpandoc.processBlock(block, pandoc)
		markdown = pandoc.genOutput()
	except ModuleNotFoundError:
		markdown = raw
	paginatedList(markdown.split("\n"), 30, print, maxpages)


def listRepos(data: str, user: str):
	"""List the user repos."""
	userRepos = github_rest.getListOfUserRepos(user, data)
	paginatedList(userRepos, 8, github_rest.printRepo)


def paginatedList(
	iterable: list[Any],
	perPage: int,
	printFunc: Callable[[dict[Any, Any]], None],
	maxpages: int = 0,
):
	"""Print a paginated list."""
	totalPages = len(iterable) // perPage + 1
	for index, iteration in enumerate(iterable):
		page = index // perPage
		if maxpages != 0 and page >= maxpages:
			return
		if index > 0 and index % perPage == 0:
			input(f"Page {index // perPage} of {totalPages} (Next)>")
		printFunc(iteration)


"""REPL functions
"""


def replhelp():
	"""Return help text for the REPL."""
	utils.clear()
	utils.printf.logPrint("Most of the time the 'user' arg can be omitted", LogType.INFO)
	utils.printf.logPrint("Functions: ", LogType.BOLD)
	for name, function in functions.items():
		params = list(function.__code__.co_varnames[: function.__code__.co_argcount])
		utils.printf.logPrint(f"- {name} : {params}")


def replexit():
	"""Exit the REPL."""
	sys.exit(0)


def repos(user: str | None = None):
	"""List repos."""
	user = user if user is not None else username
	listRepos("repos", user)


def stars(user: str | None = None):
	"""List repos the user has starred."""
	user = username if user is None else user
	listRepos("stargazing", user)


def watching(user: str | None = None):
	"""List repos the user is watching."""
	user = username if user is None else user
	listRepos("subscriptions", user)


def profile(user: str | None = None):
	"""Print user profile info."""
	user = username if user is None else user
	utils.clear()
	userData = github_rest.getUser(user)
	utils.printf.logPrint(f"{userData['name']}", LogType.BOLD)
	utils.printf.logPrint(
		f"""{userData['login']}
Avatar: {userData['avatar_url']}
Company: {userData['company']}
Location: {userData['location']}
Email: {userData['email']}
Followers: {userData['followers']} Following: {userData['following']}"""
	)


def gists(user: str | None = None):
	"""Print paginated list of user gists."""
	user = username if user is None else user
	userGists = github_rest.getUserGists(user)
	paginatedList(userGists, 30, github_rest.printGist)


def showrepo(repo: str, user: str | None = None):
	"""Print user repo data for a given repo."""
	utils.clear()
	user = username if user is None else user
	rawMarkdown = github_rest.getReadme(user + "/" + repo)
	repoText = github_rest.getRepo(user + "/" + repo)
	github_rest.printRepo(repoText)
	utils.printf.logPrint("README", LogType.BOLD)
	printMarkdown(rawMarkdown, 1)


def showreadme(repo: str, user: str | None = None):
	"""Print the readme for a given repo."""
	utils.clear()
	user = username if user is None else user
	printMarkdown(github_rest.getReadme(user + "/" + repo))


def searchissues(searchTerm: str):
	"""Search function for issues."""
	issues = github_rest.search(searchTerm, context="issues")
	paginatedList(issues, 30, github_rest.printIssue)


def searchrepos(searchTerm: str):
	"""Search function for repos."""
	searchRepos = github_rest.search(searchTerm, context="repositories")
	paginatedList(searchRepos, 10, github_rest.printRepo)


def searchusers(searchTerm: str):
	"""Search function for users."""
	users = github_rest.search(searchTerm, context="users")
	paginatedList(users, 30, github_rest.printUser)


functions = {
	"exit": replexit,
	"help": replhelp,
	"repos": repos,
	"stars": stars,
	"watching": watching,
	"profile": profile,
	"showrepo": showrepo,
	"showreadme": showreadme,
	"searchissues": searchissues,
	"searchrepos": searchrepos,
	"searchusers": searchusers,
	"gists": gists,
}


def repl():
	"""Read Eval Print Loop."""
	while True:
		command = input(">")
		try:
			func, *params = command.split()
			functions[func.lower()](*params)
		except TypeError as error:
			utils.printf.logPrint(str(error), LogType.ERROR)
		except KeyError as error:
			utils.printf.logPrint(str(error) + " is not a function", LogType.ERROR)
		except ValueError:
			pass


username = utils.getUsername()
replhelp()
repl()
