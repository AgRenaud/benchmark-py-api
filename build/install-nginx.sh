#!/bin/sh

install_nginx() {
    apt-get install nginx
}

main() {
    install_nginx
}

main
