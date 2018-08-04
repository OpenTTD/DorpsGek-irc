#!/bin/sh

echo "Running flake8 ..."
flake8 dorpsgek_irc

echo "Running test build for Docker image ..."
docker build --pull --no-cache --force-rm -t dorpsgek/irc:testrun . \
    && docker rmi dorpsgek/irc:testrun
