#!/bin/bash
pushd Source

rm -rf  build
rm -rf  dist
rm -rf  xml-preferences.egg-info

python3 ../setup.py sdist bdist_wheel "$@"

popd
ls -1 Source/dist/*.whl
