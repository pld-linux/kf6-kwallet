# TODO:
# Not packaged:
# - build with kf6-gpgmepp
#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeframever	6.19
%define		qt_ver		6.5.0
%define		kfname		kwallet

Summary:	Safe desktop-wide storage for passwords
Summary(pl.UTF-8):	Bezpieczny schowek na hasła dla całego środowiska
Name:		kf6-%{kfname}
Version:	6.19.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	4f4c2e65367071c4ed3c75fe98687175
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6DBus-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6Test-devel >= %{qt_ver}
BuildRequires:	Qt6Widgets-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gpgmepp-devel >= 1.7.0
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
Requires(post,postun):	desktop-file-utils
Requires:	Qt6DBus >= %{qt_ver}
Requires:	Qt6Gui >= %{qt_ver}
Requires:	Qt6Widgets >= %{qt_ver}
Requires:	gpgmepp >= 1.7.0
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
Provides:	kf5-kwallet-service = %{version}
Obsoletes:	kf5-kwallet-service < 6
%requires_eq_to Qt6Core Qt6Core-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This framework contains two main components:
- Interface to KWallet, the safe desktop-wide storage for passwords on
  KDE work spaces.
- The kwalletd used to safely store the passwords on KDE work spaces.

%description -l pl.UTF-8
Ten szkielet składa się z dwóch komponentów:
- interfejsu do KWallet - bezpiecznego schowka na hasła dla przestreni
  roboczych KDE
- usługi kwalletd służącej do bezpiecznego przechowywania haseł w
  przestrzeniach roboczych KDE

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Gui-devel >= %{qt_ver}

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

# kwallet6-query and kwalletd6 domains
%find_lang %{kfname} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kfname}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/ksecretd
%attr(755,root,root) %{_bindir}/kwallet-query
%attr(755,root,root) %{_bindir}/kwalletd6
%{_libdir}/libKF6Wallet.so.*.*.*
%ghost %{_libdir}/libKF6Wallet.so.6
%{_libdir}/libKF6WalletBackend.so.*.*.*
%ghost %{_libdir}/libKF6WalletBackend.so.6
%{_desktopdir}/org.kde.ksecretd.desktop
%{_datadir}/dbus-1/interfaces/kf6_org.kde.KWallet.xml
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.kwallet.service
%{_datadir}/dbus-1/services/org.kde.kwalletd5.service
%{_datadir}/dbus-1/services/org.kde.kwalletd6.service
%{_datadir}/dbus-1/services/org.kde.secretservicecompat.service
%{_datadir}/qlogging-categories6/kwallet.categories
%{_datadir}/qlogging-categories6/kwallet.renamecategories
%{_datadir}/xdg-desktop-portal/portals/kwallet.portal
%{_datadir}/knotifications6/ksecretd.notifyrc
%{_mandir}/man1/kwallet-query.1*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF6Wallet.so
%{_includedir}/KF6/KWallet
%{_libdir}/cmake/KF6Wallet
