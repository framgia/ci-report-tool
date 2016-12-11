# Framgia CI CLI Tool

[![PyPI](https://img.shields.io/pypi/v/framgia-ci.svg)](https://pypi.python.org/pypi/framgia-ci/)
[![PyPI](https://img.shields.io/pypi/pyversions/framgia-ci.svg)]([![PyPI](https://img.shields.io/pypi/v/framgia-ci.svg)](https://pypi.python.org/pypi/framgia-ci/))
[![PyPI](https://img.shields.io/pypi/status/framgia-ci.svg)](https://pypi.python.org/pypi/framgia-ci/)
[![PyPI](https://img.shields.io/pypi/dm/framgia-ci.svg)](https://pypi.python.org/pypi/framgia-ci/)
[![PyPI](https://img.shields.io/pypi/dw/framgia-ci.svg)](https://pypi.python.org/pypi/framgia-ci/)
[![PyPI](https://img.shields.io/pypi/dd/framgia-ci.svg)](https://pypi.python.org/pypi/framgia-ci/)

- A part of **Framgia CI** service
- A tool for managing project configuration, as well as running test commands with **Framgia CI** Service
- Written in Python
- Authors: **Tran Duc [@wataridori](https://github.com/wataridori) Thang** - **Nguyen Anh [@vigov5](https://github.com/vigov5) Tien**

## Install
### Linux
#### Pre-compiled executale file
- For running inside **Docker Container**, which does not contain Python in almost cases
```
// Using curl
curl -o /usr/bin/framgia-ci https://raw.githubusercontent.com/framgia/ci-report-tool/master/dist/framgia-ci && chmod +x /usr/bin/framgia-ci

// Using wget
wget -O /usr/bin/framgia-ci https://raw.githubusercontent.com/framgia/ci-report-tool/master/dist/framgia-ci && chmod +x /usr/bin/framgia-ci
```
#### Install by using `pip`
- Requirement: **python 3.5**
- Command:
```
pip install framgia-ci
```

### Mac OS
#### Install by using `pip`
- Requirement: **python 3.5** (You may have to install `python3` by using `brew` first)
- Command:
```
// Install python3
brew install python3

// Install framgia-ci
pip3 install framgia-ci
```

## Usage
- Command lists
```
check-config  Validate config file
finish        Running finish command tools
init          Init new config file base-ed on template. Supported project type: php, ruby, android
report        Running report command to send request to CI Report service
run           Running test, report, finish command
show-config   Display current config
test          Running test tools
```

For example
```
// Init .framgia-ci.yml configuration file for php project
framgia-ci init php

// Run test commands defined in .framgia-ci.yml
framgia-ci test

// Run all test, report, finish commands. This should only be run inside framgia ci service
framgia-ci run
```

Contribution
--------------
View contribution guidelines [here](./CONTRIBUTING.md)
