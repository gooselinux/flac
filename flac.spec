Summary: An encoder/decoder for the Free Lossless Audio Codec
Name: flac
Version: 1.2.1
Release: 6.1%{?dist}
License: BSD and GPLv2+
Group: Applications/Multimedia
Source: http://prdownloads.sourceforge.net/flac/flac-%{version}.tar.gz
Patch1: flac-1.2.1-asm.patch
Patch2: flac-1.2.1-gcc43.patch
Patch3: flac-1.2.1-hidesyms.patch
Patch4: flac-1.2.1-tests.patch
Patch5: flac-1.2.1-cflags.patch
Patch6: flac-1.2.1-bitreader.patch
URL: http://flac.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libogg-devel
BuildRequires: automake autoconf libtool gettext-devel
%ifarch %{ix86}
# 2.0 supports symbol visibility
BuildRequires: nasm >= 2.0
%endif

%description
FLAC stands for Free Lossless Audio Codec. Grossly oversimplified, FLAC
is similar to Ogg Vorbis, but lossless. The FLAC project consists of
the stream format, reference encoders and decoders in library form,
flac, a command-line program to encode and decode FLAC files, metaflac,
a command-line metadata editor for FLAC files and input plugins for
various music players.

%package devel
Summary: Development libraries and header files from FLAC
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains all the files needed to develop applications that
will use the Free Lossless Audio Codec.

%prep
%setup -q
%patch1 -p1 -b .asm
%patch2 -p1 -b .gcc43
%patch3 -p1 -b .hidesyms
# reduce number of tests
%patch4 -p1 -b .tests
%patch5 -p1 -b .cflags
%patch6 -p0 -b .bitreader

%build
./autogen.sh -V

%configure \
    --disable-xmms-plugin \
    --disable-thorough-tests

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find doc/ -name "Makefile*" -exec rm -f {} \;

%check
make -C test check &> /dev/null

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root,-)
%doc AUTHORS COPYING* README
%{_bindir}/flac
%{_bindir}/metaflac
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-, root, root)
%doc doc/html
%{_includedir}/*
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*.m4

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.2.1-6.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Mar 17 2008 Miroslav Lichvar <mlichvar@redhat.com> 1.2.1-4
- speed up decoding
- CFLAGS cleanup

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.1-3
- Autorebuild for GCC 4.3

* Tue Jan 29 2008 Miroslav Lichvar <mlichvar@redhat.com> 1.2.1-2
- fix building with gcc-4.3 
- reenable some assembly optimizations
- hide private libFLAC symbols (#285961)
- update license tag
- add %%check
- remove -maltivec from CFLAGS

* Mon Sep 17 2007 - Bastien Nocera <bnocera@redhat.com> - 1.2.1-1
- Update to 1.2.1

* Wed Sep 12 2007 - Bastien Nocera <bnocera@redhat.com> - 1.2.0-3
- Make a few functions hidden, to try and avoid textrels
- Disable optimisations on x86 for the same reason
  (#285961)

* Tue Sep 11 2007 - Bastien Nocera <bnocera@redhat.com> - 1.2.0-2
- Update GNU stack patch to cover all the NASM sources used

* Mon Sep 10 2007 - Bastien Nocera <bnocera@redhat.com> - 1.2.0-1
- Update for 1.20 and drop obsolete patches (#285161)

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 1.1.4-5
- Rebuild for build ID

* Thu Apr 12 2007 - Bastien Nocera <bnocera@redhat.com> - 1.1.4-4
- The byteSwap symbol shouldn't be global, reported by Joe Orton
  <jorton@redhat.com> (#215920)

* Wed Feb 14 2007 - Bastien Nocera <bnocera@redhat.com> - 1.1.4-3
- Also include the new pkgconfig files

* Wed Feb 14 2007 - Bastien Nocera <bnocera@redhat.com> - 1.1.4-2
- Update link-ogg patch for 1.1.4

* Wed Feb 14 2007 - Bastien Nocera <bnocera@redhat.com> - 1.1.4-1
- Update to upstream 1.1.4

* Tue Feb 13 2007 - Bastien Nocera <bnocera@redhat.com> - 1.1.3-2
- A few fixes from the the Fedora merge review
- Remove the static library

* Tue Feb 13 2007 - Bastien Nocera <bnocera@redhat.com> - 1.1.3-1
- Update with work from Matthias Clasen <mclasen@redhat.com> up
  to upstream 1.1.3 (#229462)
- Remove xmmx-flac Obsolete, as we don't ship the xmms plugin

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.1.2-27
- rebuild
- Try building w/ glib2-devel

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 1.1.2-26
- rebuild for -devel deps

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1.2-25.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1.2-25.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Apr 21 2005 Warren Togami <wtogami@redhat.com> - 1.1.2-25
- Fix buildreqs  (#154649 thias)
- obsolete older xmms-flac

* Mon Apr  4 2005 Elliot Lee <sopwith@redhat.com> - 1.1.2-24
- Removed xmms-flac subpackage

* Tue Mar 29 2005 John (J5) Palmieri <johnp@redhat.com> 1.1.2-2
- Rebuild (flac picked up a dependancy on it's older version)

* Mon Mar 28 2005 John (J5) Palmieri <johnp@redhat.com> 1.1.2-1
- Update to upstream version 1.1.2
- Replace flac-1.1.0-libtool.patch with flac-1.1.2-libtool.patch

* Wed Mar 02 2005 John (J5) Palmieri <johnp@redhat.com> 1.1.0-9
- rebuild for gcc 4.0

* Wed Feb 23 2005 Colin Walters <walters@redhat.com> 1.1.0-8
- New patch flac-1.1.0-gnu-stack.patch from Ulrich Drepper to mark asm
  as not requiring an executable stack

* Thu Jul 15 2004 Tim Waugh <twaugh@redhat.com> 1.1.0-7
- Fixed warnings in shipped m4 file.

* Mon Jun 21 2004 Colin Walters <walters@redhat.com> 1.1.0-6
- BuildRequire glib-devel for xmms plugin
- BuildRequire nasm

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Apr 04 2004 Warren Togami <wtogami@redhat.com> 1.1.0-4
- #119551 flac-xmms -> xmms-flac to match fedora.us and freshrpms.net
- Obsoletes flac-libs to upgrade smoothly from fedora.us

* Thu Mar 11 2004 Bill Nottingham <notting@redhat.com> 1.1.0-3
- fix x86_64 linkage (#117893)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Aug  6 2003 Bill Nottingham <notting@redhat.com> 1.1.0-1
- initial build
