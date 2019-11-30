#!/bin/bash
cd app
nosetests #--with-coverage --cover-package=app
# coverage report --fail-under=20