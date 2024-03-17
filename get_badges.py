#!/usr/bin/env python3
"""Generate badges for repos under an user/org - here we're going to do it for python/ pypi
but this can be easily adapted.
"""

from __future__ import annotations

import argparse
import functools
import operator
import re
from typing import Any

import requests

from lib import github_graph
from lib.utils import getUsername, printf

parser = argparse.ArgumentParser("Generate badges for repos under an user/org")
parser.add_argument(
	"-o",
	"--orgs",
	action="append",
	nargs="+",
	help="add an org to get traffic for",
)
parser.add_argument(
	"-u",
	"--user",
	action="store_true",
	help="return the list of user owned repos?",
)
args = parser.parse_args()
username = getUsername()

if args.orgs is None or args.user is None:
	printf.logPrint("Pass at least 1 org or 1 user see --help for more info")

sourceRepos = []
for organization in functools.reduce(operator.iadd, args.orgs, []):
	sourceRepos += github_graph.getListOfRepos(organization, organization=True)
if args.user:
	sourceRepos += github_graph.getListOfRepos(username)

sortRepos = []
for repoData in sourceRepos:
	repositoryName = repoData["name"]

	sortRepos.append(
		(
			("(Archived) " if repoData["isArchived"] else "") + repositoryName,
			repoData["owner"]["login"],
			repositoryName,
		)
	)


def getKey(item: list[Any]):
	"""Return the key."""
	return item[0]


sortedRepos = sorted(sortRepos, key=getKey, reverse=True)

for repoData in sortedRepos:
	badge = f"https://img.shields.io/pypi/dm/{repoData[2].lower()}.svg?style=for-the-badge"
	ret = requests.get(badge)
	downRank = "UNKNOWN"
	try:
		downloads = int(
			re.findall(b"<title>(.*?)</title>", ret.content)[0]
			.lower()
			.replace(b"downloads: ", b"")
			.replace(b"/month", b"")
		)
		downRank = "LOW" if downloads < 65 else "HIGH"
	except ValueError:
		pass
