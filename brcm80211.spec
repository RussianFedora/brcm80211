# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
#define buildforkernels newest

Name:		brcm80211
Version:	2.6.40
Release:	1%{?dist}
Summary:	Kernel module for broadcom wireless devices
Group:		System Environment/Kernel
License:	GPLv2
URL:		http://linuxwireless.org/en/users/Drivers/brcm80211
Source0:	%{name}.tar.bz2
Source2:	%{name}-blacklist.conf
Source11:	%{name}-kmodtool-excludekernel-filterfile
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1:		%{name}-includes.patch

BuildRequires:	%{_bindir}/kmodtool
Requires:	kernel = %{version}

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i686 x86_64
# ppc disabled because broadcom only provides x86 and x86_64 bits

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%package common
Summary:	Common files for Broadcom brcmsmac (mac80211-based softmac PCIe) and brcmfmac (SDIO) drivers.
BuildArch:	noarch
Provides:	%{name}-kmod-common = %{version}
Requires:	%{name}-kmod = %{version}
ExcludeArch:    ppc ppc64

%description
Broadcom brcmsmac (mac80211-based softmac PCIe) and brcmfmac (SDIO) drivers.
* Completely open source host drivers, no binary object files.
* Framework for supporting new chips, including mac80211-aware embedded chips
* Does not support older PCI/PCIe chips with SSB backplane 

%description common
This package contains the readme and configuration files
for the Broadcom brcmsmac (mac80211-based softmac PCIe) 
and brcmfmac (SDIO) drivers.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -n %{name}
%patch1 -p1 -b .add-includes
cd %{_builddir}

for kernel_version in %{?kernel_versions} ; do
 cp -a %{name} _kmod_build_${kernel_version%%___*}
done

%build
cd %{_builddir}
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}
 CONFIG_BRCMUTIL=m CONFIG_BRCMFMAC=m CONFIG_BRCMSMAC=m make -C ${kernel_version##*___} M=`pwd` modules
 popd
done

%install
rm -rf ${RPM_BUILD_ROOT}
cd %{_builddir}
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
 install -m 644 brcmsmac/*.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
 install -m 644 brcmfmac/*.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
 install -m 644 util/*.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
 popd
done

mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/modprobe.d/
install -p -m0644 %{SOURCE2} ${RPM_BUILD_ROOT}/%{_sysconfdir}/modprobe.d/ 

chmod 0755 $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/*/%{kmodinstdir_postfix}/* || :
%{?akmod_install}

%files common
%defattr(-,root,root,-)
%doc README TODO
%config(noreplace) %{_sysconfdir}/modprobe.d/%{name}-blacklist.conf

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Aug  7 2011 Alexei Panov <elemc AT atisserv DOT ru> - 2.6.40-1
- Initial build


