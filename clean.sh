#!/bin/bash

find ./ -name "*.pyc" | xargs rm
find ./ -name "*~" | xargs rm
find ./ -name "__pycache__" | xargs rm -fr
