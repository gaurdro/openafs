# Openafs Spec $Revision$
%define pkgrel 1
%define afsvers 1.6.11

Summary: OpenAFS distributed filesystem
Name: openafs-kmod
Version: 1.6.11
Release: %{pkgrel}%{?dist}
License: IBM Public License
URL: http://www.openafs.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Group: Networking/Filesystems
BuildRequires: pam-devel, flex, bison

ExclusiveArch: %{ix86} x86_64

Source0: http://www.openafs.org/dl/openafs/%{afsvers}/openafs-%{afsvers}-src.tar.bz2

Source10: http://www.openafs.org/dl/openafs/%{afsvers}/RELNOTES-%{afsvers}
Source11: http://www.openafs.org/dl/openafs/%{afsvers}/ChangeLog
Source13: find-installed-kversion.sh
Source14: openafs-kmodtool

%description
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the kernel module for the OpenAFS client

%define dkms_version %{version}-%{pkgrel}%{?dist}
%{expand:%(sh %{SOURCE13})}
%{expand:%(sh %{SOURCE14} rpmtemplate openafs %{kversion} /usr/sbin/depmod "")}

%package -n dkms-openafs
Summary:        DKMS-ready kernel source for AFS distributed filesystem
Group:          Development/Kernel
Provides:       openafs-kernel = %{version}
Provides:       openafs-kmod = %{version}
Requires(pre):  dkms
Requires(pre):  flex, bison, gcc
Requires(post): dkms
Requires:	openafs-kmod-common = %{version}

%description -n dkms-openafs
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the source code to allow DKMS to build an
AFS kernel module.

%package docs
Summary:        OpenAFS kernel module documentation
Group:          Networking/Filesystems
Requires:	openafs-kmod-common = %{version}

%description docs
The AFS distributed filesystem.  AFS is a distributed filesystem
allowing cross-platform sharing of files among multiple computers.
Facilities are provided for access control, authentication, backup and
administrative management.

This package provides the documentation for the AFS kernel module.


##############################################################################
#
# PREP
#
##############################################################################

%prep
# Just for logging purposes
echo '%kversion'
# Install OpenAFS src and doc
%setup -q -n openafs-%{afsvers}

##############################################################################
#
# building
#
##############################################################################
%build
case %{_arch} in
       x86_64)                         sysname=amd64_linux26        ;;
       i386|i486|i586|i686|athlon)     sysname=i386_linux26         ;;
       *)                              sysname=%{_arch}_linux26     ;;
esac

./configure --with-afs-sysname=${sysname} \
  	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
        --with-linux-kernel-packaging \
	--with-linux-kernel-headers=/usr/src/kernels/%{kversion}.%{_target_cpu} \
	|| exit 1

make dest_only_libafs MPS=SP

# Build the libafs tree
make only_libafs_tree || exit 1


##############################################################################
#
# installation
#
##############################################################################
%install
case %{_arch} in
       x86_64)                         sysname=amd64_linux26        ;;
       i386|i486|i586|i686|athlon)     sysname=i386_linux26         ;;
       *)                              sysname=%{_arch}_linux26     ;;
esac

srcdir=${sysname}/dest/root.client/lib/modules/%{kversion}.%{_target_cpu}/extra/openafs
dstdir=$RPM_BUILD_ROOT/lib/modules/%{kversion}.%{_target_cpu}/extra/openafs

[ $RPM_BUILD_ROOT != / ] && rm -rf $RPM_BUILD_ROOT
install -D -m 755 ${srcdir}/openafs.ko ${dstdir}/openafs.ko

# copy Release notes and changelog into src dir
cp %{SOURCE10} %{SOURCE11} .

#
# install dkms source
#
install -d -m 755 $RPM_BUILD_ROOT%{_prefix}/src
cp -a libafs_tree $RPM_BUILD_ROOT%{_prefix}/src/openafs-%{dkms_version}

cat > $RPM_BUILD_ROOT%{_prefix}/src/openafs-%{dkms_version}/dkms.conf <<"EOF"

PACKAGE_VERSION="%{dkms_version}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="openafs"
MAKE[0]='./configure --with-linux-kernel-headers=${kernel_source_dir} --with-linux-kernel-packaging && make && mv src/libafs/MODLOAD-*/openafs.ko .'
CLEAN="make -C src/libafs clean"

BUILT_MODULE_NAME[0]="openafs"
DEST_MODULE_LOCATION[0]="/extra/openafs/"
STRIP[0]=no
AUTOINSTALL=yes

EOF

##############################################################################
###
### clean
###
##############################################################################
%clean
[ "$RPM_BUILD_ROOT" != "/" ] && \
	rm -fr $RPM_BUILD_ROOT

##############################################################################
###
### scripts
###
##############################################################################
%post -n dkms-openafs
dkms add -m openafs -v %{dkms_version} --rpm_safe_upgrade
dkms build -m openafs -v %{dkms_version} --rpm_safe_upgrade
dkms install -m openafs -v %{dkms_version} --rpm_safe_upgrade

%preun -n dkms-openafs
dkms remove -m openafs -v %{dkms_version} --rpm_safe_upgrade --all ||:

##############################################################################
###
### file lists
###
##############################################################################
%files docs
%defattr(-,root,root)
%doc src/LICENSE README README.DEVEL README.GIT NEWS RELNOTES-%{afsvers} ChangeLog

%files -n dkms-openafs
%defattr(-,root,root)
%{_prefix}/src/openafs-%{dkms_version}

##############################################################################
###
### openafs-kmod.spec change log
###
##############################################################################
%changelog
* Mon Mar 02 2015 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.11-1.1
- Rebuilt for 1.6.11

* Wed Oct  1 2014 Jonathan S. Billings <jsbillin@umich.edu> - 1.6.9-1
- Created initial spec file

