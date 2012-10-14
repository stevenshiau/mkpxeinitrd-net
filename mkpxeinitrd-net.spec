%define BUSYBOX_VERSION 1.20.2
%define _libdir /usr/lib/
Summary: PXE Network-booting initrd builder
Name: mkpxeinitrd-net
Version: 2.0.7
Release: drbl1
Source0: %{name}-%{version}.tar.bz2
Source1: http://www.busybox.net/downloads/busybox-%{BUSYBOX_VERSION}.tar.bz2

License: GPL
Group: System/Kernel and hardware
URL: http://www.fensystems.co.uk/SRPMS.fensys
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
Requires: coreutils, pciutils, module-init-tools, procps, drbl >= 2.1.13
Obsoletes: mkinitrd-net
ExclusiveArch: %{ix86}, x86_64

%description
mkpxeinitrd-net is a derived program from mkinitrd-net.
mkpxeinitrd-net allows you to build initial ramdisk images (initrds) suitable for use with PXE and Etherboot (Using PXE compatable mode) network-booting software.  This package contains one main utility: mkpxeinitrd-net (to build an initrd containing a specified set of network-card modules).

mkpxeinitrd-net uses code from busybox projects.

%prep
%setup -q -n %{name}-%{version}/initrd -a1

%build
# Ugly jobs. Should use patch file for these. This is for gcc (GCC) 3.2.2 20030222.
# From Busybox 1.10.1, the compiling switch for static linking with gcc will be automatically set by scripts/trylink from busybox. Therefore comment these 3:
#perl -pi -e "s/-Wl,--gc-sections//g" busybox-%{BUSYBOX_VERSION}/scripts/trylink
#perl -pi -e "s/-Wl,--sort-section -Wl,alignment//g" busybox-%{BUSYBOX_VERSION}/scripts/trylink
#perl -pi -e "s/^#error Aborting compilation.*//g" busybox-%{BUSYBOX_VERSION}/applets/applets.c
make -j4

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/mkpxeinitrd-net
%{_bindir}/parse-net-mod
%{_bindir}/parse-nfs-mod

#
%{_libdir}/mkpxeinitrd-net
%doc README
%doc AUTHORS.busybox LICENSE.busybox COPYING CHANGES

%changelog
* Sun Oct 14 2012 Steven Shiau <steven _at_ nchc org tw> 2.0.7-drbl1
- Bug fixed: For Linux kernel 3.6, the required modules for NFS are not only nfs.ko, yet more modules are required, e.g. nfsv2.ko, nfsv3.ko, nfsv4.ko...

* Fri Oct 12 2012 Steven Shiau <steven _at_ nchc org tw> 2.0.6-drbl1
- Bug fixed: /run should be umounted before exiting initrd.

* Sat Aug 25 2012 Steven Shiau <steven _at_ nchc org tw> 2.0.5-drbl1
- Bug fixed: $initrd/dev should be created before node files are made.

* Sat Aug 25 2012 Steven Shiau <steven _at_ nchc org tw> 2.0.4-drbl1
- Do not create the empty dir /proc and /dev in Makefile.
- Updating debian/control. Wrong home page was corrected.
- File debian/watch was added.

* Sun Aug 12 2012 Steven Shiau <steven _at_ nchc org tw> 2.0.3-drbl1
- Using /usr/share/drbl instead of /usr/share/drbl/ so that no "//" in the PATH.

* Wed Aug 08 2012 Steven Shiau <steven _at_ nchc org tw> 2.0.2-drbl1
- Source format 3.0 was added in dir debian.

* Wed Aug 08 2012 Steven Shiau <steven _at_ nchc org tw> 2.0.1-drbl1
- Depends on drbl.
- Program mkpxeinitrd-net will only read /etc/drbl/drbl.conf if it exists. 

* Tue Aug 07 2012 Steven Shiau <steven _at_ nchc org tw> 2.0.0-drbl1
- Mkpxeinitrd-net version 2. New files arch so it's easier to be packaged in Debian.
- New upstream busybox 1.20.2.
- Replacing drbl.nchc.org.tw with drbl.org in the prompt messages.

