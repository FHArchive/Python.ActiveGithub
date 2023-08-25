"""Print in fancy ways
"""
# pylint: disable=too-few-public-methods
from __future__ import annotations

import builtins
from enum import Enum


class LogType(Enum):
	"""Contains logtypes for this module

	NONE
	No special formatting

	BOLD
	Bold text

	ITALIC
	Italic text

	HEADER
	Some form of heading

	DEBUG
	Detailed information, typically of interest only when diagnosing problems.

	INFO
	Confirmation that things are working as expected.

	WARNING
	An indication that something unexpected happened, or indicative of some
	problem in the near future (e.g. ‘disk space low’). The software is still
	working as expected.

	ERROR
	Due to a more serious problem, the software has not been able to perform
	some function.

	CRITICAL
	A serious error, indicating that the program itself may be unable to
	continue running.

	INDENT
	Stores the indent for NONE, BOLD, ITALIC, HEADER

	"""

	NONE = 0
	BOLD = 1
	ITALIC = 2
	HEADER = 3
	DEBUG = 4
	INFO = 5
	SUCCESS = 6
	WARNING = 7
	ERROR = 8
	CRITICAL = 9
	INDENT = 10


class Formatter:
	"""Format text in meterpreter style"""

	def __init__(self):
		self.format = {}


class MeterpreterFormatter(Formatter):
	"""Format text in meterpreter style"""

	def __init__(self):
		Formatter.__init__(self)
		self.format = {
			LogType.NONE: "{}",
			LogType.BOLD: "\033[01m{}\033[00m",
			LogType.ITALIC: "\033[03m{}\033[00m",
			LogType.HEADER: "\033[01m\033[04m{}\033[00m",
			LogType.DEBUG: "\033[01m\033[96m[$]\033[00m {}",
			LogType.INFO: "\033[01m\033[36m[*]\033[00m {}",
			LogType.SUCCESS: "\033[01m\033[32m[+]\033[00m {}",
			LogType.WARNING: "\033[01m\033[33m[/]\033[00m {}",
			LogType.ERROR: "\033[01m\033[31m[-]\033[00m {}",
			LogType.CRITICAL: "\033[01m\033[91m[!]\033[00m {}",
			LogType.INDENT: 4,
		}


class FHFormatter(Formatter):
	"""Format text in my own style"""

	def __init__(self):
		Formatter.__init__(self)
		self.format = {
			LogType.NONE: "{}",
			LogType.BOLD: "\033[01m{}\033[00m",
			LogType.ITALIC: "\033[03m{}\033[00m",
			LogType.HEADER: "\033[01m\033[04m{}\033[00m",
			LogType.DEBUG: "[\033[01m\033[96m$  Deb\033[00m] {}",
			LogType.INFO: "[\033[36m* Info\033[00m] {}",
			LogType.SUCCESS: "[\033[32m+   Ok\033[00m] {}",
			LogType.WARNING: "[\033[33m/ Warn\033[00m] {}",
			LogType.ERROR: "[\033[31m-  Err\033[00m] {}",
			LogType.CRITICAL: "[\033[01m\033[91m! Crit\033[00m] {}",
			LogType.INDENT: 9,
		}


class FHNFFormatter(Formatter):
	"""Format text in my own style with nerd fonts"""

	def __init__(self):
		Formatter.__init__(self)
		self.format = {
			LogType.NONE: "{}",
			LogType.BOLD: "\033[01m{}\033[00m",
			LogType.ITALIC: "\033[03m{}\033[00m",
			LogType.HEADER: "\033[01m\033[04m{}\033[00m",
			LogType.DEBUG: "[\033[01m\033[96m\uf46f  Deb\033[00m] {}",
			LogType.INFO: "[\033[36m\uf449 Info\033[00m] {}",
			LogType.SUCCESS: "[\033[32m\uf42e   Ok\033[00m] {}",
			LogType.WARNING: "[\033[33m\uf467 Warn\033[00m] {}",
			LogType.ERROR: "[\033[31m\uf46e  Err\033[00m] {}",
			LogType.CRITICAL: "[\033[01m\033[91m\uf421 Crit\033[00m] {}",
			LogType.INDENT: 9,
		}


class PythonFormatter(Formatter):
	"""Format text in my python logger style"""

	def __init__(self):
		Formatter.__init__(self)
		self.format = {
			LogType.NONE: "{}",
			LogType.BOLD: "{}",
			LogType.ITALIC: "{}",
			LogType.HEADER: "HEADER:{}",
			LogType.DEBUG: "DEBUG:{}",
			LogType.INFO: "INFO:{}",
			LogType.SUCCESS: "SUCCESS:{}",
			LogType.WARNING: "WARNING:{}",
			LogType.ERROR: "ERROR:{}",
			LogType.CRITICAL: "CRITICAL:{}",
			LogType.INDENT: 4,
		}


