# Hypershot

Create screen shots of a video file, and upload them to an image host.

[![PyPI](https://img.shields.io/pypi/v/hypershot.svg)](https://pypi.python.org/pypi/hypershot/)

**Contents**

 * [Introduction](#introduction)
 * [Installation](#installation)
 * [Usage](#usage)
 * [Working with the Source Code](#working-with-the-source-code)
 * [Links](#links)


## Introduction

### What it Does

### How it Works


## Installation

You can install this software into your user home by using the following commands:

    mkdir -p ~/.local/venvs/hypershot && /usr/bin/pyvenv $_ ; . $_/bin/activate
    pip install -U pip
    pip install hypershot
    mkdir -p ~/bin && ln -nfs ../.local/venvs/hypershot/bin/hypershot $_


Doing it this way ensures that the software is installed in isolation not interfering
with other apps, and vice versa.
It also makes uninstalling very easy, because all files are contained in a single directory tree.

For a global install, do the above as `root` and replace `~/.local` by `/usr/local`, and
also replace the last command by this:

    ln -nfs ../venvs/hypershot/bin/hypershot /usr/local/bin

You might need to install `pyvenv` first, on Debian and Ubuntu this is done using
`sudo apt-get install python3-venv`.
If your platform does not come with a suitable Python3 package, consider using
[pyenv](https://github.com/pyenv/pyenv) to get Python 3.4+.


## Usage


## Working with the Source Code

### Releasing to PyPI

Building and uploading a (pre-)release:

    next=$(( 1 + $(grep ^tag_build setup.cfg | tr -cd 0-9) ))
    sed -i -e 's/^\(tag_build = .dev\).*/\1'$next'/' setup.cfg
    rm -rf dist
    ./setup.py sdist bdist_wheel
    twine upload --config-file setup.cfg dist/*.{zip,whl}


## Links

 * [docopt Manual](http://docopt.org/)
 * [A hands-on introduction to video technology](https://github.com/leandromoreira/digital_video_introduction)
