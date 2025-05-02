#!/usr/bin/env bash

echo "Install shell scripts"
mkdir -p ~/.local/bin
cp shell_scripts/* -r ~/.local/bin/

echo "Install python scripts"
cp python_scripts/* -r ~/.local/bin/
