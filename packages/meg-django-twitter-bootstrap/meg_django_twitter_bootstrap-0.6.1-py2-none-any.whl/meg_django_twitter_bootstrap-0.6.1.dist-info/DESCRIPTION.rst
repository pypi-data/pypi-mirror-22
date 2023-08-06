================
TwitterBootstrap
================

Starter templates for django sites based on twitter bootstrap http://twitter.github.io/bootstrap/

Development files are at  git@git.maithu.com:TwitterBootstrap.git


To release a new version

1. add the following to ~/.pypirc::

    [distutils]
    index-servers =
        maithu

    [maithu]
    username: admin
    password: password
    repository: http://pypi.maithu.com/simple/


2. python setup.py sdist upload -r maithu

