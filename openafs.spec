# Openafs Spec $Revision$

%define afsvers 1.6.9
%define pkgvers 1.6.9
# for beta/rc releases make pkgrel 0.<tag>
# for real releases make pkgrel 1 (or more for extra releases)
%define pkgrel 1
%define kmod_name openafs

# Define the location of your init.d directory
%define initdir /etc/rc.d/init.d

# Make sure RPM doesn't complain about installed but non-packaged files.
#define __check_files  %{nil}

Summary: OpenAFS distributed filesystem
Name: openafs
Version: %{pkgvers}
Release: %{pkgrel}%{?dist}
License: IBM Public License
URL: http://www.openafs.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Packager: OpenAFS Gatekeepers <openafs-gatekeepers@openafs.org>
Group: Networking/Filesystems
BuildRequires: %{?kdepend:%{kdepend}, } pam-devel, ncurses-devel, flex, bison
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
BuildRequires: systemd-units
%endif
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 6
BuildRequires: perl-devel
%endif
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: krb5-devel

ExclusiveArch: %{ix86} x86_64 ia64 s390 s390x sparc64 ppc ppc64

#    http://dl.openafs.org/dl/openafs/candidate/%{afsvers}/...
Source0: http://www.openafs.org/dl/openafs/%{afsvers}/openafs-%{afsvers}-src.tar.bz2
Source1: http://www.openafs.org/dl/openafs/%{afsvers}/openafs-%{afsvers}-doc.tar.bz2
%define srcdir openafs-%{afsvers}

Source10: http://www.openafs.org/dl/openafs/%{afsvers}/RELNOTES-%{afsvers}
Source11: http://www.openafs.org/dl/openafs/%{afsvers}/ChangeLog
Source20: http://dl.central.org/dl/cellservdb/CellServDB.2013-01-28

%description
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides common files shared across all the various
OpenAFS packages but are not necessarily tied to a client or server.


##############################################################################
#
# build the userspace side of things if so requested
#
##############################################################################
%package client
Requires: binutils, openafs = %{version}
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
Requires: systemd-units
Requires(post): systemd-units, systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif
Requires: %{name}-kmod >= %{version}
Provides: %{name}-kmod-common = %{version}
Summary: OpenAFS Filesystem Client
Group: Networking/Filesystem

%description client
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides basic client support to mount and manipulate
AFS.

%package server
Requires: openafs = %{version}
Summary: OpenAFS Filesystem Server
Group: Networking/Filesystems
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
Requires: systemd-units
Requires(post): systemd-units, systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif

%description server
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides basic server support to host files in an AFS
Cell.

%package authlibs
Summary: OpenAFS authentication shared libraries
Group: Networking/Filesystems

%description authlibs
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides a shared version of libafsrpc and libafsauthent. 
None of the programs included with OpenAFS currently use these shared 
libraries; however, third-party software that wishes to perform AFS 
authentication may link against them.

%package authlibs-devel
Requires: openafs-authlibs = %{version}-%{release}
Requires: openafs-devel = %{version}-%{release}
Summary: OpenAFS shared library development
Group: Development/Filesystems

%description authlibs-devel
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package includes the static versions of libafsrpc and 
libafsauthent, and symlinks required for building against the dynamic 
libraries.

%package devel
Summary: OpenAFS Development Libraries and Headers
Group: Development/Filesystems
Requires: openafs = %{version}-%{release}

%description devel
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides static development libraries and headers needed
to compile AFS applications.  Note: AFS currently does not provide
shared libraries.

%package docs
Summary: OpenAFS user and administrator documentation
Requires: openafs = %{version}-%{release}
Group: Networking/Filesystems

%description docs
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides HTML documentation for OpenAFS users and system
administrators.

%package kpasswd
Summary: OpenAFS KA kpasswd support
Requires: openafs
Group: Networking/Filesystems

%description kpasswd
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the compatibility symlink for kpasswd, in case
you are using KAserver instead of Krb5.

%package krb5
Summary: OpenAFS programs to use with krb5
Requires: openafs = %{version}
Group: Networking/Filesystems
BuildRequires: krb5-devel

%description krb5
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides compatibility programs so you can use krb5
to authenticate to AFS services, instead of using AFS's homegrown
krb4 lookalike services.


##############################################################################
#
# PREP
#
##############################################################################

%prep
# Install OpenAFS src and doc
%setup -q -b 1 -n %{srcdir}

