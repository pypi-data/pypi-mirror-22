@echo off

rem make source distribution and upload the package
python setup.py register sdist --formats=gztar upload
