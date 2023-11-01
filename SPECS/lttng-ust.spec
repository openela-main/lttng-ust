%define with_numactl          0%{!?_without_numactl:1}

# Numactl is not available on armhf
%ifarch armv7hl
%define with_numactl 0
%endif

%if %{with_numactl}
    %define arg_numactl --enable-numa
%else
    %define arg_numactl --disable-numa
%endif


Name:           lttng-ust
Version:        2.12.0
Release:        6%{?dist}

License:        LGPLv2.1, MIT and GPLv2
Summary:        LTTng Userspace Tracer library
URL:            https://lttng.org
Source0:        https://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2
Source1:        https://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2.asc
# gpg2 --export --export-options export-minimal 2A0B4ED915F2D3FA45F5B16217280A9781186ACF > gpgkey-2A0B4ED915F2D3FA45F5B16217280A9781186ACF.gpg
Source2:        gpgkey-2A0B4ED915F2D3FA45F5B16217280A9781186ACF.gpg
Patch0:         lttng-gen-tp-shebang.patch
Patch1:         0001-Fix-namespace-contexts-CONFIG_RCU_TLS-variable-initi.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gnupg2
BuildRequires:  libtool
BuildRequires:  libuuid-devel
BuildRequires:  pkgconfig
BuildRequires:  systemtap-sdt-devel
BuildRequires:  userspace-rcu-devel >= 0.12.0
%if %{with_numactl}
BuildRequires:  numactl-devel
%endif

%description
This library may be used by user-space applications to generate 
trace-points using LTTng.


%package -n %{name}-devel
Summary:        LTTng Userspace Tracer library headers and development files
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       userspace-rcu-devel
Requires:       systemtap-sdt-devel

%description -n %{name}-devel
The %{name}-devel package contains libraries and header to instrument
applications using %{name}


%package -n python3-lttngust
Summary:        Python bindings for LTTng UST
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  python3-devel
BuildRequires: make
%{?python_provide:%python_provide python3-lttngust}

%description -n python3-lttngust
The python3-lttngust package contains libraries needed to instrument
applications that use %{name}'s Python logging backend.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
# Reinitialize libtool with the fedora version to remove Rpath
autoreconf -vif

%configure \
	--docdir=%{_docdir}/%{name} \
	--disable-static \
	--enable-python-agent \
	--with-sdt \
	%{?arg_numactl}

make %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install
rm -vf %{buildroot}%{_libdir}/*.la

%check
make check

%ldconfig_scriptlets

%files
%{_libdir}/*.so.*
%{_mandir}/man3/do_tracepoint.3.gz
%{_mandir}/man3/lttng-ust.3.gz
%{_mandir}/man3/lttng-ust-cyg-profile.3.gz
%{_mandir}/man3/lttng-ust-dl.3.gz
%{_mandir}/man3/tracef.3.gz
%{_mandir}/man3/tracelog.3.gz
%{_mandir}/man3/tracepoint.3.gz
%{_mandir}/man3/tracepoint_enabled.3.gz

%dir %{_docdir}/%{name}
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/COPYING
%{_docdir}/%{name}/java-agent.txt
%{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/README.md


%files -n %{name}-devel
%{_bindir}/lttng-gen-tp
%{_mandir}/man1/lttng-gen-tp.1.gz
%{_prefix}/include/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/lttng-ust*.pc

%dir %{_docdir}/%{name}/examples
%{_docdir}/%{name}/examples/*

%files -n python3-lttngust
%{python3_sitelib}/lttngust/
%{python3_sitelib}/lttngust-*.egg-info

%changelog
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 2.12.0-6
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 2.12.0-5
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.12.0-2
- Rebuilt for Python 3.9

* Tue Apr 14 2020 Michael Jeanson <mjeanson@efficios.com> - 2.12.0-1
- New upstream release

* Fri Mar 06 2020 Michael Jeanson <mjeanson@efficios.com> - 2.11.1-1
- New upstream release
- Add requires systemtap-sdt-devel to lttng-ust-devel (#1386412)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Michael Jeanson <mjeanson@efficios.com> - 2.11.0-3
- Enable SystemTAP SDT support (#1386412)

* Wed Jan 22 2020 Michael Jeanson <mjeanson@efficios.com> - 2.11.0-2
- Add patch to fix build failure with GCC 10

* Tue Oct 22 2019 Michael Jeanson <mjeanson@efficios.com> - 2.11.0-1
- New upstream release

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.10.4-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.10.4-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 03 2019 Michael Jeanson <mjeanson@efficios.com> - 2.10.4-1
- New upstream release
- Add patch to build on glibc >= 2.30

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 07 2018 Michael Jeanson <mjeanson@efficios.com> - 2.10.2-1
- New upstream release
- Add python3-lttngust sub-package.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.10.1-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Michael Jeanson <mjeanson@efficios.com> - 2.10.1-1
- New upstream release

* Fri Aug 18 2017 Dan Horák <dan[at]danny.cz> - 2.10.0-2
- drop the s390(x) build workaround

* Wed Aug 02 2017 Michael Jeanson <mjeanson@efficios.com> - 2.10.0-1
- New upstream release

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Michael Jeanson <mjeanson@efficios.com> - 2.9.1-1
- New upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 30 2016 Michael Jeanson <mjeanson@efficios.com> - 2.9.0-1
- New upstream release

* Wed Jun 22 2016 Michael Jeanson <mjeanson@efficios.com> - 2.8.1-2
- Re-add rpath removing
- Fix spelling errors

* Tue Jun 21 2016 Michael Jeanson <mjeanson@efficios.com> - 2.8.1-1
- New upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 6 2015 Suchakra Sharma <suchakra@fedoraproject.org> - 2.6.2-2
- Remove remaining BR for SystemTap SDT and add python as a BR

* Thu Jul 23 2015 Michael Jeanson <mjeanson@gmail.com> - 2.6.2-1
- New upstream release
- Drop SystemTap SDT support
- Remove patches applied upstream

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec  9 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.5.1-2
- Add patch to fix aarch64 support

* Mon Nov 03 2014 Suchakra Sharma <suchakra@fedoraproject.org> - 2.5.1-1
- New upstream release
- Update URL

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.4.1-1
- New upstream bugfix release

* Sat Mar 1 2014 Suchakra Sharma <suchakra@fedoraproject.org> - 2.4.0-1
- New upstream release
- Add new files (man and doc)

* Sat Feb 22 2014 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.3.0-2
- Rebuilt for URCU Soname change

* Fri Sep 20 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.3.0-1
- New upstream release (include snapshop feature)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.2.1-1
- New upstream release
- Bump URCU dependency

* Thu May 23 2013 Dan Horák <dan[at]danny.cz> - 2.1.2-2
- add build workaround for s390(x)

* Fri May 17 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.2-1
- New upstream bugfix release
- Remove patches applied upstream

* Wed Feb 27 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.1-2
- Remove dependency of probes on urcu-bp

* Tue Feb 26 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.1-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.5-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.4-2
- Add dependency on systemtap-sdt-devel for devel package

* Tue Jun 19 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.4-1
- New upstream release
- Updates from review comments

* Thu Jun 14 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.3-1
- New package, inspired by the one from OpenSuse

