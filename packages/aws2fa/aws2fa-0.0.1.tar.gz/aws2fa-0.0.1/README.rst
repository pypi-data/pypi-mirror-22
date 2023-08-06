aws2fa
=======

``aws2fa`` is a simple command to handle 2fa authentication respecting ``aws-cli`` standard configuration.

Simple usage::

    $ aws2fa [profile]

Features
---------

* ``aws2fa`` respects ``aws-cli`` configuration (``~/.aws/credentials`` and ``~/.aws/config``) no new magic or copies of your credentials
* Full support with ``aws-cli`` profiles
* Smooth device handling
* Super minimal implementation


Contribute
-----------

* Fork the repository on GitHub.
* Write a test which shows that the bug was fixed or that the feature works as expected.

  - Use ``tox`` command to run all the tests in all locally available python version.

* Send a pull request and bug the maintainer until it gets merged and published. :).

For more instructions see `TESTING.rst`.


Helpful Links
-------------

* http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
