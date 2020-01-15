#!/usr/bin/env python3
import requests
import datetime
import sys

def logPrint(printText, printType="standard"):
	types = {"standard": "{}", "success": "[\033[92m+ Success\033[00m] {}",
	"warning": "[\033[93m/ Warning\033[00m] {}", "error": "[\033[91m- Error\033[00m] {}",
	"info": "[\033[96m* Info\033[00m] {}", "bold": "\033[01m{}\033[00m"}
	print(types[printType.lower()] .format(printText))

death = 36
try:
	death = int(input("Set time considered to be dead (weeks - eg. 1 - default=36)>"))
except:
	logPrint("Invalid input - using default", "warning")
repo = input("Enter the user and repo name in the form (user/repo - eg. fredhappyface/python.imageround)>")

sourceRepo = requests.get(url="https://api.github.com/repos/"+repo).json()

if "message" in sourceRepo:
	logPrint("Some error has occurred", "error")
	logPrint(sourceRepo)
	sys.exit(1)

sourceRepoPushedAt = sourceRepo["pushed_at"]

forkedRepos = requests.get(
	url="https://api.github.com/repos/"+repo+"/forks?sort=stargazers&per_page=100").json()

if datetime.datetime.strptime(sourceRepoPushedAt, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(
	weeks=death) > datetime.datetime.now():
	logPrint("Source repo is alive! Head to {}\n" .format(sourceRepo["html_url"]), "success")


aliveRepos = []
for forkedRepo in forkedRepos:
	forkedRepoPushedAt = forkedRepo["pushed_at"]
	if datetime.datetime.strptime(forkedRepoPushedAt, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(
		weeks=death) > datetime.datetime.now():
		aliveRepos.append(forkedRepo)


logPrint("{} out of {} Forked repos are alive!" .format(len(aliveRepos), len(forkedRepos)), "bold")
for aliveRepo in aliveRepos:
	logPrint("Name: {}\n- Latest update: {}\n- Link: {}\n- Stars: {}"
	.format(aliveRepo["full_name"], aliveRepo["pushed_at"], aliveRepo["html_url"],
	aliveRepo["stargazers_count"]))
