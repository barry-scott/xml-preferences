#!/bin/bash
rm -rf  build
rm -rf  dist
rm -rf  xml-preferences.egg-info

python3 setup.py sdist bdist_wheel "$@"

ls -1 dist/*.whl
