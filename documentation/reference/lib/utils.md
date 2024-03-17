# Utils

[Python Index](../README.md#python-index) / [Lib](./index.md#lib) / Utils

> Auto-generated documentation for [lib.utils](../../../lib/utils.py) module.

- [Utils](#utils)
  - [clear](#clear)
  - [getDatetime](#getdatetime)
  - [getPassword](#getpassword)
  - [getUsername](#getusername)
  - [getUsernameAndLifespan](#getusernameandlifespan)

## clear

[Show source in utils.py:15](../../../lib/utils.py#L15)

Clear the terminal.

#### Signature

```python
def clear(): ...
```



## getDatetime

[Show source in utils.py:20](../../../lib/utils.py#L20)

Get the datetime from a date in the format YYYY-MM-DDThh:mm:ssZ e.g. 2000-01-01T00:00:00Z.

#### Signature

```python
def getDatetime(datetimeIn: str): ...
```



## getPassword

[Show source in utils.py:30](../../../lib/utils.py#L30)

Get authenticated password.

#### Signature

```python
def getPassword() -> str: ...
```



## getUsername

[Show source in utils.py:25](../../../lib/utils.py#L25)

Get authenticated username.

#### Signature

```python
def getUsername() -> str: ...
```



## getUsernameAndLifespan

[Show source in utils.py:35](../../../lib/utils.py#L35)

Return the username from env.json and lifespan from user input.

#### Signature

```python
def getUsernameAndLifespan() -> tuple[str, int]: ...
```