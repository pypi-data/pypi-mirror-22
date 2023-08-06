#!/bin/bash

export PATH=\
/opt/buildout.python/bin:\
$PATH:

if [[ "$1" = "python-2.7" ]]
then
    python_version=2.7
fi

virtualenv-$python_version .
bin/pip install zc.buildout
bin/zc.buildout bootstrap
bin/buildout
bin/test

