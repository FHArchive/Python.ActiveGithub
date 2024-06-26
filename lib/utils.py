"""Adds functions used by both github_graph and github_rest."""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path

from lib.metprint import FHFormatter, Logger, LogType

printf = Logger(FHFormatter())


def clear() -> None:
	"""Clear the terminal."""
	os.system("cls" if os.name == "nt" else "clear")


def getDatetime(datetimeIn: str) -> datetime.datetime:
	"""Get the datetime from a date in the format YYYY-MM-DDThh:mm:ssZ e.g. 2000-01-01T00:00:00Z."""
	return datetime.datetime.strptime(datetimeIn, "%Y-%m-%dT%H:%M:%S%z")


def getUsername() -> str:
	"""Get authenticated username."""
	return AUTH[0]


def getPassword() -> str:
	"""Get authenticated password."""
	return AUTH[1]


def getUsernameAndLifespan() -> tuple[str, int]:
	"""Return the username from env.json and lifespan from user input."""
	username = getUsername()
	lifespan = 36
	try:
		lifespan = int(input("Set the repo lifespan (weeks - eg. 1 - default=36)\n>"))
	except ValueError:
		printf.logPrint("Invalid input - using default", LogType.WARNING)
	return username, lifespan


if "AUTH" not in locals():
	try:
		authJson = json.loads(Path("env.json").read_text(encoding="utf-8"))
		AUTH = (authJson["username"], authJson["password"])
		printf.logPrint(f"Authenticated user {authJson['username']}", LogType.SUCCESS)
	except FileNotFoundError:
		printf.logPrint(
			"Not authenticated - Do you want to log in? (just hit enter if not)",
			LogType.WARNING,
		)
		AUTH = (input("Enter your username\n>"), input("Enter your password\n>"))
		if len(AUTH[0]) == 0 or len(AUTH[1]) == 0:
			printf.logPrint(
				"Not authenticated - rate limit is 60 requests per hour",
				LogType.WARNING,
			)