##############################################################################
#
# building
#
##############################################################################
%build
kv='26'
case %{_arch} in
       x86_64)                         sysname=amd64_linux${kv}        ;;
       alpha*)                         sysname=alpha_linux_${kv}       ;;
       i386|i486|i586|i686|athlon)     sysname=i386_linux${kv}         ;;
       *)                              sysname=%{_arch}_linux${kv}     ;;
esac
DESTDIR=$RPM_BUILD_ROOT; export DESTDIR
CFLAGS="$RPM_OPT_FLAGS"; export CFLAGS

KRB5_CONFIG="%{krb5config}"
export KRB5_CONFIG
./configure --with-afs-sysname=${sysname} \
       --prefix=%{_prefix} \
       --libdir=%{_libdir} \
       --bindir=%{_bindir} \
       --sbindir=%{_sbindir} \
       --disable-strip-binaries \
       --disable-kernel-module \
       --enable-debug \
       --with-krb5 \
       --enable-bitmap-later \
       --enable-supergroups \
       || exit 1
make
#make -j16

##############################################################################
#
# installation
#
##############################################################################
%install
make install DESTDIR=$RPM_BUILD_ROOT
export DONT_GPRINTIFY=1

kv='26'

case %{_arch} in
       x86_64)                         sysname=amd64_linux${kv}        ;;
       alpha*)                         sysname=alpha_linux_${kv}       ;;
       i386|i486|i586|i686|athlon)     sysname=i386_linux${kv}         ;;
       *)                              sysname=%{_arch}_linux${kv}     ;;
esac

# Fix the location of restorevol, since it should be available for
# any user in /usr/bin
#mv $RPM_BUILD_ROOT%{_prefix}/afs/bin/restorevol $RPM_BUILD_ROOT%{_bindir}/restorevol

# Link kpasswd to kapasswd
#ln -f $RPM_BUILD_ROOT%{_bindir}/kpasswd $RPM_BUILD_ROOT%{_bindir}/kapasswd

# Copy root.client config files
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
install -m 755 src/packaging/RedHat/openafs.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/openafs
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
install -m 755 src/packaging/RedHat/openafs-client.init $RPM_BUILD_ROOT%{initdir}/openafs-client
install -m 755 src/packaging/RedHat/openafs-server.init $RPM_BUILD_ROOT%{initdir}/openafs-server
%else
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules
install -m 755 src/packaging/RedHat/openafs-client.service $RPM_BUILD_ROOT%{_unitdir}/openafs-client.service
install -m 755 src/packaging/RedHat/openafs-client.modules $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/modules/openafs-client.modules
install -m 755 src/packaging/RedHat/openafs-server.service $RPM_BUILD_ROOT%{_unitdir}/openafs-server.service
%endif

# PAM symlinks
ln -sf pam_afs.so.1 $RPM_BUILD_ROOT%{_libdir}/pam_afs.so
ln -sf pam_afs.krb.so.1 $RPM_BUILD_ROOT%{_libdir}/pam_afs.krb.so

#
# Install DOCUMENTATION
#

# Build the DOC directory
mkdir -p $RPM_BUILD_ROOT/$RPM_DOC_DIR/openafs-%{afsvers}
tar cf - -C doc LICENSE html pdf | \
    tar xf - -C $RPM_BUILD_ROOT/$RPM_DOC_DIR/openafs-%{afsvers}
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT/$RPM_DOC_DIR/openafs-%{afsvers}
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT/$RPM_DOC_DIR/openafs-%{afsvers}

# Copy the uninstalled krb5 files (or delete the unused krb5 files)
#mv $RPM_BUILD_ROOT%{_prefix}/afs/bin/asetkey $RPM_BUILD_ROOT%{_sbindir}/asetkey

# remove unused man pages
for x in afs_ftpd afs_inetd afs_login afs_rcp afs_rlogind afs_rsh \
    dkload knfs symlink symlink_list symlink_make \
    symlink_remove; do
	rm -f $RPM_BUILD_ROOT%{_mandir}/man1/${x}.1
done

# rename kpasswd to kapasswd
#mv $RPM_BUILD_ROOT%{_mandir}/man1/kpasswd.1 $RPM_BUILD_ROOT%{_mandir}/man1/kapasswd.1

#
# Remove files we're not installing
#

# the rest are not needed.
for f in dlog dpass install knfs livesys ; do
  rm -f $RPM_BUILD_ROOT%{_bindir}/$f
done

# not supported on Linux or duplicated
for f in kdb rmtsysd kpwvalid ; do
  rm -f $RPM_BUILD_ROOT%{_sbindir}/$f
done

