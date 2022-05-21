BUSYBOX_VERSION = 1.35.0
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
	mkdir -p $@/bin
	ln -s bin $@/sbin
	install -m 755 busybox scan_pci ls_pciid.sh get-nic-devs insert-modules $@/bin/
	install -m 644 pcitable pci.ids linuxrc.conf netdev.conf modules $@/etc/
	ln -s busybox $@/bin/sh
	ln -s busybox $@/bin/echo
	ln -s busybox $@/bin/mknod
	ln -s busybox $@/bin/chmod
	ln -s busybox $@/bin/ifconfig
	ln -s busybox $@/bin/route
	#ln -s busybox $@/bin/mount
	ln -s busybox $@/bin/pivot_root
	#ln -s busybox $@/bin/umount
	ln -s busybox $@/bin/[
	ln -s busybox $@/bin/grep
	ln -s busybox $@/bin/sed
	ln -s busybox $@/bin/cat
	ln -s busybox $@/bin/cut
	ln -s busybox $@/bin/sort
	ln -s busybox $@/bin/head
	ln -s busybox $@/bin/uniq
	#ln -s busybox $@/bin/insmod
	#ln -s busybox $@/bin/modprobe
	#ln -s busybox $@/bin/rmmod
	#ln -s busybox $@/bin/lsmod
	ln -s busybox $@/bin/ping
	ln -s busybox $@/bin/df
	ln -s busybox $@/bin/id
	ln -s busybox $@/bin/more
	ln -s busybox $@/bin/ln
	ln -s busybox $@/bin/ls
	ln -s busybox $@/bin/gunzip
	ln -s busybox $@/bin/uname
	ln -s busybox $@/bin/tr
	ln -s busybox $@/bin/mkdir
	ln -s busybox $@/bin/rm
	# busybox 1.0 has udhcpc
	ln -s busybox $@/bin/udhcpc
	ln -s busybox $@/bin/switch_root
	ln -s busybox $@/bin/mountpoint
	ln -s busybox $@/bin/wc
	ln -s busybox $@/bin/ps
	ln -s busybox $@/bin/xargs

	install -m 755 linuxrc-or-init $@/linuxrc-or-init
	install -m 755 udhcpc-post $@/bin/udhcpc-post
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
