#!/bin/bash
# script to make mkpxeinitrd-net, 
# written by Steven Shiau <steven _at_ nchc org tw>
# 2005/10/29
set -e
#
PKG="mkpxeinitrd-net"
RPMBUILD="${HOME}/rpmbuild/"
SPEC_FILE="$PKG.spec"
BUSYBOX_URL="http://www.busybox.net/downloads/"

# Source function library.
#. /etc/rc.d/init.d/functions

#
[ ! -f "$SPEC_FILE" ] && echo "Can NOT find spec file $SPEC_FILE" && exit 1

#
VER=`grep ^Version $SPEC_FILE |sed -e "s/\t/ /g" -e "s/ \+/ /g" |cut  -d":" -f2 |tr -d " "`
RELEASE=`grep ^Release $SPEC_FILE |sed -e "s/\t/ /g" -e "s/ \+/ /g" |cut  -d":" -f2 |tr -d " "`
echo "VER, RELEASE: $VER, $RELEASE"
#
RVER=$VER-$RELEASE
#case `uname -m` in
#  i[356]86) platform=i386;;
#  x86_64)   platform=x86_64;;
#esac

#
BUSYBOX_VER="$(LC_ALL=C grep -Ew "^BUSYBOX_VERSION = .*" initrd/Makefile | awk -F"=" '{print $2}' | sed -r -e "s/^[[:space:]]*//g")"
echo "BUSYBOX VER: $BUSYBOX_VER"

#
TARBALL="$PKG-$VER.tar.xz"

#
busybox_pkg="busybox-$BUSYBOX_VER.tar.bz2"
busybox_cfg="busybox-$BUSYBOX_VER.config"
mkinitrd_net_pkg="$PKG-$VER.tar.xz"

# check if pkg exists
if [ ! -f "$busybox_pkg" ]; then
  wget $BUSYBOX_URL/$busybox_pkg
fi

#
build_prefix="${HOME}/rpmbuild/"

#
[ -d $build_prefix/SOURCES/$PKG-$VER ] && rm -rf $build_prefix/SOURCES/$PKG-$VER

# clearn junk
mkdir -p $build_prefix/SOURCES/$PKG-$VER

cp $busybox_pkg initrd/config.busybox/$busybox_cfg $mkinitrd_net_pkg $build_prefix/SOURCES/$PKG-$VER

rpmbuild -ba $PKG.spec

[ -d RPMS.drbl-test ] && rm -rf RPMS.drbl-test
mkdir RPMS.drbl-test
#cp $mkinitrd_net_pkg $build_prefix/RPMS/$PKG-$RVER.$platform.rpm $build_prefix/SRPMS/$PKG-$RVER.src.rpm RPMS.drbl-test
cp $mkinitrd_net_pkg $build_prefix/RPMS/$PKG-$RVER.*.rpm $build_prefix/SRPMS/$PKG-$RVER.src.rpm RPMS.drbl-test
