#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# Not packaged:
# - build with kf6-gpgmepp
%define		kdeframever	5.249.0
%define		qtver		5.15.2
%define		kfname		kwallet

Summary:	Safe desktop-wide storage for passwords
Name:		kf6-%{kfname}
Version:	5.249.0
Release:	0.1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/unstable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	21629b0c4d4c3e5f3d507686707727d7
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gpgme-c++-devel >= 1:1.7.0
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kconfig-devel >= %{version}
BuildRequires:	kf6-kconfigwidgets-devel >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	kf6-kdbusaddons-devel >= %{version}
BuildRequires:	kf6-kdoctools-devel >= %{version}
BuildRequires:	kf6-ki18n-devel >= %{version}
BuildRequires:	kf6-knotifications-devel >= %{version}
BuildRequires:	kf6-kservice-devel >= %{version}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{version}
BuildRequires:	kf6-kwindowsystem-devel >= %{version}
BuildRequires:	libgcrypt-devel >= 1.5.0
BuildRequires:	ninja
BuildRequires:	qca-qt6-devel
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6DBus >= %{qtver}
Requires:	Qt6Gui >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Requires:	gpgme-c++ >= 1:1.7.0
Requires:	kf6-dirs
Requires:	kf6-kconfig >= %{version}
Requires:	kf6-kconfigwidgets >= %{version}
Requires:	kf6-kcoreaddons >= %{version}
Requires:	kf6-kdbusaddons >= %{version}
Requires:	kf6-ki18n >= %{version}
Requires:	kf6-knotifications >= %{version}
Requires:	kf6-kservice >= %{version}
Requires:	kf6-kwidgetsaddons >= %{version}
Requires:	kf6-kwindowsystem >= %{version}
Requires:	libgcrypt >= 1.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
This framework contains two main components:
- Interface to KWallet, the safe desktop-wide storage for passwords on
  KDE work spaces.
- The kwalletd used to safely store the passwords on KDE work spaces.

The library can be built alone, without kwalletd, by setting the
`BUILD_KWALLETD` option to `OFF`.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Gui-devel >= %{qtver}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/kwallet-query
%attr(755,root,root) %{_bindir}/kwalletd6
%attr(755,root,root) %{_libdir}/libKF6Wallet.so.*.*
%ghost %{_libdir}/libKF6Wallet.so.6
%attr(755,root,root) %{_libdir}/libKF6WalletBackend.so.*.*
%ghost %{_libdir}/libKF6WalletBackend.so.6
%{_desktopdir}/org.kde.kwalletd6.desktop
%{_datadir}/dbus-1/interfaces/kf6_org.kde.KWallet.xml
%{_datadir}/dbus-1/services/org.kde.kwalletd5.service
%{_datadir}/dbus-1/services/org.kde.kwalletd6.service
%{_datadir}/knotifications6/kwalletd6.notifyrc
%{_datadir}/qlogging-categories6/kwallet.categories
%{_datadir}/qlogging-categories6/kwallet.renamecategories
%{_mandir}/man1/kwallet-query.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KWallet
%{_libdir}/cmake/KF6Wallet
%{_libdir}/libKF6Wallet.so
