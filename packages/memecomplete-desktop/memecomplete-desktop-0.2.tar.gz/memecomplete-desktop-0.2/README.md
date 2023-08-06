Unix: [![Unix Build Status](http://img.shields.io/travis/jacebrowning/memecomplete-desktop/master.svg)](https://travis-ci.org/jacebrowning/memecomplete-desktop) Windows: [![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/memecomplete-desktop/master.svg)](https://ci.appveyor.com/project/jacebrowning/memecomplete-desktop)<br>Metrics: [![Coverage Status](http://img.shields.io/coveralls/jacebrowning/memecomplete-desktop/master.svg)](https://coveralls.io/r/jacebrowning/memecomplete-desktop) [![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/memecomplete-desktop.svg)](https://scrutinizer-ci.com/g/jacebrowning/memecomplete-desktop/?branch=master)<br>Usage: [![PyPI Version](http://img.shields.io/pypi/v/memecomplete-desktop.svg)](https://pypi.python.org/pypi/memecomplete-desktop) [![PyPI Downloads](http://img.shields.io/pypi/dm/memecomplete-desktop.svg)](https://pypi.python.org/pypi/memecomplete-desktop)

# Overview

Desktop client for https://memecomplete.com.

# Setup

## Requirements

* Python 3.6+
* SpeechRecognition requirements: https://github.com/Uberi/speech_recognition#requirements
  * macOS: `$ brew install flac portaudio swig`

## Installation

Install the client with pip:

```sh
$ pip install memecomplete-desktop
```

or directly from the source code:

```sh
$ git clone https://github.com/jacebrowning/memecomplete-desktop.git
$ cd memecomplete-desktop
$ python setup.py install
```

# Usage

Launch the GUI from the command-line:

```sh
$ memecomplete
```
