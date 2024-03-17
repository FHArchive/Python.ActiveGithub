# Metprint

[Python Index](../README.md#python-index) / [Lib](./index.md#lib) / Metprint

> Auto-generated documentation for [lib.metprint](../../../lib/metprint.py) module.

- [Metprint](#metprint)
  - [ColorLogFormatter](#colorlogformatter)
  - [CustomFormatter](#customformatter)
  - [FHFormatter](#fhformatter)
  - [FHNFFormatter](#fhnfformatter)
  - [Formatter](#formatter)
  - [LamuFormatter](#lamuformatter)
  - [LogType](#logtype)
  - [Logger](#logger)
    - [Logger().logPrint](#logger()logprint)
    - [Logger().logString](#logger()logstring)
  - [MeterpreterFormatter](#meterpreterformatter)
  - [PrintTagsFormatter](#printtagsformatter)
  - [PythonFormatter](#pythonformatter)
  - [XaFormatter](#xaformatter)

## ColorLogFormatter

[Show source in metprint.py:151](../../../lib/metprint.py#L151)

Format text in colorlog style
https://github.com/borntyping/python-colorlog

#### Signature

```python
class ColorLogFormatter(Formatter):
    def __init__(self): ...
```

#### See also

- [Formatter](#formatter)



## CustomFormatter

[Show source in metprint.py:240](../../../lib/metprint.py#L240)

Create a custom formatter

#### Arguments

----
 - `none` *str, optional* - Set format for LogType.NONE.
 Defaults to "{}".
 - `bold` *str, optional* - Set format for LogType.BOLD.
 Defaults to "[01m{}[00m".
 - `italic` *str, optional* - Set format for LogType.ITALIC.
 Defaults to "[03m{}[00m".
 - `header` *str, optional* - Set format for LogType.HEADER.
 Defaults to "[01m[04m{}[00m".
 - `debug` *str, optional* - Set format for LogType.DEBUG.
 Defaults to "[[01m[96m$  Deb[00m] {}".
 - `info` *str, optional* - Set format for LogType.INFO.
 Defaults to "[[96m* Info[00m] {}".
 - `success` *str, optional* - Set format for LogType.SUCCESS.
 Defaults to "[[92m+   Ok[00m] {}".
 - `warning` *str, optional* - Set format for LogType.WARNING.
 Defaults to "[[93m/ Warn[00m] {}".
 - `error` *str, optional* - Set format for LogType.ERROR.
 Defaults to "[[91m-  Err[00m] {}".
 - `critical` *str, optional* - Set format for LogType.CRITICAL.
 Defaults to "[[01m[91m! Crit[00m] {}".
 - `indentPlain` *int, optional* - Set indent for 'plain' formats (None,
 Bold, Italic, and Header). Defaults to 9

#### Signature

```python
class CustomFormatter(Formatter):
    def __init__(
        self,
        none: str = "{}",
        bold: str = "\x1b[01m{}\x1b[00m",
        italic: str = "\x1b[03m{}\x1b[00m",
        header: str = "\x1b[01m\x1b[04m{}\x1b[00m",
        debug: str = "[\x1b[01m\x1b[96m$  Deb\x1b[00m] {}",
        info: str = "[\x1b[36m* Info\x1b[00m] {}",
        success: str = "[\x1b[32m+   Ok\x1b[00m] {}",
        warning: str = "[\x1b[33m/ Warn\x1b[00m] {}",
        error: str = "[\x1b[31m-  Err\x1b[00m] {}",
        critical: str = "[\x1b[01m\x1b[91m! Crit\x1b[00m] {}",
        indentPlain: int = 9,
    ): ...
```

#### See also

- [Formatter](#formatter)



## FHFormatter

[Show source in metprint.py:91](../../../lib/metprint.py#L91)

Format text in my own style

#### Signature

```python
class FHFormatter(Formatter):
    def __init__(self): ...
```

#### See also

- [Formatter](#formatter)



## FHNFFormatter

[Show source in metprint.py:111](../../../lib/metprint.py#L111)

Format text in my own style with nerd fonts

#### Signature

```python
class FHNFFormatter(Formatter):
    def __init__(self): ...
```

#### See also

- [Formatter](#formatter)



## Formatter

[Show source in metprint.py:64](../../../lib/metprint.py#L64)

Format text in meterpreter style

#### Signature

```python
class Formatter:
    def __init__(self): ...
```



## LamuFormatter

[Show source in metprint.py:218](../../../lib/metprint.py#L218)

Format text in Lamu style
https://github.com/egoist/lamu

#### Signature

```python
class LamuFormatter(Formatter):
    def __init__(self): ...
```

#### See also

- [Formatter](#formatter)



## LogType

[Show source in metprint.py:10](../../../lib/metprint.py#L10)

Contains logtypes for this module

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

#### Warnings

-------
An indication that something unexpected happened, or indicative of some
problem in the near future (e.g. ‘disk space low’). The software is still
working as expected.

Error:
-----
Due to a more serious problem, the software has not been able to perform
some function.

CRITICAL
A serious error, indicating that the program itself may be unable to
continue running.

INDENT
Stores the indent for NONE, BOLD, ITALIC, HEADER

#### Signature

```python
class LogType(Enum): ...
```



## Logger

[Show source in metprint.py:300](../../../lib/metprint.py#L300)

Setup a logger and call logPrint to print text in certian formats

#### Signature

```python
class Logger:
    def __init__(self, formatter: Formatter = MeterpreterFormatter()): ...
```

#### See also

- [Formatter](#formatter)

### Logger().logPrint

[Show source in metprint.py:306](../../../lib/metprint.py#L306)

Print in the formatter style

#### Arguments

----
 - `text` *str* - Text to print
 - `logType` *LogType, optional* - How to print. Defaults to "LogType.NONE".
 - `indentPlain` *bool, optional* - Indent for 'plain' formats (None,
 Bold, Italic, and Header). Defaults to False

#### Signature

```python
def logPrint(
    self, text: str, logType: LogType = LogType.NONE, indentPlain: bool = False
): ...
```

#### See also

- [LogType](#logtype)

### Logger().logString

[Show source in metprint.py:319](../../../lib/metprint.py#L319)

Get a string in the formatter style

#### Arguments

----
 - `text` *str* - Text to print
 - `logType` *LogType, optional* - How to print. Defaults to "LogType.NONE".
 - `indentPlain` *bool, optional* - Indent for 'plain' formats (None,
 Bold, Italic, and Header). Defaults to False

#### Signature

```python
def logString(
    self, text: str, logType: LogType = LogType.NONE, indentPlain: bool = False
) -> str: ...
```

#### See also

- [LogType](#logtype)



## MeterpreterFormatter

[Show source in metprint.py:71](../../../lib/metprint.py#L71)

Format text in meterpreter style

#### Signature

```python
class MeterpreterFormatter(Formatter):
    def __init__(self): ...
```

#### See also

- [Formatter](#formatter)



## PrintTagsFormatter

[Show source in metprint.py:173](../../../lib/metprint.py#L173)

Format text in PrintTag style
https://github.com/mdlockyer/PrintTags
Note that this project provides other functionality that this one lacks

#### Signature

```python
class PrintTagsFormatter(Formatter):
    def __init__(self): ...
```

#### See also

- [Formatter](#formatter)



## PythonFormatter

[Show source in metprint.py:131](../../../lib/metprint.py#L131)

Format text in my python logger style

#### Signature

```python
class PythonFormatter(Formatter):
    def __init__(self): ...
```

#### See also

- [Formatter](#formatter)



## XaFormatter

[Show source in metprint.py:196](../../../lib/metprint.py#L196)

Format text in Xa style
https://github.com/xxczaki/xa

#### Signature

```python
class XaFormatter(Formatter):
    def __init__(self): ...
```

#### See also

- [Formatter](#formatter)