class ColorLogFormatter(Formatter):
	"""Format text in colorlog style
	https://github.com/borntyping/python-colorlog
	"""

	def __init__(self):
		Formatter.__init__(self)
		self.format = {
			LogType.NONE: "{}",
			LogType.BOLD: "\033[01m{}\033[00m",
			LogType.ITALIC: "\033[03m{}\033[00m",
			LogType.HEADER: "\033[01m\033[04m{}\033[00m",
			LogType.DEBUG: "\033[36mDEBUG    \033[00m\033[34m{}\033[00m",
			LogType.INFO: "\033[32mINFO     \033[00m\033[34m{}\033[00m",
			LogType.SUCCESS: "\033[32mSUCCESS  \033[00m\033[34m{}\033[00m",
			LogType.WARNING: "\033[33mWARNING  \033[00m\033[34m{}\033[00m",
			LogType.ERROR: "\033[31mERROR    \033[00m\033[34m{}\033[00m",
			LogType.CRITICAL: "\033[31mCRITICAL \033[00m\033[34m{}\033[00m",
			LogType.INDENT: 9,
		}


class PrintTagsFormatter(Formatter):
	"""Format text in PrintTag style
	https://github.com/mdlockyer/PrintTags
	Note that this project provides other functionality that this one lacks
	"""

	def __init__(self):
		Formatter.__init__(self)
		self.format = {
			LogType.NONE: "{}",
			LogType.BOLD: "\033[01m{}\033[00m",
			LogType.ITALIC: "\033[03m{}\033[00m",
			LogType.HEADER: "\033[01m\033[04m{}\033[00m",
			LogType.DEBUG: "\033[36m[debug] {}\033[00m",
			LogType.INFO: "\033[36m[info] {}\033[00m",
			LogType.SUCCESS: "\033[32m[success] {}\033[00m",
			LogType.WARNING: "\033[35m[warn] {}\033[00m",
			LogType.ERROR: "\033[31m[error] {}\033[00m",
			LogType.CRITICAL: "\033[31m[critical] {}\033[00m",
			LogType.INDENT: 4,
		}


class XaFormatter(Formatter):
	"""Format text in Xa style
	https://github.com/xxczaki/xa
	"""

	def __init__(self):
		Formatter.__init__(self)
		self.format = {
			LogType.NONE: "{}",
			LogType.BOLD: "\033[01m{}\033[00m",
			LogType.ITALIC: "\033[03m{}\033[00m",
			LogType.HEADER: "\033[01m\033[40m\033[93m TITLE \033[00m {}",
			LogType.DEBUG: "\033[01m\033[106m\033[30m DEBUG \033[00m {}",
			LogType.INFO: "\033[01m\033[46m\033[30m INFO \033[00m {}",
			LogType.SUCCESS: "\033[01m\033[42m\033[30m SUCCESS \033[00m {}",
			LogType.WARNING: "\033[01m\033[43m\033[30m WARNING \033[00m {}",
			LogType.ERROR: "\033[01m\033[41m\033[30m ERROR \033[00m {}",
			LogType.CRITICAL: "\033[01m\033[101m\033[30m CRITICAL \033[00m {}",
			LogType.INDENT: 4,
		}


class LamuFormatter(Formatter):
	"""Format text in Lamu style
	https://github.com/egoist/lamu
	"""

	def __init__(self):
		Formatter.__init__(self)
		self.format = {
			LogType.NONE: "{}",
			LogType.BOLD: "\033[01m{}\033[00m",
			LogType.ITALIC: "\033[03m{}\033[00m",
			LogType.HEADER: "\033[01m\033[04m{}\033[00m",
			LogType.DEBUG: "\033[96m   debug\033[00m  : :  {}",
			LogType.INFO: "\033[36m    info\033[00m  : :  {}",
			LogType.SUCCESS: "\033[32m success\033[00m  : :  {}",
			LogType.WARNING: "\033[33m warning\033[00m  : :  {}",
			LogType.ERROR: "\033[31m   error\033[00m  : :  {}",
			LogType.CRITICAL: "\033[91mcritical\033[00m  : :  {}",
			LogType.INDENT: 15,
		}


