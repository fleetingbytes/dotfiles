#!/usr/bin/env sh

greeting_file=~/greeting

if [ -e "${greeting_file}" ]; then
    cat "${greeting_file}"
fi
