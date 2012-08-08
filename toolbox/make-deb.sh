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
TARBALL_ORIG=${PKG}_${VER}.orig.tar.bz2
busybox_pkg="busybox-$BUSYBOX_VER.tar.bz2"

# check
[ ! -f "$TARBALL" ] && echo "Can NOT find file $TARBALL! Did you forget to update the rdate in file clonezilla.spec ? Program Stop!!!" && exit 1

# mkdir for build
rm -rf debforge/*
mkdir -p debforge/
(cd debforge; ln -fs ../$TARBALL $TARBALL_ORIG)
tar -xvjf $TARBALL -C debforge/
# With Debian format 3.0, you can not put binary file in a package unless it's assigned by  debian/source/include-binaries.
# The error messages:
# dpkg-source: info: using source format `3.0 (quilt)'
# dpkg-source: info: building mkpxeinitrd-net using existing ./mkpxeinitrd-net_2.0.2.orig.tar.bz2
# dpkg-source: error: cannot represent change to initrd/busybox-1.20.2.tar.bz2: binary file contents changed
# dpkg-source: error: add initrd/busybox-1.20.2.tar.bz2 in debian/source/include-binaries if you want to store the modified binary in the debian tarball
# dpkg-source: error: unrepresentable changes to source
# dpkg-buildpackage: error: dpkg-source -b mkpxeinitrd-net-2.0.2 gave error exit status 2
#
#[ -e "$busybox_pkg" ] && cp $busybox_pkg debforge/$PKG-$VER/initrd/
cp -a debian debforge/$PKG-$VER/
cd debforge/$PKG-$VER
debuild --no-tgz-check --no-lintian
rm -f $TARBALL_ORIG