class CustomFormatter(Formatter):
	"""Create a custom formatter

	Args:
		none (str, optional): Set format for LogType.NONE.
		Defaults to "{}".
		bold (str, optional): Set format for LogType.BOLD.
		Defaults to "\033[01m{}\033[00m".
		italic (str, optional): Set format for LogType.ITALIC.
		Defaults to "\033[03m{}\033[00m".
		header (str, optional): Set format for LogType.HEADER.
		Defaults to "\033[01m\033[04m{}\033[00m".
		debug (str, optional): Set format for LogType.DEBUG.
		Defaults to "[\033[01m\033[96m$  Deb\033[00m] {}".
		info (str, optional): Set format for LogType.INFO.
		Defaults to "[\033[96m* Info\033[00m] {}".
		success (str, optional): Set format for LogType.SUCCESS.
		Defaults to "[\033[92m+   Ok\033[00m] {}".
		warning (str, optional): Set format for LogType.WARNING.
		Defaults to "[\033[93m/ Warn\033[00m] {}".
		error (str, optional): Set format for LogType.ERROR.
		Defaults to "[\033[91m-  Err\033[00m] {}".
		critical (str, optional): Set format for LogType.CRITICAL.
		Defaults to "[\033[01m\033[91m! Crit\033[00m] {}".
		indentPlain (int, optional): Set indent for 'plain' formats (None,
		Bold, Italic, and Header). Defaults to 9
	"""

	def __init__(
		self,
		none: str = "{}",
		bold: str = "\033[01m{}\033[00m",
		italic: str = "\033[03m{}\033[00m",
		header: str = "\033[01m\033[04m{}\033[00m",
		debug: str = "[\033[01m\033[96m$  Deb\033[00m] {}",
		info: str = "[\033[36m* Info\033[00m] {}",
		success: str = "[\033[32m+   Ok\033[00m] {}",
		warning: str = "[\033[33m/ Warn\033[00m] {}",
		error: str = "[\033[31m-  Err\033[00m] {}",
		critical: str = "[\033[01m\033[91m! Crit\033[00m] {}",
		indentPlain: int = 9,
	):
		Formatter.__init__(self)
		self.format = {
			LogType.NONE: none,
			LogType.BOLD: bold,
			LogType.ITALIC: italic,
			LogType.HEADER: header,
			LogType.DEBUG: debug,
			LogType.INFO: info,
			LogType.SUCCESS: success,
			LogType.WARNING: warning,
			LogType.ERROR: error,
			LogType.CRITICAL: critical,
			LogType.INDENT: indentPlain,
		}


class Logger:
	"""Setup a logger and call logPrint to print text in certian formats"""

	def __init__(self, formatter: Formatter = MeterpreterFormatter()):
		self.formatter = formatter

	def logPrint(self, text: str, logType: LogType = LogType.NONE, indentPlain: bool = False):
		"""Print in the formatter style

		Args:
			text (str): Text to print
			logType (LogType, optional): How to print. Defaults to "LogType.NONE".
			indentPlain (bool, optional): Indent for 'plain' formats (None,
			Bold, Italic, and Header). Defaults to False
		"""
		print(self.logString(text, logType, indentPlain))

	def logString(
		self, text: str, logType: LogType = LogType.NONE, indentPlain: bool = False
	) -> str:
		"""Get a string in the formatter style

		Args:
			text (str): Text to print
			logType (LogType, optional): How to print. Defaults to "LogType.NONE".
			indentPlain (bool, optional): Indent for 'plain' formats (None,
			Bold, Italic, and Header). Defaults to False
		"""
		padding = ""
		if logType in [LogType.NONE, LogType.BOLD, LogType.ITALIC, LogType.HEADER] and indentPlain:
			padding = " " * int(self.formatter.format[LogType.INDENT])
		return padding + str(self.formatter.format[logType].format(text))


# pylint: disable=no-member
# pyright: reportUnknownMemberType=false, reportUnknownArgumentType=false
# pyright: reportGeneralTypeIssues=false
"""
Option to set donations
"""
if hasattr(builtins, "METPRINT_DONATIONS") and len(builtins.METPRINT_DONATIONS) > 0:
	metprintDonations: dict[str, str] = builtins.METPRINT_DONATIONS
	print(
		str(len(metprintDonations))
		+ (" projects are" if len(metprintDonations) > 1 else " project is")
		+ " looking for funding:\n"
	)
	for project in metprintDonations:
		print(project + ": " + metprintDonations[project])
	print()

"""
Option to just print rather than dealing with setting up a new logger
"""
LAZY_FORMATTERS = {
	"MeterpreterFormatter": MeterpreterFormatter(),
	"FHFormatter": FHFormatter(),
	"FHNFFormatter": FHNFFormatter(),
	"PythonFormatter": PythonFormatter(),
	"ColorLogFormatter": ColorLogFormatter(),
	"PrintTagsFormatter": PrintTagsFormatter(),
	"XaFormatter": XaFormatter(),
	"LamuFormatter": LamuFormatter(),
}
if (
	hasattr(builtins, "METPRINT_LAZY_FORMATTER")
	and builtins.METPRINT_LAZY_FORMATTER in LAZY_FORMATTERS
):
	LAZY_PRINT = Logger(LAZY_FORMATTERS[builtins.METPRINT_LAZY_FORMATTER]).logPrint
else:
	LAZY_PRINT = Logger().logPrint  # type: ignore
