#!/bin/sh

NAME=brcm80211
COMMIT="6b1933abb0546867fc35"

git clone -q git://github.com/elemc/brcm80211.git

pushd ${NAME} > /dev/null 2>&1
git checkout -qf $COMMIT
popd > /dev/null 2>&1

# Remove .git
rm -rf ${NAME}/.git

# make tarboll
tar cfjv ${NAME}.tar.bz2 $NAME > /dev/null 2>&1

# remove dir
rm -rf ${NAME}