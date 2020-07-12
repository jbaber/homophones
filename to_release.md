Python's entire packaging system is notoriously splintered and hard to find
clear explanations of.  I find it much more difficult to package code than
to write it.

Here's how I release this code to pypi:

First, have a $HOME/.pypirc with no password in it, just nothing after the :

    cat $HOME/.pypirc

    [distutils]
    index-servers =
        pypi

    [pypi]
    username:jbaber
    password:


First, be in a virtualenv

    python3 -m venv env
    source env/bin/activate

Only the first time

    python setup.py register

then

    python setup.py sdist
    python setup.py sdist upload
