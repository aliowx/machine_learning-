#!/bin/sh -e

set -x

ruff app/app --fix
isort app/app
black app/app

