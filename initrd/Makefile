BUSYBOX_VERSION = 1.36.1
BUSYBOX = busybox-$(BUSYBOX_VERSION)
$(BUSYBOX)_SOURCE = http://www.busybox.net/downloads/$(BUSYBOX).tar.bz2
SHELL := /bin/bash
MP_OPT = -j 6

all : utils initrd-skel

%.tar.bz2 :
	[ -d $* ] || wget $($*_SOURCE)
	[ -f $*.t*gz ] && ( gunzip $*.t*gz ; bzip2 -9 $*.tar ) || true

%.tar.gz :
	[ -d $* ] || wget $($*_SOURCE)

UTILS = busybox

utils : $(UTILS)

clean : partlyclean

partlyclean :
	rm -rf $(BUSYBOX)
	rm -rf initrd-skel
	rm -f *.img
	rm -f $(UTILS)

.PHONY : all utils clean partlyclean

busybox : $(BUSYBOX)
	install -m 755 -s $(BUSYBOX)/$@ $@

$(BUSYBOX) : $(BUSYBOX).tar.bz2
	[ -d $@ ] || tar xvjf $<
	install -m 644 config.busybox/$(BUSYBOX).config $(BUSYBOX)/.config
	$(MAKE) $(MP_OPT) -C $(BUSYBOX)
	install -m 644 $(BUSYBOX)/AUTHORS AUTHORS.busybox
	install -m 644 $(BUSYBOX)/LICENSE LICENSE.busybox

initrd-skel : $(UTILS) linuxrc-or-init udhcpc-post
	rm -rf $@
	mkdir -p $@
	mkdir -p $@/etc
	mkdir -p $@/usr/bin
	mkdir -p $@/usr/lib
	mkdir -p $@/usr/lib64
	ln -s -t $@ usr/bin
	ln -s -t $@ usr/sbin
	ln -s -t $@ usr/lib
	ln -s -t $@ usr/lib64
	(cd $@/usr/; ln -s bin sbin)
	install -m 755 busybox scan_pci ls_pciid.sh get-nic-devs insert-modules $@/usr/bin/
	install -m 644 pcitable pci.ids linuxrc.conf netdev.conf modules $@/etc/
	ln -s busybox $@/usr/bin/sh
	ln -s busybox $@/usr/bin/echo
	ln -s busybox $@/usr/bin/mknod
	ln -s busybox $@/usr/bin/chmod
	ln -s busybox $@/usr/bin/ifconfig
	ln -s busybox $@/usr/bin/route
	#ln -s busybox $@/usr/bin/mount
	ln -s busybox $@/usr/bin/pivot_root
	#ln -s busybox $@/usr/bin/umount
	ln -s busybox $@/usr/bin/[
	ln -s busybox $@/usr/bin/grep
	ln -s busybox $@/usr/bin/sed
	ln -s busybox $@/usr/bin/cat
	ln -s busybox $@/usr/bin/cut
	ln -s busybox $@/usr/bin/sort
	ln -s busybox $@/usr/bin/head
	ln -s busybox $@/usr/bin/uniq
	#ln -s busybox $@/usr/bin/insmod
	#ln -s busybox $@/usr/bin/modprobe
	#ln -s busybox $@/usr/bin/rmmod
	#ln -s busybox $@/usr/bin/lsmod
	ln -s busybox $@/usr/bin/ping
	ln -s busybox $@/usr/bin/df
	ln -s busybox $@/usr/bin/id
	ln -s busybox $@/usr/bin/more
	ln -s busybox $@/usr/bin/ln
	ln -s busybox $@/usr/bin/ls
	ln -s busybox $@/usr/bin/gunzip
	ln -s busybox $@/usr/bin/uname
	ln -s busybox $@/usr/bin/tr
	ln -s busybox $@/usr/bin/mkdir
	ln -s busybox $@/usr/bin/rm
	# busybox 1.0 has udhcpc
	ln -s busybox $@/usr/bin/udhcpc
	ln -s busybox $@/usr/bin/switch_root
	ln -s busybox $@/usr/bin/mountpoint
	ln -s busybox $@/usr/bin/wc
	ln -s busybox $@/usr/bin/ps
	ln -s busybox $@/usr/bin/xargs

	install -m 755 linuxrc-or-init $@/linuxrc-or-init
	install -m 755 udhcpc-post $@/usr/bin/udhcpc-post
	cd $@/etc; ln -s ../dev/resolv.conf resolv.conf

tftpboot/initrd-%.img : initrd-skel
	./mkpxeinitrd-net -l `echo $* | tr . " "`

prefix = $(DESTDIR)/usr
sysconfdir = /etc
bindir = $(prefix)/bin
libdir = $(prefix)/lib
mandir = $(prefix)/share/man
docdir = $(prefix)/share/doc
initrdskeldir = $(libdir)/mkpxeinitrd-net/initrd-skel
hooksdir = $(libdir)/mkpxeinitrd-net/hooks

install :
	mkdir -p $(bindir)
	mkdir -p $(docdir)
	mkdir -p $(sysconfdir)
	mkdir -p $(initrdskeldir)
	mkdir -p $(hooksdir)
	mkdir -p $(libdir)/mkpxeinitrd-net/bin/
	install -m 755 \
	        mkpxeinitrd-net $(bindir)/
	install -m 755 \
	        mkpxeinitrd-net-func parse-net-mod parse-nfs-mod $(libdir)/mkpxeinitrd-net/bin/
	cp -a initrd-skel/* $(initrdskeldir)/
	cp -a hooks/* $(hooksdir)/
