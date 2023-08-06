# Hypershot

Create screen shots of a video file, and upload them to an image host.

**IN DEVELOPMENT**

[![PyPI](https://img.shields.io/pypi/v/hypershot.svg)](https://pypi.python.org/pypi/hypershot/)

**Contents**

 * [Introduction](#introduction)
   * [What it Does](#what-it-does)
   * [How it Works](#how-it-works)
 * [Installation](#installation)
 * [Usage](#usage)
 * [Configuration](#configuration)
 * [Working with the Source Code](#working-with-the-source-code)
   * [Creating a Working Directory](#creating-a-working-directory)
   * [Releasing to PyPI](#releasing-to-pypi)
 * [Links](#links)


## Introduction

### What it Does

Look at one or more video files, taking screen shots without any human interaction,
uploading the results to an image hosting service, and finally produce some text
output containing links to the images.
That output can be used for posting to forums, blogs, etc.

*hypershot* is designed for and tested on *Linux*, and it is expected and supported
to run on *Mac OSX* (report any issues you might encounter).
It *might* run on *Windows*, if you use *CygWin/Babun*, *Ubuntu for Windows*,
or one of the *Docker* distributions for *Windows*.


### How it Works

*hypershot* looks at a video file using *mediainfo*,
and then decides on the offsets for the screen shots,
depending on how many you requested and the duration of the video.
It then calls an external script or command to take those screenshots
– a default script using *mplayer*, *ffmpeg* or *avconv* is provided.

The resulting images are then uploaded to a configured image hoster,
and the returned URLs plus the mediainfo data are fed into a templating engine.
This way you can generate HTML, BBcode, Markdown, or whatever (text) format
you need. Then take the final result and post your screen shots on the web.

See [Usage](#usage) for more details, and the following section
on how to install the necessary software.


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

Look at the start of the
[cli.py](https://gitlab.com/kybernetics/hypershot/blob/master/src/hypershot/cli.py)
module for usage information on the ``hypershot`` command,
or call ``hypershot -h`` after installation.

See the next section for examples and details on all supported configuration settings.


## Configuration

### Configuration File

Configuration is read from the file ``~/.config/hypershot/config.yaml`` (on Linux, following the XDG spec).
Only [YAML](http://lzone.de/cheat-sheet/YAML) is supported.
You can set a different location for the configuration file using ``--config-dir``,
the file itself is always called either ``config.yaml`` or ``config.yml``.

All command line parameters can be given a custom default via either the configutation file or an environment variable.
Specifically, ``HYPERSHOT_CONFIG_DIR`` can be used to set a different default for the ``--config-dir`` option.

### Image Hosters

``imgur.com`` is the default service, and you need to [register](https://api.imgur.com/oauth2/addclient)
with them if you want to use the service.
Select *“Anonymous usage without user authorization”*, which will give you a *client ID* and a *client secret*.
Add those values to the ``~/.netrc`` file like this:

    machine hypershot:api.imgur.com
        login ‹CLIENT_ID›
        password ‹CLIENT_SECRET›

Here is an example for a [Chevereto](https://chevereto.com/) site:

    services:
      example:
        handler: chevereto
        url: "https://images.example.com"
        limit: 4M
        types: [PNG, JPEG, BMP, GIF]
        login: .netrc
        nsfw: off

In this example, the special value ``.netrc`` means
the username and password are kept separate in the ``~/.netrc`` file,
which is commonly used to store credentials for FTP access and similar services.
Otherwise, provide ``login`` and ``password`` in the YAML file directly.

So also add this to the ``~/.netrc`` file:

    machine images.example.com
        login YOURNAME
        password KEEP_ME_SECRET

This file must be private, therefor call ``chmod 0600 ~/.netrc`` after you initially create it.


## Working with the Source Code

### Creating a Working Directory

    # Use "git@gitlab.com:kybernetics/hypershot.git" if you have developer access
    git clone "https://gitlab.com/kybernetics/hypershot.git"
    cd hypershot; mkdir -p .venv/$_; /usr/bin/pyvenv $_; . $_/bin/activate
    pip install -U pip
    pip install -r requirements-dev.txt


### Releasing to PyPI

Building and uploading a (pre-)release:

    next=$(( 1 + $(grep ^tag_build setup.cfg | tr -cd 0-9) ))
    sed -i -e 's/^\(tag_build = .dev\).*/\1'$next'/' setup.cfg
    rm -rf dist
    ./setup.py sdist bdist_wheel
    twine upload --config-file setup.cfg dist/*.{zip,whl}


## Links

 * [docopt Manual](http://docopt.org/)
 * [A hands-on introduction to video technology](https://github.com/leandromoreira/digital_video_introduction#intro)
