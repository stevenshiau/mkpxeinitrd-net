#!/bin/bash
# Steven Shiau <steven _at_ nchc org tw)
set -e
#
PKG="mkpxeinitrd-net"
SPEC_FILE="$PKG.spec"

#
[ ! -f "$SPEC_FILE" ] && echo "Can NOT find spec file $SPEC_FILE" && exit 1

#
VER=`grep ^Version $SPEC_FILE |sed -e "s/\t/ /g" -e "s/ \+/ /g" |cut  -d":" -f2 |tr -d " "`
echo "VER: $VER"

#
BUSYBOX_VER=`grep "^%define BUSYBOX_VERSION" $SPEC_FILE |sed -e "s/\t/ /g" -e "s/ \+/ /g" |cut  -d" " -f3 |tr -d " "`
echo "BUSYBOX VER: $BUSYBOX_VER"

#
TARBALL=$PKG-$VER.tar.bz2
busybox_pkg="busybox-$BUSYBOX_VER.tar.bz2"

# check
[ ! -f "$TARBALL" ] && echo "Can NOT find file $TARBALL! Did you forget to update the rdate in file clonezilla.spec ? Program Stop!!!" && exit 1

# mkdir for build
rm -rf debforge/*
mkdir -p debforge/
tar -xvjf $TARBALL -C debforge/
[ -e "$busybox_pkg" ] && cp $busybox_pkg debforge/$PKG-$VER/initrd/
cp -a debian debforge/$PKG-$VER/
cd debforge/$PKG-$VER
#dpkg-buildpackage -rfakeroot
debuild --no-tgz-check --no-lintian
