commodore
=========

Manage and maintain your user's scripts and tools

Installation
------------

From pypi::

    $ pip install commodore

... or from the project root directory::

    $ python setup.py install

Then run ``commodore`` from the command line to create the required configuration and binary directory, and define your desired editor.

Usage
-----

Create a new script::

    $ commodore create helloworld

Edit your script, including the shebang line::

    #!/usr/bin/env python
    print('Hello world!')

Then run it!::

    $ helloworld 
    Hello world!

List your scripts::

    $ commodore list
    helloworld

Edit an existing script::

    $ commodore edit helloworld

And finally, delete it::

    $ commodore delete helloworld


Use --help/-h to view info on the arguments::

    $ commodore --help
    usage: commodore [-h] {create,list,edit,delete} ...

    positional arguments:
      {create,list,edit,delete}

      optional arguments:
        -h, --help            show this help message and exit

You can manually check the history of created, edited and deleted scripts by navigating
to the commodore binary directory (default ~/.commodore/bin) and using git commands to
see changelogs. Every create, edit and delete will be tracked as a git commit.

Release Notes
-------------

:0.1.1:
    Updated README and notes on usage
:0.1.0:
    commodore create, edit, delete works
:0.0.1:
    Project created
