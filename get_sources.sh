#!/bin/sh

NAME=brcm80211

git clone -q git://github.com/elemc/brcm80211.git
# Remove .git
rm -rf ${NAME}/.git

# make tarboll
tar cfjv ${NAME}.tar.bz2 $NAME > /dev/null 2>&1

# remove dir
rm -rf ${NAME}