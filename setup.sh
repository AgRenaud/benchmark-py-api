#!/bin/bash

function setup_filesystem {
    APP_NAME=$1

    printf "[INFO] Make dir /opt/src/$APP_NAME\n"
    mkdir -p /opt/src/$APP_NAME
    
    printf "[INFO] Make dir /opt/venv/$APP_NAME\n"
    mkdir -p /opt/venv/$APP_NAME

}

function validation {
    while true; do
        read -p "Do you wish to install this program? (y/n) " yn
        case $yn in
            [Yy]* ) break;;
            [Nn]* ) exit;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

function check_parameters {
    APP_NAME=$1

    if [ -z "$APP_NAME" ]; then
        printf "Missing parameter: APP_NAME\n"
        exit 1
    fi
}

function main {
    check_parameters $@

    APP_NAME=$1

    printf "You're going to setup directories for $APP_NAME\n"
    validation
    setup_filesystem $1
    exit 0
}

main $@
