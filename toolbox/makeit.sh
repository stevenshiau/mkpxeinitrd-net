#!/bin/sh -x
set -e
rm -rf debforge RPMS.drbl-test
./packit.sh
./make-rpm.sh
./make-deb.sh
echo "Do not forgot to pack amd64 version by running make-it.sh on amd64 machine (For RPM, it must be on old OS, e.g. CentOS 5 x86_64, not on Debian Squeeze amd64.)."
