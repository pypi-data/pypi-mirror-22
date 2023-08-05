[![Python Version](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/release/python-350/)
[![Packagist](https://img.shields.io/packagist/l/doctrine/orm.svg?maxAge=2592000)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/brome/badge/?version=release)](http://brome.readthedocs.io/en/release/?badge=release)
[![PyPI version](https://badge.fury.io/py/brome.svg)](https://badge.fury.io/py/brome)
[![Build Status](https://travis-ci.org/jf-parent/brome.svg?branch=release)](https://travis-ci.org/jf-parent/brome)

# BROME - Selenium Framework

* Documentation: https://brome.readthedocs.org
* Blog: http://brome-hq.logdown.com/

# Features

* Simple API
* Focused on test stability and uniformity
* Highly configurable
* Runner for Amazon EC2, Saucelabs, Browserstack, Virtualbox and Appium
* Javascript implementation of select, drag and drop, scroll into view, inject script
* IPython embed on assertion for debugging
* Session Video recording
* Network capture with mitmproxy (firefox & chrome)
* Persistent test report
* Webserver written in React & Redux [Webbase](https://github.com/jf-parent/webbase)
* Test state persistence system
* Easier support for mobile testing (e.g.: click use Touch)

# Quick-start

* install mongodb first!

```bash
$ cookiecutter https://github.com/jf-parent/cookiecutter-brome
$ ./bro run -l firefox -s example
```
