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
   * [Configuration File](#configuration-file)
   * [Image Hosters](#image-hosters)
     * [Chevereto Sites](#chevereto-sites)
     * [imgur](#imgur)
   * [Logging Configuration](#logging-configuration)
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
    pip install -r "https://gitlab.com/kybernetics/hypershot/raw/master/requirements.txt"
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
To list all the image hosting services, both provided as defaults and those added
via the configuration, call ``hypershot services``.


## Configuration

### Configuration File

Configuration is read from the file ``~/.config/hypershot/config.yaml`` (on Linux, following the XDG spec).
Only [YAML](http://lzone.de/cheat-sheet/YAML) is supported.
You can set a different location for the configuration file using ``--config-dir``,
the file itself is always called either ``config.yaml`` or ``config.yml``.

All command line parameters can be given a custom default via either the configutation file or an environment variable.
Specifically, ``HYPERSHOT_CONFIG_DIR`` can be used to set a different default for the ``--config-dir`` option.

To select a named image hosting service (which can be configured as shown in the next section),
use either ``service: ‹name›`` in the config file, ``HYPERSHOT_SERVICE=‹name›`` in the environment,
or ``-s ‹name›`` on the command line.


### Image Hosters

#### Simple File Upload Sites

If a site basically does a HTML form upload (``multipart/form-data``), use the ``file_upload`` handler.

Consider this example for [https://lut.im/](https://lut.im/):

    services:
      lutim:
        handler: file_upload
        url: "https://lut.im/"
        limit: 5M
        types: [JPG, PNG, BMP, GIF]
        upload_url: "{url}"
        headers:
          Referer: "{url}"
        data:
          delete-day: 0
          crypt: on
        files_field_name: "file"
        response_regex: '<a href="(?P<scheme>[^:]+)://(?P<domain>[^/]+)/(?P<image>[^"]+)"[^>]*><img class="thumbnail'
        image_url: "https://{response[domain]}/{response[image]}"

You can set the HTTP POST request ``headers``,
and add any form ``data`` in addition to the file upload field.
The name of that field must be given in ``files_field_name``.

The provided ``response_regex`` is used to scan a HTTP response of type ``text/html`` or ``text/plain``,
and must contain at least one named group of the form ``(?P<name>...)``.
Those named groups are available in ``response``, in addition to all the handler's settings,
to build an ``image_url`` using the [Python string formatter](https://pyformat.info/#getitem_and_getattr).

In case of a JSON response, you can use ``json`` instead of ``response`` for building your ``image_url``.


#### Chevereto Sites

A good service powered by [Chevereto](https://chevereto.com/) is ``malzo.com``,
because you can use it anonymously
and it has a high size limit of 30 MiB.
If you want to use an account you have there,
the next paragraph shows you how
– otherwise leave out the ``login`` attribute.

Here is an example including user account credentials
– these settings go into ``config.yaml`` like all other ones:

    services:
      malzo:
        handler: chevereto
        url: "https://malzo.com"
        limit: 30M
        types: [JPG, PNG, BMP, GIF]
        login: .netrc

In this example, the special value ``.netrc`` means
the username and password are kept separate in the ``~/.netrc`` file,
which is commonly used to store credentials for FTP access and similar services.
Otherwise, provide ``login`` and ``password`` in the YAML file directly.

So also add this to the ``~/.netrc`` file:

    machine hypershot:malzo.com
        login YOURNAME
        password KEEP_ME_SECRET

This file must be private, therefor call ``chmod 0600 ~/.netrc`` after you initially create it.

See [this config.yaml](https://gitlab.com/kybernetics/hypershot/blob/master/docs/examples/config.yaml)
for more examples.


#### imgur

To use the built-in ``imgur`` service you need to
[register](https://api.imgur.com/oauth2/addclient) with them.
Select *“Anonymous usage without user authorization”*,
which will give you a *client ID* and a *client secret*.
Add those values to the ``~/.netrc`` file like this:

    machine hypershot:api.imgur.com
        login ‹CLIENT_ID›
        password ‹CLIENT_SECRET›


### Logging Configuration

The Python logging system can be configured by one of the files
`logging.yaml`, `logging.yml`, or `logging.ini`.
They must be located in the configuration directory,
and are checked in the mentioned order.

Consult the [Python Guide](http://python-guide-pt-br.readthedocs.io/en/latest/writing/logging/#logging-in-an-application)
and the [Logging How-To](https://docs.python.org/3/howto/logging.html#basic-logging-tutorial)
for details on the logging machinery and its configuration.
For the YAML files, the *dictionary* method applies (using ``dictConfig``), here is an example configuration:

    ---
    version: 1

    formatters:
      fmt:
        format: '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'

    handlers:
      stdout:
        class: logging.StreamHandler
        formatter: fmt
        level: NOTSET

    root:
      handlers:
        - stdout
      level: NOTSET

    ...

The logging level threshold of the root logger depends
on the values of ``debug`` (``DEBUG``) and ``verbose`` (``INFO``)
– if neither is set, the level is ``WARNING``.


## Working with the Source Code

### Creating a Working Directory

    # Use "git@gitlab.com:kybernetics/hypershot.git" if you have developer access
    git clone "https://gitlab.com/kybernetics/hypershot.git"
    cd hypershot; mkdir -p .venv/$_; /usr/bin/pyvenv $_; . $_/bin/activate
    pip install -U pip
    pip install -r requirements-dev.txt


### Releasing to PyPI

Building and uploading a (pre-)release:

    # pre-release
    next=$(( 1 + $(grep ^tag_build setup.cfg | tr -cd 0-9) ))
    sed -i -e 's/^\(tag_build = .dev\).*/\1'$next'/' setup.cfg

    # release
    sed -i -re 's/^(tag_[a-z ]+=)/##\1/' setup.cfg
    version="$(./setup.py --version)"
    git tag -a "v$version" -m "Release $version"

    # build & upload
    rm -rf dist
    ./setup.py sdist bdist_wheel
    twine upload --config-file setup.cfg dist/*.{zip,whl}


## Links

 * [docopt Manual](http://docopt.org/)
 * [A hands-on introduction to video technology](https://github.com/leandromoreira/digital_video_introduction#intro)
