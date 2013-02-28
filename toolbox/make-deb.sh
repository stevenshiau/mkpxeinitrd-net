#!/bin/bash
# Steven Shiau <steven _at_ nchc org tw)

# Settings
PKG="mkpxeinitrd-net"

set -e
#
VER="$(LC_ALL=C head -n 1 debian/changelog  | grep -i "^${PKG}" | grep -E -o "\(.*\)" | sed -r -e "s/\(//g" -e "s/\)//g" | cut -d"-" -f1)"
[ -z "$VER" ] && echo "No version found in debian/changelog! Program terminated!"
echo "VER: $VER"

#
BUSYBOX_VER="$(LC_ALL=C grep -Ew "^BUSYBOX_VERSION = .*" initrd/Makefile | awk -F"=" '{print $2}' | sed -r -e "s/^[[:space:]]*//g")"
echo "BUSYBOX VER: $BUSYBOX_VER"

#
TARBALL=$PKG-$VER.tar.bz2
TARBALL_ORIG=${PKG}_${VER}.orig.tar.bz2
busybox_pkg="busybox-$BUSYBOX_VER.tar.bz2"

# check
[ ! -f "$TARBALL" ] && echo "Can NOT find file $TARBALL! Program Stop!!!" && exit 1

# mkdir for build
rm -rf debforge
mkdir debforge
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
debuild
rm -f $TARBALL_ORIG
