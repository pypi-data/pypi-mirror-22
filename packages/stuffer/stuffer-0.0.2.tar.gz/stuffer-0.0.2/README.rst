Stuffer - simplified, container-friendly provisioning
=====================================================

Stuffer is a provisioning tool designed to be simple, and to be used in
simple scenarios.

Documentation is hosted on `<http://stuffer.readthedocs.io>`_.


Project status
--------------

Alpha. Raw but usable. The documentation is sparse. In some cases, it describes intentions, some of
which are not implemented.


Use cases
---------

Stuffer is primarily intended to be used for provisioing container images, Docker in particular. As
a secondary use case, it can be used to provision non-production machines, e.g. developer machines.

More complex provisioning tools, such as Puppet, Chef, and Ansible, are intended for bringing a
machine in an arbitrary state to a desired state. This turns out not to be possible in practice, and
production machines manages with such tools tend to suffer from outdated dependency packages, etc.

Stuffer is primarily intended for building a machine from scratch to the desired state. Since the
initial state is known, much of the complexity of existing provisioning tools is unnecessary. For
example, during an image build, running services need not be considered or restarted.

Overview
--------

Stuffer uses a Python embedded DSL for specifying provisioning directives. It is typically invoked
with one or more command arguments on the command line, e.g.:
::

    stuffer 'apt.Install("mercurial")'


Multiple arguments are concatenated into a multiple line Python recipe:
::

    stuffer \
      'for pkg in "mercurial", "gradle", "python-nose":' \
      '  print("Installing", pkg)' \
      '  apt.Install(pkg)'


Reused recipes can be factored out into Python modules for easier reuse:
::

    stuffer 'development.Tools()'

In development.py:
::

    from stuffer.core import Group

    class Tools(Group):
      def children(self):
        return [apt.Install(p) for p in "mercurial", "gradle", "python-nose"]

Stuffer comes with builtin knowledge of Docker best practices, which it
can enforce for you:

::

    Dockerfile:
      FROM phusion/baseimage:0.9.18

      RUN stuffer 'docker.Prologue()'  # Verifies e.g. that base image is sound.

      RUN stuffer ... # Install stuff

      RUN stuffer 'docker.Epilogue()'  # Cleans temporary files, warns about known anti-patterns in the statements above.


Design goals
------------

Stuffer design gives priority to:

-  Simplicity of use. No knowledge about the tool should be required in order to use it for simple scenarios by copying
   examples. Some simplicity in the implementation is sacrificed in order to make the usage interface simple. Actions
   are named similarly to the corresponding shell commands.

-  Transparency. Whenever reasonable, actions are translated to shell commands. All actions are logged.

-  Ease of reuse. It should be simple to extract commands from snippets and convert them to reusable modules without a
   rewrite.

-  Docker cache friendliness. Images built with similar commands should be able to share a prefix of commands in order
   to benefit from Docker image caching.

-  No dislike factors. Provisioning tools tend to be loved and/or hated by users, for various
   reasons. There might be no reason to be passionately enamoured with stuffer, but there should be
   no reason to have a strong dislike for it, given that you approve of Python and Docker.

-  Ease of debugging. Debugging stuffer recipes should be as easy as debugging standard Python programs.

-  Avoid reinventing wheels. Use existing Python modules or external tools for tasks that have already been solved. Give
   priority to reusing existing code over minimising dependencies. In particular, use Python 3 and click to save
   boilerplate.


Moreover, the project model is design to facilitate sharing and reuse of code between users, see below.


DSL
---

The DSL is designed to be comprehensible by readers that are not familiar with stuffer. For example,
the command apt.Install("mypack") runs "apt-get install mypack". There is a balance between
convenience and comprehensibility, and stuffer in most cases shuns magic that would create
convenience in preference for more understandable code.

The DSL is also designed to make it easy to do things that are correct and work well with
containers, and difficult to do things that do not harmonise with containers.

The DSL is designed to be tool friendly (with IntelliJ/PyCharm and pylint in particular), both for
writing stuff files and for working on stuffer itself. For example, all imports are explicitly
declared in order to make structure visible to tools.

Python conventions are used for naming, i.e. CamelCase classes and snake_case functions.


Collaboration model
-------------------

Users are allowed to put recipes under sites/ for others to get inspired. This model may not scale,
but as long as the number of users is small, there is value in sharing and showing each other code
snippets, in order to extract pieces of common value.

Snippets worth reuse can be put under stuffer/contrib/. Files under stuffer/contrib are expected to
be maintained by the contributor.

Routines for installing third-party software should also go under stuffer/contrib.


Contributing
------------

New code should be covered with integration tests. Avoid unit tests - since the purpose of stuffer is integration,
there is little value testing scenarios that are not authentic. Strive to figure out a way to test functionality with
Docker containers.

In order to run the test suite, run ``tox`` in the project root directory. The continuous
integration build also bulds the documentation (``tox -e docs``) and performs a distribution build
(``tox -e dist``). See shippable.yml for the exact commands.

When tests pass, fork `<https://bitbucket.org/mapflat/stuffer>`_, push your code to the fork and create a pull request.


Build and release
-----------------

Continuous integration builds are run with `Shippable
<https://app.shippable.com/bitbucket/mapflat/stuffer>`_. Shippable builds a release package for
every merge or push to master branch and uploads it to `<https://pypi.python.org>`_. In order to
make a new release, you must update the version number in setup.py before merging to master.


Deployment
----------

In order to create an installable distribution package, run ``./setup.py sdist`` from the project root directory.
Install with ``pip3 install dist/stuffer-*.tar.gz``.