* Wed Dec 14 2011 Steven Shiau <steven _at_ nchc org tw> 1.6.12-1drbl
- Bug fixed: "mount --move -n /run /sysroot/run" insetad of "mount -n -o move /run /sysroot/run" in linuxrc-or-init.
- New upstream busybox 1.19.3.

* Tue Oct 25 2011 Steven Shiau <steven _at_ nchc org tw> 1.6.11-1drbl
- Usage function in mkpxeinitrd-net was updated. More info will be shown.
- Udev hooks file was updated for the requirement of Ubuntu 11.10. Some more files need to be copied in hooks.

* Tue Sep 20 2011 Steven Shiau <steven _at_ nchc org tw> 1.6.10-1drbl
- The dir /lib64 will only be searched in mkpxeinitrd-net when it exists.

* Tue Sep 20 2011 Steven Shiau <steven _at_ nchc org tw> 1.6.9-1drbl
- To compiled in CentOS 5 (kernel 2.6.18), the UBI utils in misc were disabled, since it's useless for PXE client's initrd.

* Sun Sep 18 2011 Steven Shiau <steven _at_ nchc org tw> 1.6.8-2drbl
- Force to define the ${_libdir} as /usr/lib/.

* Fri Sep 09 2011 Steven Shiau <steven _at_ nchc org tw> 1.6.8-1drbl
- Bug fixed: mkpxeinitrd-net failed to copy files to sub dir for libnss_files* for x86-64 GNU/linux.
- New upstream busybox 1.19.2.

* Fri Aug 12 2011 Steven Shiau <steven _at_ nchc org tw> 1.6.7-1drbl
- Two more flags were implemented: use_run_in_initrd and use_dev_pts_in_initrd. This allows to decide if /run and /dev/pts should be mounted in initramfs.

* Mon Aug 08 2011 Steven Shiau <steven _at_ nchc org tw> 1.6.6-1drbl
- Add mounting /dev/pts in linuxrc-or-init

* Fri Aug 05 2011 Steven Shiau <steven _at_ nchc org tw> 1.6.5-1drbl
- The hook file "udev" was updated for more files to be included in /lib/udev/.
- The dir /run will be created so that udevd can work.

* Thu Aug 04 2011 Steven Shiau <steven _at_ nchc org tw> 1.6.4-1drbl
- Support linux kernel 3.
- New upstream busybox 1.18.5.

* Sun May 01 2011 Steven Shiau <steven _at_ nchc org tw> 1.6.3-1drbl
- By default in mkpxeinitrd-net we switch to not including all firmwares in initrd, because what "modinfo -F firmwares" should be trusted.

* Mon Apr 11 2011 Steven Shiau <steven _at_ nchc org tw> 1.6.2-1drbl
- Bug fixed: mkpxeinitrd-net failed to copy files to sub dir for libnss_files*.

* Mon Apr 11 2011 Steven Shiau <steven _at_ nchc org tw> 1.6.1-1drbl
- No more using mount from busybox, we use the one from distribution system. This is specially for mount.nfs.
- The NFS client options were changed: "rsize=65536,wsize=65536" for NFS clients was removed. Let mount and kernel decide that. "nfsvers=3" was added.

* Wed Mar 30 2011 Steven Shiau <steven _at_ nchc org tw> 1.5-12
- New upstream busybox 1.18.4.

* Tue Feb 16 2011 Steven Shiau <steven _at_ nchc org tw> 1.5-11
- New upstream busybox 1.18.3.

* Tue Oct 26 2010 Steven Shiau <steven _at_ nchc org tw> 1.5-10
- New upstream busybox 1.17.3.

* Fri Sep 17 2010 Steven Shiau <steven _at_ nchc org tw> 1.5-9
- A better method to find USB related files was added. 
- New upstream busybox 1.17.2.

* Wed Aug 11 2010 Steven Shiau <steven _at_ nchc org tw> 1.5-8
- New upstream busybox 1.17.1.

* Tue Jun 15 2010 Steven Shiau <steven _at_ nchc org tw> 1.5-7
- Bug fixed: udevd should not be started if daemon mode is not supported. This should fix an issue on CentOS/RHEL 4.
- New upstream busybox 1.16.2.

