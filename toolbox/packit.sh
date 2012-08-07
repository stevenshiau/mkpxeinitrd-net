#!/bin/bash
PKG="mkpxeinitrd-net"
RPMBUILD="${HOME}/rpmbuild/"
SPEC_FILE="$PKG.spec"

set -e
#
[ ! -f "$SPEC_FILE" ] && echo "Can NOT find spec file $SPEC_FILE" && exit 1

# Create the changelog file
#
VER=`grep ^Version $SPEC_FILE |sed -e "s/\t/ /g" -e "s/ \+/ /g" |cut  -d":" -f2 |tr -d " "`
echo "VER: $VER"

TARBALL="$PKG-$VER.tar.bz2"
td="$PKG-$VER"
#check if necessary files exist...
[ -f $SPEC_FILE ] || exit 0
[ -f $TARBALL ] && rm -f $TARBALL
# Clean stale files in debian
rm -rf debian/tmp
[ -d "$td" ] && rm -rf $td
mkdir $td
cp -a initrd $SPEC_FILE $td
tar -cjf $TARBALL $td --owner=root --group=root 
[ -d "$td" ] && rm -rf $td
[ -f $TARBALL ] || exit 0
