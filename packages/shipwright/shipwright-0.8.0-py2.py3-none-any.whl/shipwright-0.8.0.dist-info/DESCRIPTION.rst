Shipwright builds shared Docker images within a git repository in **the
right order** and publishes them tagged with git's revision/branch
information so you'll never loose track of an image's origin.

It's the perfect tool for building and publishing your images to places
like Docker Hub or your own private registry. Have a look at `our
motivation <docs/motivation.md>`__ to see why we built it and the pain
points it solves for you.

Installation
============

Shipwright is a simple python script you can install with pip

::

    $ pip install shipwright

Quickstart
==========

Once installed, simply change to a project of yours that contains
multiple Dockerfiles and is in git.

Add a json formatted file named ``.shipwright.json`` to the root
directory of your project. At minimum it should contain the version
number of your Shipwright config and a ``namespace`` which is either
your docker hub user name or the URL to your private repository.

1.0 is the current version for the config.

.. code:: json

    {
      "version": 1.0,
      "namespace": "[your docker hub name or private repository]"
    }

Additionally your config file can map directory names to alternative
docker repositories. For example here is a ``.shipwright.json`` for the
docker hub user ``shipwright`` that also maps the root of the git
repository to the docker image ``shipwright/shared`` and the ``/foo``
directory to ``shipwright/awesome_sauce``.

