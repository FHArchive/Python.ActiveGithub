# utils

> Auto-generated documentation for [lib.utils](../../lib/utils.py) module.

Adds functions used by both github_graph and github_rest.

- [Python](../README.md#python-index) / [Modules](../README.md#python-modules) / [lib](index.md#lib) / utils
    - [clear](#clear)
    - [getDatetime](#getdatetime)
    - [getPassword](#getpassword)
    - [getUsername](#getusername)
    - [getUsernameAndLifespan](#getusernameandlifespan)

## clear

[[find in source code]](../../lib/utils.py#L15)

```python
def clear():
```

Clear the terminal.

## getDatetime

[[find in source code]](../../lib/utils.py#L20)

```python
def getDatetime(datetimeIn: str):
```

Get the datetime from a date in the format YYYY-MM-DDThh:mm:ssZ e.g. 2000-01-01T00:00:00Z.

## getPassword

[[find in source code]](../../lib/utils.py#L30)

```python
def getPassword() -> str:
```

Get authenticated password.

## getUsername

[[find in source code]](../../lib/utils.py#L25)

```python
def getUsername() -> str:
```

Get authenticated username.

## getUsernameAndLifespan

[[find in source code]](../../lib/utils.py#L35)

```python
def getUsernameAndLifespan() -> tuple[(str, int)]:
```

Return the username from env.json and lifespan from user input.