# remove man pages from programs deleted above
for f in 1/dlog 1/copyauth 1/dpass 1/livesys 8/rmtsysd 8/aklog_dynamic_auth 8/kdb 8/kpwvalid 8/xfs_size_check 1/package_test 5/package 8/package ; do
  rm -f $RPM_BUILD_ROOT%{_mandir}/man$f.*
done

# PAM modules are doubly-installed  Remove the version we don't need
#for f in pam_afs.krb.so.1 pam_afs.so.1 ; do
#  rm -f $RPM_BUILD_ROOT%{_libdir}/$f
#done

#%endif
#delete static libraries not in upstream package
rm -f $RPM_BUILD_ROOT%{_libdir}/libjuafs.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libuafs.a

##############################################################################
###
### clean
###
##############################################################################
%clean
rm -f openafs-file-list
[ "$RPM_BUILD_ROOT" != "/" -a "x%{debugspec}" != "x1" ] && \
	rm -fr $RPM_BUILD_ROOT

##############################################################################
###
### scripts
###
##############################################################################
%post client
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
chkconfig --add openafs-client
%else
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%endif
if [ ! -d /afs ]; then
	mkdir /afs
	chown root.root /afs
	chmod 0755 /afs
	[ -x /sbin/restorecon ] && /sbin/restorecon /afs
fi

# Create the CellServDB
[ -f /usr/vice/etc/CellServDB.local ] || touch /usr/vice/etc/CellServDB.local

( cd /usr/vice/etc ; \
  cat CellServDB.local CellServDB.dist > CellServDB ; \
  chmod 644 CellServDB )

%post server
#on an upgrade, don't enable if we were disabled
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
if [ $1 = 1 ] ; then
  chkconfig --add openafs-server
fi
%{initdir}/openafs-server condrestart

%post authlibs
/sbin/ldconfig

%postun authlibs
/sbin/ldconfig

%preun
if [ $1 = 0 ] ; then
	[ -d /afs ] && rmdir /afs
	:
fi

%preun client
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
if [ $1 = 0 ] ; then
        %{initdir}/openafs-client stop
        chkconfig --del openafs-client
fi
%else
if [ $1 -eq 0 ] ; then
    	# Package removal, not upgrade
    	/bin/systemctl --no-reload disable openafs-client.service > /dev/null 2>&1 || :
    	/bin/systemctl stop openafs-client.service > /dev/null 2>&1 || :
fi
%endif

%preun server
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
if [ $1 = 0 ] ; then
        %{initdir}/openafs-server stop
        chkconfig --del openafs-server
fi
%else
if [ $1 -eq 0 ] ; then
    	/bin/systemctl --no-reload disable openafs-server.service > /dev/null 2>&1 || :
    	/bin/systemctl stop openafs-server.service > /dev/null 2>&1 || :
fi
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%postun client
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun server
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif

%endif


%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%triggerun -- openafs-client < 1.6.0-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save openafs-client >/dev/null 2>&1 ||:

# Run this because the SysV package being removed won't do it
/sbin/chkconfig --del openafs-client >/dev/null 2>&1 || :

%triggerun -- openafs-server < 1.6.0-1
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save openafs-server >/dev/null 2>&1 ||:

# Run this because the SysV package being removed won't do it
/sbin/chkconfig --del openafs-server >/dev/null 2>&1 || :
%endif