.. code:: json

    {
      "version": 1.0,

      "namespace": "shipwright",
      "names": {
        "/": "shipwright/shared",
        "/foo": "shipwright/awesome_sauce"
    }

Now you can build all the docker images in the git repo by simply
changing to any directory under your git repo and running:

::

    $ shipwright

This will recurse through all the directories, looking for ones that
contain a Dockerfile. Shipwright will build these Dockerfiles in order
and by default tag them with ``<namespace>/<dirname>:<git commit>``
along with ``<namespace>/<dirname>:<git branch>`` and
``<namespace>/<dirname>:latest``

Working example
---------------

We have `a sample shipwright
project <https://github.com/6si/shipwright-sample>`__ you can use if you
want to try this out right away.

.. code:: bash

    $ git clone https://github.com/6si/shipwright-sample.git
    $ cd shipwright-sample
    $ shipwright 

**NOTE: you can use any username you'd like while building locally. In
the above example we use ``shipwright``. Nothing is published unless you
use the ``push`` command. For your own projects, substitute
``shipwright`` in the above example with your (or your organizations)
official docker hub username or private repository.**

Notice that if you run the ``shipwright`` a second time it will return
immediately without doing anything. Shipwright is smart enough to know
nothing has changed.

Shipwright really shines when you switch git branches.

.. code:: bash

    $ git checkout new_feature
    $ shipwright

Notice that shipwright only rebuilt the shared library and service1,
ignoring the other projects because they have a common git ancestry.
Running ``docker images`` however shows that all the images in the git
repository have been tagged with the latest git revision, branch and
``latest``.

In fact, as Shipwright builds images it rewrites the Dockerfiles so
that they require the base images with tags from the current git
revision. This ensures that the entire build is deterministic and
reproducible.

Building
========

By default, if you run shipwright with no arguments, it will build all
Dockerfiles in your git repo. You can specify one or more ``specifiers``
to select fewer images to build. For example you can build a single
images and its dependencies by simply specifying its name on the command
line.

::

    $ shipwright <namespace>/some_image

Run \`shipwright --help' for more examples of specifiers and their uses.

Publishing
==========

With one command Shipwright can build your images and push them to a
remote repository.

::

    $ shipwright push

If you like you can just push your latest images without building.

::

    $ shipwright push --no-build 

The same specifiers for building also work with ``push``. You might use
this to build an entire tree in one step then push a specific image like
so.

::

    $ shipwright build
    $ shipwright push -e <namespace>/public_image


0.8.0 (2017-06-08)
------------------

- Add proper stack traces for direct registry errors.
  (`Issue #93 <https://github.com/6si/shipwright/pull/93>`_).
- Handle differences between docker over TCP and Unix socket.
  (`Issue #96 <https://github.com/6si/shipwright/pull/96>`_).
- Mark every internal package as private to allow exporting
  of select parts of shipwright publicly.
  (`Issue #99 <https://github.com/6si/shipwright/pull/99>`_).
- Create shipwright.targets.targets function to list available
  docker targets in a repo programaticaly.
  (`Issue #100 <https://github.com/6si/shipwright/pull/100>`_).


0.7.0 (2017-01-13)
------------------

- Depend on docker>=2.0.1.
  (`Issue #91 <https://github.com/6si/shipwright/pull/91>`_).


0.6.6 (2017-01-13)
------------------

- Exprimental --registry-login cache flag to skip creation of already built
  images and speed up tagging. Feature not subject to semver.
  (`Issue #89 <https://github.com/6si/shipwright/pull/89>`_).

0.6.5 (2017-01-08)
------------------

- Fix changelog.


0.6.4 (2017-01-08)
------------------

- Add images command for creating docker save.
  (`Issue #88 <https://github.com/6si/shipwright/pull/88>`_).


0.6.3 (2016-08-24)
------------------

- Push images to the registry in parallel.
  (`Issue #82 <https://github.com/6si/shipwright/pull/82>`_).


0.6.2 (2016-08-23)
------------------

- Also push image target ref so that --pull-cache can pull them.
  (`Issue #81 <https://github.com/6si/shipwright/pull/81>`_).


0.6.1 (2016-08-23)
------------------

- Warn on --pull-cache errors
  (`Issue #80 <https://github.com/6si/shipwright/pull/80>`_).


0.6.0 (2016-08-22)
------------------

- Add --pull-cache to pull images from repository before building.
  (`Issue #49 <https://github.com/6si/shipwright/issues/49>`_).


0.5.0 (2016-08-19)
------------------

- Add --dirty to build from working tree, even when uncommitted and untracked changes exist.
  (`Issue #74 <https://github.com/6si/shipwright/pull/74>`_).
  Thanks `James Pickering <https://github.com/jamespic>`_!
- Ignore images without RepoTags when gathering built_tags to fix a crash
  caused by docker images pulled via RepoDigest.
  (`Issue #77 <https://github.com/6si/shipwright/issues/77>`_).
  Thanks `kgpayne <https://github.com/kgpayne>`_!


0.4.2 (2016-06-16)
------------------

- Correct naming, shipwright builds docker images.
  (`Issue #71 <https://github.com/6si/shipwright/pull/71>`_)
- Allow building with a detached HEAD
  (`Issue #72 <https://github.com/6si/shipwright/pull/72>`_)


0.4.1 (2016-06-15)
------------------

- Fix push crash. (`Issue #70 <https://github.com/6si/shipwright/pull/70>`_)


0.4.0 (2016-06-13)
------------------

- Isolate all git functionality, so as to create pluggable Source Control wrappers.
- More efficient required build detection. (`Issue #63 <https://github.com/6si/shipwright/pull/63>`_)
- Isolate all zipper usage, vendor zipper library.

0.2.2 (2015-01-07)
------------------

-  Fix bug missing ``tls`` when communicating with docker over a unix
   socket.

0.2.1 (2015-01-01)
------------------

-  Force tag to support docker 1.4.1
-  Requries docker-py >= 0.6
-  Added ``assert_hostname`` as an option to ``.shipwright.json``
-  Added command line option ``--x-assert-hostname`` to disable hostname
   checking when TLS is used. Useful for boot2docker

0.2.0 (2014-12-31)
------------------

-  Added ``shipwright push`` and ``shipwright purge``
-  Added support for specifiers ``-u``, ``-d``, ``-e`` and ``-x``

0.1.0 (2014-09-10)
------------------

-  Build and tag containers
-  Moved config to ``.shipwright.json``


