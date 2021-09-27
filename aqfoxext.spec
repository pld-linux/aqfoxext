#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	AqFoxExt - extension library for the FOX toolkit
Summary(pl.UTF-8):	AqFoxExt - biblioteka rozszerzeń toolkitu FOX
Name:		aqfoxext
# "beta" suffix is specific to particular version (there won't be 0.9.9 non-beta)
Version:	0.9.9beta
Release:	2
License:	LGPL v2.1+ with BSD parts
Group:		Libraries
# https://www.aquamaniac.de/sites/download/packages.php
Source0:	https://www.aquamaniac.de/sites/download/download.php?package=15&release=01&file=01&dummy=/%{name}-%{version}.tar.gz
# Source0-md5:	8556d1cc5a99a102491dab95a31eeb64
Patch0:		%{name}-pc.patch
URL:		https://www.aquamaniac.de/sites/aqfinance/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	fox16-devel >= 1.6
BuildRequires:	gwenhywfar-devel >= 4
BuildRequires:	gwenhywfar-fox-devel >= 4
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
Requires:	gwenhywfar-fox >= 4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Extension library for the FOX toolkit used by AqFinance and AqRadBase.

%description -l pl.UTF-8
Biblioteka rozszerzeń toolkitu FOX wykorzystywana przez AqFinance oraz
AqRadBase.

%package devel
Summary:	Header files for AqFoxExt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki AqFoxExt
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	fox16-devel >= 1.6
Requires:	gwenhywfar-devel >= 4
Requires:	gwenhywfar-fox-devel >= 4

%description devel
Header files for AqFoxExt library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki AqFoxExt.

%package static
Summary:	Static AqFoxExt library
Summary(pl.UTF-8):	Statyczna biblioteka AqFoxExt
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static AqFoxExt library.

%description static -l pl.UTF-8
Statyczna biblioteka AqFoxExt.

%prep
%setup -q
%patch0 -p1

# workaround to build without headers installed
install -d aqfoxext
cd aqfoxext
ln -sf ../src/*.h ../src/*.hpp ../src/widgets/*.hpp ../src/external/*.h ../src/external/x11 .

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libaqfoxext.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_libdir}/libaqfoxext.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaqfoxext.so.0
%{_datadir}/aqfoxext

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaqfoxext.so
%{_includedir}/aqfoxext
%{_pkgconfigdir}/aqfoxext.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libaqfoxext.a
%endif
