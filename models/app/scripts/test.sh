#!/bin/sh -e
set -x

CACHING=false python -m pytest ./app/app
