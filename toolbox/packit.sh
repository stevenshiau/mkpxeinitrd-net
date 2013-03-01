#!/bin/bash
# generate the ChangeLog.txt and create the tarball

# Settings
PKG="mkpxeinitrd-net"
FILES_DIRS="initrd"

set -e
#
VER="$(LC_ALL=C head -n 1 debian/changelog  | grep -i "^${PKG}" | grep -E -o "\(.*\)" | sed -r -e "s/\(//g" -e "s/\)//g" | cut -d"-" -f1)"
[ -z "$VER" ] && echo "No version found in debian/changelog! Program terminated!"
echo "VER: $VER"

td="${PKG}-${VER}"

#
[ -d "$td" ] && rm -rf $td
mkdir -p $td
# Clean stale files in debian
cp -ar $FILES_DIRS $td/

#echo $VER > $td/doc/VERSION
tar cjf $td.tar.bz2 --owner=root --group=root $td
rm -rf $td
