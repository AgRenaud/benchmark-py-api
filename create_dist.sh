#!/bin/bash

# TODO: Create array of folder to build
apps=...

for app in apps; do
    cd $app
    poetry build-project
    cd ..
done
