# Framgia CI CLI Tool

[![PyPI](https://img.shields.io/pypi/status/framgia-ci.svg)](https://pypi.python.org/pypi/framgia-ci/)
[![PyPI](https://img.shields.io/pypi/v/framgia-ci.svg)](https://pypi.python.org/pypi/framgia-ci/)
[![PyPI](https://img.shields.io/pypi/pyversions/framgia-ci.svg)]([![PyPI](https://img.shields.io/pypi/v/framgia-ci.svg)](https://pypi.python.org/pypi/framgia-ci/))

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
// Install
pip install framgia-ci

// Update
pip install --upgrade framgia-ci
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

// Update
pip3 install --upgrade framgia-ci
```

## Usage
- Command lists
```
check-config  Validate config file
finish        Running finish command tools
init          Init new config file base-ed on template. Supported project type: php, ruby, android
report        Running report command to send copying request to CI Report service
notify        Running notify command to send notify request to CI Report service
run           Running test, report, finish command
run --local   Running test, finish command. For running at local machine
show-config   Display current config
test          Running test tools
test-connect  Test connection to specific host and port
```

For example
```
// Init .framgia-ci.yml configuration file for php project
framgia-ci init php

// Run test commands defined in .framgia-ci.yml
framgia-ci test

// Run all test, report, finish commands. This should only be run inside framgia ci service
framgia-ci run

// Run test and show results at local machine
framgia-ci run --local

// Check mysql connection in localhost
framgia-ci test-connect 127.0.0.1 3306
```

## Framgia CI Configuration
- All additional configurations for Framgia CI Service **MUST** be stored in `.framgia-ci.yml` file.
- The configurations have to be written in `yaml` format.
- Example configuration file:
```
project_type: php
test:
  phpcpd:
    ignore: true
    command: phpcpd --log-pmd=.framgia-ci-reports/phpcpd.xml app
  phpmd:
    ignore: true
    command: phpmd app xml
      cleancode,codesize,controversial,design,naming,unusedcode --reportfile .framgia-ci-reports/phpmd.xml
  pdepend:
    ignore: true
    command: pdepend --summary-xml=.framgia-ci-reports/pdepend.xml
      --jdepend-chart=.framgia-ci-reports/pdepend.svg
      --overview-pyramid=.framgia-ci-reports/pyramid.svg
      app
  phpmetrics:
    ignore: true
    command: phpmetrics --report-html=.framgia-ci-reports/metrics.html
      --report-xml=.framgia-ci-reports/metrics.xml
      app
  eslint:
    command: eslint --format=checkstyle
      --output-file=.framgia-ci-reports/eslint.xml
      resources/assets/js/
  phpcs:
    command: phpcs --standard=Framgia --report-checkstyle=.framgia-ci-reports/phpcs.xml app
  phpunit:
    command:
      - framgia-ci test-connect 127.0.0.1 3306
      - php artisan migrate --database=mysql_test
      - php -dzend_extension=xdebug.so vendor/bin/phpunit
        --coverage-clover=.framgia-ci-reports/coverage-clover.xml
        --coverage-html=.framgia-ci-reports/coverage
```
- `project_type` key: Define the type of the project. Currently supports `php`, `ruby` and `android`. This key is **required**
- `test` key: Define test section with customizable commands. This section is **required**
- `phpcpd`, `phpmd`, `phpcs`, `phpunit` ...: Configuration for each test tools. All of them will be executed, even if the other test tools are success or not.
- `ignore` key: Define whether the build should be considered as `failed` or not when the test tool is failed. The default value is `false`. If you set it to `true`, the build will be considered as success even when the command returns `false` (with non-zero `exit code`)
- `command`: The section that defines command(s) that are expected to be run. If there are more than one commands in this section, `framgia-ci` will try to run them in the order from top to bottom. However, if one of them is failed, the entire section will be stopped, and the below commands will not be executed.
- All the reports file (if existed) **MUST** be exported to a folder named `.framgia-ci-reports`
- You can also use `from` keyword to extend from default template. For example:
```
from: php
test:
  phpcs:
    ignore: true # Extend the default configuration from php template, but override the ignore property for phpcs tool
```

Contribution
--------------
View contribution guidelines [here](./CONTRIBUTING.md)