* Wed Jun 09 2010 Steven Shiau <steven _at_ nchc org tw> 1.5-6
- Bug fixed: modprobe from Mandriva uses compressed kernel module, it's not the case we used before (modprobe was from busybox). 

* Wed Jun 09 2010 Steven Shiau <steven _at_ nchc org tw> 1.5-5
- Minor improvement was done in linuxrc-or-init.

* Wed Jun 09 2010 Steven Shiau <steven _at_ nchc org tw> 1.5-4
- Program mkpxeinitrd-net was improved to skip non-existing /lib/udev/*firmware* files in initrd.
- A workaround to fix an udevd issue (http://sourceforge.net/projects/drbl/forums/forum/394007/topic/3729074) in CentOS 5.5. was implemented.

* Fri Apr 16 2010 Steven Shiau <steven _at_ nchc org tw> 1.5-3
- Bug fixed: Failed to scan some of the PCI device for OpenSuSE 10.3.

* Thu Apr 08 2010 Steven Shiau <steven _at_ nchc org tw> 1.5-2
- Bug fixed: drbl.conf should be loaded.

* Thu Apr 08 2010 Steven Shiau <steven _at_ nchc org tw> 1.5-1
- Do not use the function from drbl package. The function should be in this mkpxeinitrd-net package. 
- Improvement: Program /lib/udev/firmware should be copied for Ubuntu 10.04.

* Sat Apr 03 2010 Steven Shiau <steven _at_ nchc org tw> 1.4-4
- Only the specific version of kernel firmware in /lib/firmware/ will be put in the initrd.
- More improvements about udev hooks. Some more required files should be copied.
- More USB hid modules will be copied in initramfs of client.
- New upstream busybox 1.16.1.

* Fri Mar 12 2010 Steven Shiau <steven _at_ nchc org tw> 1.4-3
- Bug fixed: kernel/drivers/hid/usbhid* was not copied to initrd.

* Thu Mar 11 2010 Steven Shiau <steven _at_ nchc org tw> 1.4-2
- RPM spec file was updated. No more mknbi related command.
- A dir name was added when creating the tarball.

* Thu Mar 11 2010 Steven Shiau <steven _at_ nchc org tw> 1.4-1
- Program lspci-satic was removed, we will copy it from the server.
- Data file pci.ids was updated.

* Thu Mar 11 2010 Steven Shiau <steven _at_ nchc org tw> 1.3-19
- Use copy_exec_drbl to include packages insmod, modprobe, rmmod and lsmod. No more using them from busybox.
- kernel/drivers/hid/usbhid was added in the USB releaded modules.
- Udev daemon should be started to make firmware loading work.

* Tue Dec 15 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-18
- Remove applets sleep and usleep in busybox. We will use the one from system.
- The timeout mechanism to detect multiple NICs' link statuses was rewritten.

* Tue Dec 15 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-17

* Tue Dec 15 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-16
- Bug fixed: usleep was not linked to busybox.

* Tue Dec 15 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-15
- New upstream busybox 1.15.3.
- Turn on usleep command in busybox.

* Wed Dec 09 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-14
- Bug fixed: For Ubuntu 9.04, we need to copy some network drivers in /lib/modules/$KVER/kernel/ubuntu/ to initrd-pxe.img.

* Sat Nov 28 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-13
- Program modules.pcimap will be copied only when it exists.

* Fri Nov 20 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-12
- In hooks/udev, we test if /sbin/udevadm exists then copy.

* Wed Oct 21 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-11
- usplash options were updated in linuxrc-or-init.
- Bug fixed: test if /sbin/usplash and /sbin/usplash_write exists before copy_exe_drbl them.

* Mon Oct 19 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-10
- To make it more general, usplash options were updated in linuxrc-or-init.

* Mon Oct 19 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-9
- Some required devices for usplash will be created in init.
- mkpxeinitrd-net will include usplash by default if it exists in the system.
- New upstream busybox 1.15.2.

* Thu Sep 24 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-8
- Bug fixed: firmware.sh was not copied in some cases.

* Thu Sep 24 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-7
- Bug fixed: The copy_exec function only links the files, and when running mkpxeinitrd-net, cpio is not run with "--dereference" option. This causes the udev related files in the created PXE initramfs useless.

* Mon Sep 21 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-6
- An option to include wireless modules in created initrd was added. By default now we won't include wireless modules.
- New upstream busybox 1.15.1.

* Wed Aug 26 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-5
- Bug fixed: firmwares were copied to wrong path in the initramfs.

* Wed Aug 26 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-4
- Bug fixed: The firmware to be included should come from client's common root path (i.e. /tftpboot/node_root/lib/firmware/, not from /lib/firmware/).

* Wed Aug 26 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-3
- Some verbose messages about firmware will only be shown when verbose option is on.

* Tue Aug 25 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-2
- File hooks/udev was updated to make it more general (e.g. work with Debian lenny).

* Tue Aug 25 2009 Steven Shiau <steven _at_ nchc org tw> 1.3-1
- Does not exclude wireless drivers.
- Required firmware of network drivers will be included if it exists on the system.

* Sun Aug 09 2009 Steven Shiau <steven _at_ nchc org tw> 1.2-44
- New upstream busybox 1.14.3.

* Tue Jun 23 2009 Steven Shiau <steven _at_ nchc org tw> 1.2-43
- New upstream busybox 1.14.2.
- Applet "wc" was turned on.
- We only sleep 3 if there are more than one NIC, since if only one, we do not care about the priority

* Sun May 31 2009 Steven Shiau <steven _at_ nchc org tw> 1.2-42
- New upstream busybox 1.14.1.

* Wed May 20 2009 Steven Shiau <steven _at_ nchc org tw> 1.2-41
- Bug fixed: "-Ew" of grub should not be used in linuxrc-or-init since it's not supported in the busybox we compiled.
- Variable iretry_max was changed to be "5" (was 10), we do not want this too long.
- "sleep 3" was added after network card is up, so we can detect the link status.

* Wed Apr 22 2009 Steven Shiau <steven _at_ nchc org tw> 1.2-40
- Variable iretry_max was changed to be "10" (was 3) since now we can detect the linked NIC and with some network switch, udhclient need to request more times.
- New upstream busybox 1.13.4.

* Sun Apr 12 2009 Steven Shiau <steven _at_ nchc org tw> 1.2-39
- New upstream busybox 1.13.3.

* Thu Apr 09 2009 Steven Shiau <steven _at_ nchc org tw> 1.2-38
- Bug fixed: parse-nfs-mod and parse-net-mod failed to deal with newer kernel modules.dep (e.g. that of Ubuntu 9.04). Thanks to oferchen at users.sourceforge.net for this bug report.

* Thu Mar 12 2009 Steven Shiau <steven _at_ nchc org tw> 1.2-37
- Bug fixed: linked network card was not correctly detected.

* Thu Jan 29 2009 Steven Shiau <steven _at_ nchc org tw> 1.2-36
- New upstream busybox 1.13.2.

* Wed Oct 15 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-35
- New upstream busybox 1.12.1.

* Mon Sep 22 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-34
- Bug fixed: if no files in /lib/modules/$KVER/extra, skip copying files.

* Thu Sep 04 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-33
- Bug fixed: suppress the unalias ls message in get-nic-devs.

* Thu Sep 04 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-32
- Put the linked NICs in the higher priority to request IP address.

* Tue Sep 02 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-31
- mkpxeinitrd-net was updated since Lenny puts extra modules in /lib/modules/kernel/$KER_VER/extra/ 
- New upstream busybox 1.11.2.

* Fri Aug 15 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-30
- busybox-1.11.1.config was updated with some minor features added.
- head is linked for busybox.

* Wed Aug 06 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-29
- New upstream busybox 1.11.1.

* Mon Jun 16 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-28
- New upstream busybox 1.10.3.

* Sun Apr 27 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-27
- More prompt was added in linuxrc-or-init.

* Sun Apr 27 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-26
- An option for udhcpc port was listed in linuxrc.conf.
- linuxrc-or-init honors udhdpc_port in linuxrc.conf.

* Sun Apr 27 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-25
- Static linking option can be automatically detected in busybox 1.10.1 or later. so comment those manual modification in rpm spec file.

* Sat Apr 26 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-24
- Turn on CONFIG_FEATURE_UDHCP_PORT in Busybox.

* Sat Apr 26 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-23
- New upstream busybox 1.10.1.
- Add entry /bin/bash when failing to mount root dir so that it's easier to debug.

* Fri Mar 28 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-22
- New upstream busybox 1.9.2.

* Mon Feb 18 2008 Steven Shiau <steven _at_ nchc org tw> 1.2-21
- New upstream busybox 1.9.1.

* Wed Dec 12 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-20
- Updated for Ubuntu 7.10, since extra network drivers are located in dir like: /lib/modules/2.6.22-14-generic/ubuntu/net.

* Thu Nov 22 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-19
- Bug fixed: Ugly patches in spec should be done in busybox-%{BUSYBOX_VERSION}/scripts/trylink instead of busybox-%{BUSYBOX_VERSION}/Makefile.

* Thu Nov 22 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-18
- New upstream busybox 1.8.1.

* Sun Oct 27 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-17
- new upstream busybox 1.7.2.

* Fri Sep 21 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-16
- new upstream busybox 1.7.1.

* Sun Sep 16 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-15
- use --clientid-none --vendorclass="$vendor_class_id" with udhcpc. This parameters can let DHCP server know the request is from DRBL client.

* Sun Sep 16 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-14
- use drbl.sourceforge.net instead of drbl.nchc.org.tw in the prompt.

* Wed Aug 29 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-13
- turn on mountpoint from busybox.

* Tue Aug 21 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-12
- bug fixed for mkpxeinitrd-net.

* Tue Aug 21 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-11
- new upstream busybox 1.6.1

* Sun Jun 17 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-10
- show more messages when sleeping after NIC is up.

* Sun Jun 17 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-9
- use dhcp_server_name in udhcpc-post.

* Sun Jun 17 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-8
- update prompt.

* Sun Jun 17 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-7
- add prompt about dhcp server name.

* Sun Jun 17 2007 Steven Shiau <steven _at_ nchc org tw> 1.2-6
- add an variable dhcp_server_name in linuxrc.conf, so that it's easier to use another existing dhcp server. Ref: http://sourceforge.net/forum/forum.php?thread_id=1753834&forum_id=394008

* Tue Dec 19 2006 Steven Shiau <steven _at_ nchc org tw> 1.2-5
- Remounting dev at correct place in linuxrc-or-init both for initramfs and initrd, Uuse "mount --move -n /dev/ /sysroot/dev" instead of "mount -t tmpfs -n -o bind /dev/ /sysroot/dev"
- add nr_inodes=24576 (mount -t tmpfs -n -o nr_inodes=24576,mode=0755 none /dev).

* Fri Dec 16 2006 Steven Shiau <steven _at_ nchc org tw> 1.2-4
- remove unnecessary pause in linuxrc-or-init.

* Thu Dec 14 2006 Steven Shiau <steven _at_ nchc org tw> 1.2-3
- change linuxrc to linuxrc or init in echos.

* Mon Dec 11 2006 Steven Shiau <steven _at_ nchc org tw> 1.2-2
- add comments in linuxrc-or-init.
- add CHANGES

* Mon Dec 11 2006 Steven Shiau <steven _at_ nchc org tw> 1.2-1
- delete the extra line for %.tar.gz ([ -f $*.t*gz ] && ( gunzip $*.t*gz ; bzip2 -9 $*.tar ) || true) in Makefile.
- /bin/switch_root is linked.
- mkpxeinitrd-net supports initramfs now.
- rename linuxrc as linuxrc-or-init, we will use mkpxeinitrd-net to rename it as linuxrc for initrd or init for initramfs.

* Fri Oct 27 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-26
- test before modprobe af_packet, and add more notes about af_packet.
- remove README.DRBL.

* Thu Oct 26 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-25
- if module of NIC is not found, show error message and enter shell to debug (insert-modules)

* Thu Oct 26 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-24
- buggy busybox 1.2.2, diskless client is not able to find the NIC module. Back to use busybox 1.2.1.

* Thu Oct 26 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-23
- new upstream busybox 1.2.2

* Sun Oct 22 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-22
- increase the rsize and wsize to 65536 (was 8192) for NFS client parameters (udhcpc-post).

* Sun Oct 08 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-21
- comment some unnecessary codes in mkpxeinitrd-net.

* Thu Oct 04 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-20
- bug fixed: kernel/net/packet should be copied to initrd for Debian based.

* Thu Oct 04 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-19
- bug fixed: parse-nfs-mod is not installed in rpm/deb.

* Wed Oct 03 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-18
- add parse-nfs-mod.
- update mkpxeinitrd-net to work with newer nfs.ko in 2.6.17-2.6.18 (now it need fscache.ko), add we use parse-nfs-mod to get that.

* Wed Sep 20 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-17
- change #!/bin/sh to #!/bin/bash in mkpxeinitrd-net.

* Fri Sep 15 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-16
- new upstream busybox 1.2.1

* Thu Jul 27 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-15
- sign the rpm with gpg.

* Sat Jul 01 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-14
- new upstream busybox 1.2.0

* Fri May 19 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-13
- new upstream busybox 1.1.3

* Tue Apr 11 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-11
- new upstream busybox 1.1.2

* Fri Apr 7 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-10
- update the prompt when loading modules.

* Fri Apr 7 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-9
- add an option -nu|--no-usb-modules to exclude USB keyboard related modules.

* Tue Mar 28 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-8
- downgrade busybox 1.1.1 to 1.1.0, since failed to mount nfs root.

* Tue Mar 28 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-7
- new upstream busybox 1.1.1

* Mon Mar 27 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-6
- The mode of files in /usr/lib/mkpxeinitrd-net/initrd-skel/etc should be 644.
- Add usbcore.ko in initrd.

* Thu Mar 16 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-5
- add necessary usb modules for usb keyboard to make it work in initrd.

* Mon Mar 13 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-4
- remove some unnecessary lines in initrd/udhcpc-post.

* Sun Mar 12 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-3
- use node_root for sysroot, not $IP now. Therefore we do not have to link /tftpboot/node_root to $IP
- it should be ro, not rw for NFS option.

* Mon Mar 06 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-2
- update notes in udhcpc-post.
- DRBL SSI is ready.

* Thu Mar 02 2006 Steven Shiau <steven _at_ nchc org tw> 1.1-1
- add drbl single system image support. (Not ready yet)

* Sat Feb 18 2006 Steven Shiau <steven _at_ nchc org tw> 1.0-9
- add an option to set the pause time (secs) after network card is up. This is specially for some switch which need extra time to link, check https://sourceforge.net/forum/message.php?msg_id=3583499 for more details.

* Sat Feb 11 2006 Steven Shiau <steven _at_ nchc org tw> 1.0-8
- refine some codes.

* Fri Feb 10 2006 Steven Shiau <steven _at_ nchc org tw> 1.0-7
- do not show error messages when loading modules in linuxrc.

* Fri Feb 10 2006 Steven Shiau <steven _at_ nchc org tw> 1.0-6
- We will try to find the NIC module from (1) the hwdata pcitable and (2) the table from kernel, if both are found with different modules, we will use both.

* Sat Feb 04 2006 Steven Shiau <steven _at_ nchc org tw> 1.0-5
- turn off gettty applet since it's useless.

* Thu Feb 02 2006 Steven Shiau <steven _at_ nchc org tw> 1.0-4
- turn on gettty applet.

* Wed Feb 01 2006 Steven Shiau <steven _at_ nchc org tw> 1.0-3
- turn on more applets for busybox 1.1.0

* Wed Feb 01 2006 Steven Shiau <steven _at_ nchc org tw> 1.0-2
- update with busybox 1.1.0

* Sat Oct 28 2005 Steven Shiau <steven _at_ nchc org tw> 1.0-1
- rename the program as mkpxeinitrd-net, no more mkinitrd-net, to avoid confusion.
