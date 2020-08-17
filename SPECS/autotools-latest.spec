%{?_compat_el5_build}

# Workaround to always have %%scl defined
%{!?scl:%global scl autotools-latest}

%{?scl:%scl_package %scl}

# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define release_prefix 14

Summary: Package that installs %scl
Name: %scl_name
Version: 1
Release: %{release_prefix}%{?dist}.cpanel
License: GPLv2+
Group: Applications/File

Requires: %{?scl_prefix}m4, %{?scl_prefix}automake
Requires: %{?scl_prefix}autoconf, %{?scl_prefix}libtool
%{?scl:BuildRequires: scl-utils-build}
%{?scl:BuildRequires: iso-codes}

%if ! 0%{?buildroot:1}
# HACK!  This should be truth only for RHEL5, so benefit from
# this %%if for defining (otherwise undefined) macro for this platform.
%global rhel 5
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif

%description
This is the main package for %scl Software Collection.  It contains the latest
released (stable) versions of autotools.  Just run "scl enable %scl bash" to
make it work instead of system-default autotools.


%package runtime
Summary: Package that handles %scl Software Collection.
Group: Applications/File
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.


%prep
%setup -c -T


%build
%if 0%{?rhel} >= 5 && 0%{?rhel} < 8
cat <<EOF | tee enable
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export LIBRARY_PATH=%{_libdir}\${LIBRARY_PATH:+:\${LIBRARY_PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}:\$MANPATH
export INFOPATH=%{_infodir}\${INFOPATH:+:\${INFOPATH}}
EOF
%else
cat > %{scl} << EOF
#%%Module1.0
prepend-path    X_SCLS              %{scl}
prepend-path    PATH                %{_bindir}
prepend-path    LIBRARY_PATH        %{_libdir}
prepend-path    LD_LIBRARY_PATH     %{_libdir}
prepend-path    MANPATH             %{_mandir}
prepend-path    INFOPATH            %{_infodir}
prepend-path    PKG_CONFIG_PATH     %{_libdir}/pkgconfig
EOF
%endif

%install
%if 0%{?rhel} == 5
rm -rf %{buildroot}
%endif

%if 0%{?rhel} >= 5 && 0%{?rhel} < 8
mkdir -p %{buildroot}/%{_scl_scripts}/root
install -c -p -m 0644 enable %{buildroot}%{_scl_scripts}/enable
%else
mkdir -p %{buildroot}%{_scl_scripts}
install -c -p -m 0644 %{scl} %{buildroot}%{_scl_scripts}
#automaticaly create enable script for compatibility
%scl_enable_script
%endif

%scl_install

cat %{buildroot}/%{_root_sysconfdir}/rpm/macros.%{scl}-config
rm -rf %{buildroot}/%{_root_sysconfdir}/rpm/macros.%{scl}-config


%files


%files runtime
%scl_files
%if 0%{?rhel} >= 8
%defattr(755,root,root,755)
/etc/scl/modulefiles/autotools-latest
/opt/rh/autotools-latest/autotools-latest
%endif

%changelog
* Thu May 21 2020 Julian Brown <julian.brown@cpanel.net> - 1-14
- ZC-6854: Correct builds issues on C8

* Wed Aug 12 2015 Pavel Raiskup <praiskup@redhat.com> - 1-13
- use _compat_el5_build only if defined (rhbz#1252751)

* Tue Jun 23 2015 Pavel Raiskup <praiskup@redhat.com> - 1-12
- make the meta-packages architecture dependant

* Thu Jun 11 2015 Pavel Raiskup <praiskup@redhat.com> - 1-11
- fix for scl-utils 2.0 (environment modules)

* Fri Aug 15 2014 Pavel Raiskup <praiskup@redhat.com> - 1-10
- rebuilt

* Sat Jul 19 2014 Pavel Raiskup <praiskup@redhat.com> - 1-9
- merge changes from autotools-git.spec

* Thu May 29 2014 Pavel Raiskup <praiskup@redhat.com> - 1-8
- release bump for %%_compat_el5_build

* Fri Apr 18 2014 Pavel Raiskup <praiskup@redhat.com> - 1-7
- the fix for 'filelist' (#1079203) is not needed, according to
  https://fedorahosted.org/SoftwareCollections/ticket/18

* Thu Apr 17 2014 Pavel Raiskup <praiskup@redhat.com> - 1-6
- merge fixes with autotools-git version

* Tue Mar 25 2014 Pavel Raiskup <praiskup@redhat.com> - 1-5
- buildroots are prepared, lets require all packages

* Tue Mar 25 2014 Pavel Raiskup <praiskup@redhat.com> - 1-4
- fixes for RHEL5

* Fri Mar 21 2014 Pavel Raiskup <praiskup@redhat.com> - 1-3
- ok, this is annoying but I overlooked the mistake

* Fri Mar 21 2014 Pavel Raiskup <praiskup@redhat.com> - 1-2
- oh well, the EPEL7 workaround causes problem now on EPEL7, giving up and not
  trying to observe what really happens

* Fri Mar 21 2014 Pavel Raiskup <praiskup@redhat.com> - 1-1
- initial packaging
