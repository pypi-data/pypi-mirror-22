# connect.py

[![PyPI](https://img.shields.io/pypi/v/connect.py.svg)](https://pypi.python.org/pypi/connect.py/)
[![PyPI](https://img.shields.io/pypi/pyversions/connect.py.svg)](https://pypi.python.org/pypi/connect.py/)
[![Build Status](https://travis-ci.org/GiovanniMCMXCIX/connect.py.svg?branch=master)](https://travis-ci.org/GiovanniMCMXCIX/connect.py)

connect.py is an API wrapper for Monstercat Connect written in Python.

If you want to report errors, bugs, typos or yell at me for my wrapper being garbage join the chat in [here](https://discord.gg/u5F8y9W)

## Installing

To install the library, you can just run the following command:

```
python3 -m pip install -U connect.py
```

To install the development version, do the following:

```
python3 -m pip install -U https://github.com/GiovanniMCMXCIX/connect.py/archive/master.zip
```

## Requirements

- Python 3.x
- `requests` library

Usually `pip` will handle these for you.

## Bugs

- List that come from the library are positioned random in versions older than Python 3.6
Example `['foo', 'bar', 'wew', 'lad']` comes as `['bar', 'lad', 'foo', 'wew']`

