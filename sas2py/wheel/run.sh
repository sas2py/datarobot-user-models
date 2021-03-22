#!/bin/bash
rm -r build
rm -r sas2py_runner.egg*
rm -r dist/*
python setup.py sdist bdist_wheel
pip uninstall --yes sas2py_runner
pip install --user dist/sas2py_runner*.whl
rm -r build
rm -r sas2py_runner.egg*