##############################################################################
###
### file lists
###
##############################################################################
%files 
#-f openafs-file-list
%defattr(-,root,root)
%config(noreplace) /etc/sysconfig/openafs
%{_bindir}/afsmonitor
%{_bindir}/bos
%{_bindir}/fs
%{_bindir}/kpasswd
%{_bindir}/klog
%{_bindir}/klog.krb
%{_bindir}/pagsh
%{_bindir}/pagsh.krb
%{_bindir}/pts
%{_bindir}/restorevol
%{_bindir}/scout
%{_bindir}/sys
%{_bindir}/tokens
%{_bindir}/tokens.krb
%{_bindir}/translate_et
%{_bindir}/xstat_cm_test
%{_bindir}/xstat_fs_test
%{_bindir}/udebug
%{_bindir}/unlog
%{_sbindir}/backup
%{_sbindir}/butc
%{_sbindir}/fms
%{_sbindir}/fstrace
%{_sbindir}/kas
%{_sbindir}/read_tape
%{_sbindir}/rxdebug
%{_sbindir}/uss
%{_sbindir}/vos
%{_sbindir}/vsys
%{_mandir}/man1/fs*.gz
%{_mandir}/man1/pts*.gz
%{_mandir}/man1/vos*.gz
%{_mandir}/man1/afs.1.gz
%{_mandir}/man1/afsmonitor.1.gz
%{_mandir}/man1/klog.1.gz
%{_mandir}/man1/klog.krb.1.gz
%{_mandir}/man1/pagsh.1.gz
%{_mandir}/man1/pagsh.krb.1.gz
%{_mandir}/man1/kpasswd.1.gz
%{_mandir}/man1/rxdebug.1.gz
%{_mandir}/man1/restorevol.1.gz
%{_mandir}/man1/scout.1.gz
%{_mandir}/man1/tokens.1.gz
%{_mandir}/man1/tokens.krb.1.gz
%{_mandir}/man1/translate_et.1.gz
%{_mandir}/man1/xstat_cm_test.1.gz
%{_mandir}/man1/xstat_fs_test.1.gz
%{_mandir}/man5/afsmonitor.5.gz
%{_mandir}/man1/udebug.1.gz
%{_mandir}/man1/unlog.1.gz
%{_mandir}/man5/uss.5.gz
%{_mandir}/man5/uss_bulk.5.gz
%{_mandir}/man8/bos*
%{_mandir}/man8/fstrace*
%{_mandir}/man8/kas*
%{_mandir}/man1/sys.1.gz
%{_mandir}/man8/backup*
%{_mandir}/man5/butc.5.gz
%{_mandir}/man5/butc_logs.5.gz
%{_mandir}/man8/butc.8.gz
%{_mandir}/man8/fms.8.gz
%{_mandir}/man8/read_tape.8.gz
%{_mandir}/man8/fssync-debug*
%{_mandir}/man8/uss*
%{_mandir}/man5/CellServDB.5.gz
%{_mandir}/man5/ThisCell.5.gz
%doc %{_docdir}/openafs-%{afsvers}/LICENSE

%files docs
%defattr(-,root,root)
%docdir %{_docdir}/openafs-%{afsvers}
%dir %{_docdir}/openafs-%{afsvers}
%{_docdir}/openafs-%{afsvers}/ChangeLog
%{_docdir}/openafs-%{afsvers}/RELNOTES-%{afsvers}
%{_docdir}/openafs-%{afsvers}/pdf

%files client
%defattr(-,root,root)
#%dir %{_prefix}/vice
#%dir %{_prefix}/vice/cache
#%dir %{_prefix}/vice/etc
#%dir %{_prefix}/vice/etc/C
#%{_prefix}/vice/etc/CellServDB.dist
#%config(noreplace) %{_prefix}/vice/etc/ThisCell
#%config(noreplace) %{_prefix}/vice/etc/cacheinfo
%{_bindir}/afsio
%{_bindir}/cmdebug
%{_bindir}/up
%{_sbindir}/afsd
%{_prefix}/share/openafs/C/afszcm.cat
%{_libdir}/pam_afs.krb.so.1
%{_libdir}/pam_afs.krb.so
%{_libdir}/pam_afs.so.1
%{_libdir}/pam_afs.so
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
%{initdir}/openafs-client
%else
%{_unitdir}/openafs-client.service
%{_sysconfdir}/sysconfig/modules/openafs-client.modules
%endif
%{_mandir}/man1/cmdebug.*
%{_mandir}/man1/up.*
%{_mandir}/man5/afs.5.gz
%{_mandir}/man5/afs_cache.5.gz
%{_mandir}/man5/afs_volume_header.5.gz
%{_mandir}/man5/afszcm.cat.5.gz
%{_mandir}/man5/cacheinfo.*
%{_mandir}/man8/afsd.*
%{_mandir}/man8/vsys.*
%{_mandir}/man5/CellAlias.*

