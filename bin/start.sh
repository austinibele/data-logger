#!/usr/bin/env bash

set -e

SCRIPT="$(realpath -s $0)"
SCRIPTDIR="$(dirname $SCRIPT)"
cd "$SCRIPTDIR"

exec python3.9 ../main.py