%files server
%defattr(-,root,root)
%{_sbindir}/bosserver
%{_sbindir}/bos_util
%{_libexecdir}/openafs/buserver
%{_libexecdir}/openafs/dafileserver
%{_sbindir}/dafssync-debug
%{_libexecdir}/openafs/dasalvager
%{_libexecdir}/openafs/davolserver
%{_libexecdir}/openafs/fileserver
%{_sbindir}/fssync-debug
# Should we support KAServer?
%{_libexecdir}/openafs/kaserver
%{_sbindir}/ka-forwarder
%{_sbindir}/pt_util
%{_libexecdir}/openafs/ptserver
%{_libexecdir}/openafs/salvager
%{_libexecdir}/openafs/salvageserver
%{_sbindir}/salvsync-debug
%{_sbindir}/state_analyzer
%{_libexecdir}/openafs/upclient
%{_libexecdir}/openafs/upserver
%{_libexecdir}/openafs/vlserver
%{_sbindir}/volinfo
%{_libexecdir}/openafs/volserver
%{_sbindir}/kadb_check
%{_sbindir}/prdb_check
%{_sbindir}/vldb_check
%{_sbindir}/vldb_convert
%{_sbindir}/voldump
%if 0%{?fedora} < 15 && 0%{?rhel} < 7
%{initdir}/openafs-server
%else
%{_unitdir}/openafs-server.service
%endif
%{_mandir}/man5/AuthLog.*
%{_mandir}/man5/BackupLog.*
%{_mandir}/man5/BosConfig.*
%{_mandir}/man5/BosLog.*
%{_mandir}/man5/FORCESALVAGE.*
%{_mandir}/man5/FileLog.*
%{_mandir}/man5/KeyFile.*
%{_mandir}/man5/NetInfo.*
%{_mandir}/man5/NetRestrict.*
%{_mandir}/man5/NoAuth.*
%{_mandir}/man5/SALVAGE.fs.*
%{_mandir}/man5/SalvageLog.*
%{_mandir}/man5/sysid.*
%{_mandir}/man5/UserList.*
%{_mandir}/man5/VLLog.*
%{_mandir}/man5/VolserLog.*
%{_mandir}/man5/bdb.DB0.*
%{_mandir}/man5/fms.log.*
%{_mandir}/man5/kaserver.DB0.*
%{_mandir}/man5/kaserverauxdb.*
%{_mandir}/man5/krb.conf.*
%{_mandir}/man5/krb.excl.*
%{_mandir}/man5/prdb.DB0.*
%{_mandir}/man5/salvage.lock.*
%{_mandir}/man5/tapeconfig.*
%{_mandir}/man5/vldb.DB0.*
%{_mandir}/man8/buserver.*
%{_mandir}/man8/fileserver.*
%{_mandir}/man8/dafileserver.*
%{_mandir}/man8/dafssync-debug.*
%{_mandir}/man8/dasalvager.*
%{_mandir}/man8/davolserver.*
%{_mandir}/man8/kadb_check.*
%{_mandir}/man8/ka-forwarder.*
%{_mandir}/man8/prdb_check.*
%{_mandir}/man8/ptserver.*
%{_mandir}/man8/pt_util.*
%{_mandir}/man8/salvager.*
%{_mandir}/man8/salvageserver.*
%{_mandir}/man8/state_analyzer.*
%{_mandir}/man8/upclient.*
%{_mandir}/man8/upserver.*
%{_mandir}/man8/vldb_check.*
%{_mandir}/man8/vldb_convert.*
%{_mandir}/man8/vlserver.*
%{_mandir}/man8/voldump.*
%{_mandir}/man8/volinfo.*
%{_mandir}/man8/volserver.*

%files authlibs
%defattr(-,root,root)
%{_libdir}/libafsauthent.so.*
%{_libdir}/libafsrpc.so.*
%{_libdir}/libkopenafs.so.*

%files authlibs-devel
%defattr(-,root,root)
%{_includedir}/kopenafs.h
%{_libdir}/libafsauthent.a
%{_libdir}/libafscp.a
%{_libdir}/libafsrpc.a
%{_libdir}/libafsauthent_pic.a
%{_libdir}/libafsrpc_pic.a
%{_libdir}/libkopenafs.a
%{_libdir}/libafsauthent.so
%{_libdir}/libafsrpc.so
%{_libdir}/libkopenafs.so

%files devel
%defattr(-,root,root)
%{_bindir}/afs_compile_et
%{_bindir}/rxgen
%{_includedir}/afs
%{_includedir}/des.h
%{_includedir}/des_conf.h
%{_includedir}/des_odd.h
%{_includedir}/des_prototypes.h
%{_includedir}/lock.h
%{_includedir}/lwp.h
%{_includedir}/mit-cpyright.h
%{_includedir}/preempt.h
%{_includedir}/rx
%{_includedir}/timer.h
%{_includedir}/ubik.h
%{_includedir}/ubik_int.h
%{_libdir}/afs
%{_libdir}/libdes.a
%{_libdir}/liblwp.a
%{_libdir}/librx.a
%{_libdir}/librxkad.a
%{_libdir}/librxstat.a
%{_libdir}/libubik.a
%{_mandir}/man1/rxgen.*
%{_mandir}/man1/afs_compile_et.*

%files kpasswd
%defattr(-,root,root)
%{_bindir}/kpasswd
%{_bindir}/kpwvalid

%files krb5
%defattr(-,root,root)
%{_bindir}/aklog
%{_bindir}/klog.krb5
%{_bindir}/asetkey
%{_mandir}/man1/aklog.*
%{_mandir}/man1/klog.krb5.1.gz
%{_mandir}/man8/asetkey.*

