# The full MythTV Version string is computed from the output of git describe.
%global vers_string v35.0-45-g187b4cc6ca

# The git date of last commit on mythtv repo
# git_date=$(git log -1 --format=%cd --date=format:"%Y%m%d")
%global git_date 20251203

# Specfile for building MythTV and MythPlugins RPMs from a git checkout.
#
# by:   Chris Petersen <cpetersen@mythtv.org>
#       Jarod Wilson <jarod@wilsonet.com>
#       Richard Shaw <hobbes1069@gmail.com>
#
#  Modified/Extended from the great work of:
#     Axel Thimm <Axel.Thimm@ATrpms.net>
#     David Bussenschutt <buzz@oska.com>
#     and others; see changelog at bottom for details.
#
# The latest canonical upstream version of this file can be found at:
#
#     https://github.com/MythTV/packaging/tree/master/rpm
#
# The latest RPM Fusion version can be found at:
#
#     https://pkgs.rpmfusion.org/cgit/free/mythtv.git/
#
# Note:
#
#     This spec relies upon several files included in the RPM Fusion mythtv
#     src.rpm file.  Please install it into your build tree before trying to
#     build anything with this spec.
#
# Explanation of options:
#
# --with proc_opt           Enable MythTV's optimized processor detection code
#                               and override RPM's defaults.
# --with debug              Enable debug mode
#
# The following options are enabled by default.  Use these options to disable:
#
# --without vdpau           Disable VDPAU support
# --without vaapi           Disable VAAPI support
# --without perl            Disable building of the perl bindings
# --without php             Disable building of the php bindings
# --without python          Disable building of the python bindings
#
# # All plugins get built by default, but you can disable them as you wish:
#
# --without mytharchive
# --without mythbrowser
# --without mythgame
# --without mythmusic
# --without mythnetvision
# --without mythnews
# --without mythweather
# --without mythzoneminder
#

################################################################################
%define _lto_cflags %{nil}
%global py_prefix python3

# These values are computed from git describe provided earlier
%global githash %(c=%{vers_string}; echo $c|cut -d"-" -f3)
%global shorthash %(c=%{githash}; echo ${c:1:11})
%global commits %(c=%{vers_string}; echo $c|cut -d"-" -f2)
%global rel_string .%{commits}.%{git_date}git%{shorthash}

# A list of which applications we want to put into the desktop menu system
%global desktop_applications mythfrontend mythtv-setup

# This is the correct folder for firewalld service files, even on x86_64
# It is not used for shared objects
%global fw_services %{_prefix}/lib/firewalld/services

# fedora >= 43 normalizes python dist-info folder name
%if 0%{?fedora} >= 43
%global distinfo mythtv-%{version}.dist-info
%else
%global distinfo MythTV-%{version}.dist-info
%endif

#
# Basic descriptive tags for this package:
#
Name:           mythtv
Version:        35.0
Release:        11%{rel_string}%{?dist}
Summary:        A digital video recorder (DVR) application

# The primary license is GPLv2+, but bits are borrowed from a number of
# projects... For a breakdown of the licensing, see PACKAGE-LICENSING.
License:        GPLv2+ and LGPLv2+ and LGPLv2 and (GPLv2 or QPL) and (GPLv2+ or LGPLv2+)
URL:            http://www.mythtv.org/
Source0:        https://github.com/MythTV/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         https://github.com/MythTV/%{name}/compare/v%{version}..%{shorthash}.patch
Patch1:         %{name}-space_in_GB.patch

%global major_rel %(c=%{version}; echo $c|cut -d"." -f1)

################################################################################

# Set "--with proc_opt" to let mythtv autodetect your CPU and run its
# processor-specific optimizations.  It seems to cause compile problems on many
# systems (particularly x86_64), so it is classified by the MythTV developers
# as "use at your own risk."
%bcond_with proc_opt

# Set "--without debug" to disable MythTV debug compile mode
%bcond_without debug

# The following options are enabled by default.  Use --without to disable them
%bcond_without vdpau
%bcond_without vaapi
%bcond_without sdnotify
%bcond_without perl
%bcond_without php
%bcond_without python
%bcond_without pulseaudio

# All plugins get built by default, but you can disable them as you wish
%bcond_without plugins
%bcond_without mytharchive
%if 0%{?fedora}
%bcond_without mythbrowser
%else
%bcond_with mythbrowser
%endif
%bcond_without mythgame
%bcond_without mythmusic
%bcond_without mythnews
%bcond_without mythweather
%bcond_without mythzoneminder
%bcond_with mythnetvision

################################################################################
#
### THE BELOW IS NOW AUTOMATED BY SCRIPTS IN SCM ###
#
# From the mythtv git repository with the appropriate branch checked out:
# Example: git diff -p --stat v0.26.0 > mythtv-0.26-fixes.patch
# Also update ChangeLog with git log v0.28..HEAD > ChangeLog
# and update define vers_string to v0.28-52-ge6a60f7 with git describe

Source3:   mythtv.sysusers
Source10:  %{name}-PACKAGE-LICENSING
Source11:  %{name}-ChangeLog
Source104: %{name}.logrotate.sysd
Source105: mythbackend.service
Source106: mythfrontend.png
Source107: mythfrontend.desktop
Source108: %{name}-setup.png
Source109: %{name}-setup.desktop
Source111: 99-mythbackend.rules
Source112: mythjobqueue.service
Source113: mythdb-optimize.service
Source114: mythdb-optimize.timer
# firewalld config for new web application
# https://www.mythtv.org/wiki/Web_Application
Source115: mythtv-webfrontend.xml
Source116: mythtv-webbackend.xml

# Global MythTV and Shared Build Requirements

# Use systemd
BuildRequires:  systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

# sysusers config is now required
BuildRequires:  systemd-rpm-macros
%{?sysusers_requires_compat}

BuildRequires:  gcc-c++ lzo-devel
# For binary diff support
BuildRequires:  git-core
BuildRequires:  perl-generators
BuildRequires:  desktop-file-utils
BuildRequires:  qt5-qtbase-devel >= 5.2
BuildRequires:  qt5-qtscript-devel >= 5.2
# qt5-qtwebkit has been retired in latest epel, effecting mythbrowser plugin
%{?fedora:BuildRequires:  qt5-qtwebkit-devel >= 5.2}
BuildRequires:  freetype-devel >= 2
BuildRequires:  mariadb-connector-c-devel
BuildRequires:  libcec-devel >= 1.7
BuildRequires:  libvpx-devel
BuildRequires:  lm_sensors-devel
BuildRequires:  lirc-devel
BuildRequires:  nasm

# X, and Xv video support
BuildRequires:  libXmu-devel
BuildRequires:  libXv-devel
### Will not likely be required in a future release
BuildRequires:  libXxf86vm-devel
BuildRequires:  libXinerama-devel
###
BuildRequires:  libXrandr-devel
BuildRequires:  mesa-libGLU-devel
%ifarch %arm
BuildRequires:  mesa-libGLES-devel
%endif
BuildRequires:  xorg-x11-proto-devel

# OpenGL video output and vsync support
BuildRequires:  libGL-devel
BuildRequires:  libGLU-devel
BuildRequires:  libXNVCtrl-devel

# Misc A/V format support
BuildRequires:  fftw-devel >= 3
BuildRequires:  flac-devel >= 1.0.4
BuildRequires:  lame-devel
BuildRequires:  libbluray-devel
BuildRequires:  libcdio-devel libcdio-paranoia-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  libogg-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel >= 1.0
BuildRequires:  taglib-devel >= 1.7
BuildRequires:  x264-devel
BuildRequires:  x265-devel
BuildRequires:  xvidcore-devel >= 0.9.1
BuildRequires:  exiv2-devel

# Audio framework support
BuildRequires:  sox-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  pipewire-jack-audio-connection-kit-devel
%if %{with pulseaudio}
BuildRequires:  pulseaudio-libs-devel
%endif
BuildRequires:  avahi-compat-libdns_sd-devel

# Bluray support
BuildRequires:  ant java-devel
BuildRequires:  libxml2-devel
#BuildRequires:  libudf-devel

# Subtitle support
BuildRequires:  libass-devel

# Need dvb headers to build in dvb support
BuildRequires:  kernel-headers

# FireWire cable box support
%if 0%{?fedora}
BuildRequires:  libavc1394-devel
BuildRequires:  libiec61883-devel
BuildRequires:  libraw1394-devel
%endif

# Tuner support
BuildRequires:  hdhomerun-devel

# For ttvdb.py, not available in EPEL
BuildRequires: %{py_prefix}-requests
BuildRequires: %{py_prefix}-requests-cache

%if %{with vdpau}
BuildRequires:  libvdpau-devel
%endif

%if %{with vaapi}
BuildRequires:  libva-devel
%endif

%if %{with sdnotify}
BuildRequires:  systemd-devel
%endif

%if %{with mythgame}
BuildRequires:  minizip-compat-devel
%endif


# API Build Requirements

%if %{with perl}
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(DBI)
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(Net::UPnP::QueryResponse)
BuildRequires:  perl(Net::UPnP::ControlPoint)
BuildRequires:  perl(DBD::mysql)
BuildRequires:  perl(IO::Socket::INET6)
%endif

%if %{with php}
# No php specific requirements yet.
%endif

%if %{with python}
BuildRequires:  %{py_prefix}-setuptools
BuildRequires:  %{py_prefix}-pip
BuildRequires:  %{py_prefix}-wheel
BuildRequires:  %{py_prefix}-devel
BuildRequires:  %{py_prefix}-mysqlclient
BuildRequires:  %{py_prefix}-lxml
%endif

# Plugin Build Requirements

%if %{with plugins}

%if %{with mythgame}
BuildRequires:  zlib-devel
%endif

%if %{with mythnews}
%endif

BuildRequires: ncurses-devel
BuildRequires: soundtouch-devel
BuildRequires: libzip-devel
BuildRequires: expat-devel

%if %{with mythweather}
Requires:       mythweather      >= %{version}
BuildRequires:  perl(XML::Simple)
Requires:       perl(XML::Simple)
Requires:       perl(LWP::Simple)
BuildRequires:  perl(DateTime::Format::ISO8601)
Requires:       perl(DateTime::Format::ISO8601)
BuildRequires:  perl(XML::XPath)
Requires:       perl(XML::XPath)
BuildRequires:  perl(Date::Manip)
Requires:       perl(Date::Manip)
BuildRequires:  perl(Image::Size)
Requires:       perl(Image::Size)
BuildRequires:  perl(SOAP::Lite)
Requires:       perl(SOAP::Lite)
BuildRequires:  perl(JSON)
Requires:       perl(JSON)
%endif

%if %{with mythzoneminder}
%endif

%if %{with mythnetvision}
BuildRequires:  %{py_prefix}-pycurl
BuildRequires:  %{py_prefix}-lxml
BuildRequires:  %{py_prefix}-oauth
BuildRequires:  %{py_prefix}-urllib3
%endif

%endif

################################################################################
# Requirements for the mythtv meta package

Requires:  mythtv-libs%{?_isa}        = %{version}-%{release}
Requires:  mythtv-backend%{?_isa}     = %{version}-%{release}
Requires:  mythtv-base-themes%{?_isa} = %{version}-%{release}
Requires:  mythtv-common%{?_isa}      = %{version}-%{release}
Requires:  mythtv-docs                = %{version}-%{release}
Requires:  mythtv-frontend%{?_isa}    = %{version}-%{release}
Requires:  mythtv-setup%{?_isa}       = %{version}-%{release}
Requires:  perl-MythTV                = %{version}-%{release}
Requires:  php-MythTV                 = %{version}-%{release}
Requires:  %{py_prefix}-MythTV  = %{version}-%{release}
%if %{with plugins}
Requires:  mythplugins%{?_isa}        = %{version}-%{release}
%endif
# Reminder this one is noarch - and not a sub-package (no EVR)
Recommends:  mythweb
Requires:  mythffmpeg%{?_isa}         = %{version}-%{release}
#Requires:  mariadb
#Requires:  mariadb-server
%{?fedora:Recommends:  xmltv}

# Generate the required mythtv-frontend-api version string here so we only
# have to do it once.
%global mythfeapiver %(echo %{version} | awk -F. '{print $1 "." $2}')

################################################################################

%description
MythTV provides a unified graphical interface for recording and viewing
television programs. Refer to the mythtv package for more information.

There are also several add-ons and themes available. In order to facilitate
installations with smart/apt-get/yum and other related package
resolvers this meta-package can be used to install all in one sweep.

MythTV implements the following DVR features, and more, with a
unified graphical interface:

- Basic 'live-tv' functionality. Pause/Fast Forward/Rewind "live" TV.
- Video compression using RTjpeg or MPEG-4, and support for DVB and
  hardware encoder cards/devices.
- Program listing retrieval using XMLTV
- Themable, semi-transparent on-screen display
- Electronic program guide
- Scheduled recording of TV programs
- Resolution of conflicts between scheduled recordings
- Basic video editing

################################################################################

%package docs
Summary:   MythTV documentation
BuildArch: noarch

%description docs
The MythTV documentation, database initialization file
and miscellaneous other bits and pieces.

################################################################################

%package libs
Summary:   Library providing mythtv support

%{?rhel:BuildRequires: epel-rpm-macros}
Requires:  freetype%{?_isa} >= 2
Requires:  qt5-qtbase-mysql%{?_isa}
Requires:  libudisks2%{?_isa}

# Handle package obsoletes here as this is the only "common" package.
# mythgallery is dead
Obsoletes:      mythgallery < 31
# mythnetvision is buggy and doesn't want to build with python3-urllib3
%if !%{with mythnetvision}
Obsoletes:      mythnetvision < 31
%endif

%description libs
Common library code for MythTV and add-on modules (development)
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

################################################################################

%package devel
Summary:   Development files for mythtv

Requires:  mythtv-libs%{?_isa} = %{version}-%{release}

BuildRequires:  mariadb-connector-c-devel
Requires:  qt5-qtbase-devel%{?_isa} >= 5.2
Requires:  qt5-qtscript-devel%{?_isa} >= 5.2
# qt5-qtwebkit has been retired in latest epel, affecting mythbrowser plugin
%{?fedora:BuildRequires:  qt5-qtwebkit-devel >= 5.2}

%description devel
This package contains the header files and libraries for developing
add-ons for mythtv.

################################################################################

%package base-themes
Summary: Core user interface themes for mythtv

%description base-themes
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv-docs package for more information.

This package contains the base themes for the mythtv user interface.

################################################################################

%package frontend
Summary:   Client component of mythtv (a DVR)
Requires:  freetype%{?_isa}
%if 0%{?fedora}
Requires:  lame
%endif
Requires:  perl(XML::Simple)
Requires:  mythtv-common%{?_isa}       = %{version}-%{release}
Requires:  mythtv-base-themes%{?_isa}  = %{version}-%{release}
	
# RHBZ 1838780 - mariadb lacks mysql provides on el8
Requires:       (mysql%{?_isa} >= 5 or mariadb%{?_isa})

Requires:  %{py_prefix}-MythTV       = %{version}-%{release}
Recommends: libaacs%{?_isa}
%{?fedora:Requires:  google-droid-sans-mono-fonts}
%{?fedora:Recommends:  mesa-vdpau-drivers%{?_isa}}
Provides:  mythtv-frontend-api%{?_isa} = %{mythfeapiver}

# Mythfrontend dvd menu support comes from libdvdcss
# https://www.mythtv.org/wiki/Using_MythTV#Optical_Disks
Recommends: libdvdcss

# Disable the startup overview on newer Gnome desktops to allow proper kiosk mode
Recommends: gnome-shell-extension-no-overview

%description frontend
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the client software, which provides a
front-end for playback and configuration.  It requires access to a
mythtv-backend installation, either on the same system or one
reachable via the network.

################################################################################

%package backend
Summary:    Server component of mythtv (a DVR)
%if 0%{?fedora}
Requires:   lame
%endif
Requires:   mythtv-common%{?_isa} = %{version}-%{release}
Requires:   mythtv-libs%{?_isa}   = %{version}-%{release}
Requires:   mythtv-setup%{?_isa}
Requires:   %{py_prefix}-requests
Requires:   %{py_prefix}-requests-cache

Requires(pre): shadow-utils
Conflicts:  xmltv-grabbers < 0.5.37

%description backend
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the server software, which provides video
and audio capture and encoding services.  In order to be useful, it
requires a mythtv-frontend installation, either on the same system or
one reachable via the network.

################################################################################

%package setup
Summary:   Setup the mythtv backend
Requires:  freetype%{?_isa}
Requires:  mythtv-backend%{?_isa} = %{version}-%{release}
Requires:  mythtv-base-themes%{?_isa} = %{version}
Requires:  google-droid-sans-fonts

# Needed for svg channel icon support
Requires: qt5-qtsvg

%description setup
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the setup software for configuring the
mythtv backend.

################################################################################

%package common
Summary: Common components needed by multiple other MythTV components
# For ttvdb.py
Requires:   %{py_prefix}-requests
Requires:   %{py_prefix}-requests-cache

%description common
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains components needed by multiple other MythTV components.

################################################################################
################################################################################

%package -n mythffmpeg
Summary: MythTV build of FFmpeg

%description -n mythffmpeg
Several MythTV utilities interact with FFmpeg, which changes its parameters
often enough to make it a hassle to support the variety of versions used by
MythTV users.  This is a snapshot of the FFmpeg code so that MythTV utilities
can interact with a known verion.

################################################################################

%if %{with perl}

%package -n perl-MythTV
Summary:        Perl bindings for MythTV
BuildArch:      noarch

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(DBD::mysql)
Requires:       perl(Net::UPnP)
Requires:       perl(Net::UPnP::ControlPoint)

%description -n perl-MythTV
Provides a perl-based interface to interacting with MythTV.

%endif

################################################################################

%if %{with php}

%package -n php-MythTV
Summary:        PHP bindings for MythTV
BuildArch:      noarch

%description -n php-MythTV
Provides a PHP-based interface to interacting with MythTV.

%endif

################################################################################

%if %{with python}

%package -n %{py_prefix}-MythTV
Summary:        Python bindings for MythTV
%{?python_provide:%python_provide python3-%{name}}
Obsoletes:      python2-MythTV < 30.0-9.20190601git6bd8cd4993
BuildArch:      noarch

Requires:       %{py_prefix}-mysqlclient
Requires:       %{py_prefix}-lxml

%description -n %{py_prefix}-MythTV
Provides a python-based interface to interacting with MythTV.

%endif

################################################################################

%if %{with plugins}

# Meta package for all mythtv plugins
%package -n mythplugins

Summary:  Main MythTV plugins

%if %{with mythmusic}
Requires:  mythmusic%{?_isa}      = %{version}-%{release}
%endif
%if %{with mythweather}
Requires:  mythweather%{?_isa}    = %{version}-%{release}
%endif
%if %{with mythgame}
Requires:  mythgame%{?_isa}       = %{version}-%{release}
%endif
%if %{with mythnews}
Requires:  mythnews%{?_isa}       = %{version}-%{release}
%endif
%if %{with mythbrowser}
Requires:  mythbrowser%{?_isa}    = %{version}-%{release}
%endif
%if %{with mytharchive}
Requires:  mytharchive%{?_isa}    = %{version}-%{release}
%endif
%if %{with mythzoneminder}
Requires:  mythzoneminder%{?_isa} = %{version}-%{release}
%endif
%if %{with mythnetvision}
Requires:  mythnetvision%{?_isa}  = %{version}-%{release}
%endif

%description -n mythplugins
This is a consolidation of all the official MythTV plugins that used to be
distributed as separate downloads from mythtv.org.

################################################################################
%if %{with mytharchive}

%package -n mytharchive
Summary:   A module for MythTV for creating and burning DVDs

Requires:  mythtv-frontend-api%{?_isa} = %{mythfeapiver}
Requires:  wodim
Requires:  dvd+rw-tools%{?_isa} >= 5.21.4.10.8
Requires:  dvdauthor%{?_isa} >= 0.6.11
Requires:  ffmpeg%{?_isa} >= 0.4.9
Requires:  mjpegtools%{?_isa} >= 1.6.2
Requires:  genisoimage%{?_isa}
Requires:  %{py_prefix}-mysqlclient
Requires:  %{py_prefix}-pillow
Requires:  pmount%{?_isa}

%description -n mytharchive
MythArchive is a new plugin for MythTV that lets you create DVDs from
your recorded shows, MythVideo files and any video files available on
your system.

%endif
################################################################################
%if %{with mythbrowser}

%package -n mythbrowser
Summary:   A small web browser module for MythTV
Requires:  mythtv-frontend-api%{?_isa} = %{mythfeapiver}

%description -n mythbrowser
MythBrowser is a full fledged web-browser (multiple tabs) to display
webpages in full-screen mode. Simple page navigation is possible.
Starting with version 0.13 it also has full support for mouse driven
navigation (right mouse opens and clos es the popup menu).

MythBrowser also contains a BookmarkManager to manage the website
links in a simple mythplugin.

%endif
################################################################################
%if %{with mythgame}

%package -n mythgame
Summary:   A game frontend (xmame, nes, snes, pc) for MythTV
Requires:  mythtv-frontend-api%{?_isa} = %{mythfeapiver}

%description -n mythgame
A game frontend (xmame, nes, snes, pc) for MythTV.

%endif
################################################################################
%if %{with mythmusic}

%package -n mythmusic
Summary:   The music player add-on module for MythTV
Requires:  mythtv-frontend-api%{?_isa} = %{mythfeapiver}

%description -n mythmusic
Music add-on for mythtv.

%endif
################################################################################
%if %{with mythnews}

%package -n mythnews
Summary:   An RSS news feed plugin for MythTV
Requires:  mythtv-frontend-api%{?_isa} = %{mythfeapiver}

%description -n mythnews
An RSS news feed reader plugin for MythTV.

%endif
################################################################################
%if %{with mythweather}

%package -n mythweather
Summary:   A MythTV module that displays a weather forecast
Requires:  mythtv-frontend-api%{?_isa} = %{mythfeapiver}
Requires:  perl(XML::SAX::Base)

%description -n mythweather
A MythTV module that displays a weather forecast.

%endif
################################################################################
%if %{with mythzoneminder}

%package -n mythzoneminder
Summary:   A module for MythTV for camera security and surveillance
Requires:  mythtv-frontend-api%{?_isa} = %{mythfeapiver}

%description -n mythzoneminder
MythZoneMinder is a plugin to interface to some of the features of
ZoneMinder. You can use it to view a status window similar to the
console window in ZM. Also there are screens to view live camera shots
and replay recorded events.

%endif
################################################################################
%if %{with mythnetvision}

%package -n mythnetvision
Summary:   A MythTV module for Internet video on demand
Requires:  mythtv-frontend-api%{?_isa} = %{mythfeapiver}
Requires:  mythbrowser%{?_isa} = %{version}-%{release}
Requires:  %{py_prefix}-MythTV = %{version}-%{release}
Requires:  %{py_prefix}-pycurl
Requires:  %{py_prefix} >= 2.5
Requires:  %{py_prefix}-lxml
Requires:  %{py_prefix}-urllib3

%description -n mythnetvision
A MythTV module that supports searching and browsing of Internet video
on demand content.

%endif
################################################################################

# End of plugins
%endif

################################################################################

%prep
%autosetup -S git -p1 -n %{name}-%{version}


# Remove exe permissions
find . -type f -name "*.cpp" -exec chmod 0644 '{}' \;

# Install ChangeLog
install -m 0644 %{SOURCE11} ./ChangeLog

pushd mythtv

# Set the mythtv --version string
cat > EXPORTED_VERSION <<EOF
SOURCE_VERSION=%{vers_string}
BRANCH=fixes/%{major_rel}
EOF

# Drop execute permissions on contrib bits, since they'll be %%doc
    find contrib/ -type f -exec chmod -x "{}" \;

# Put perl bits in the right place and set opt flags
    sed -i -e 's#perl Makefile.PL#%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"#' \
        bindings/perl/Makefile

# Install other source files
    cp -a %{SOURCE10} ./PACKAGE-LICENSING
    cp -a %{SOURCE106} %{SOURCE107} %{SOURCE108} %{SOURCE109} .
popd

################################################################################

%build

# First, we build MythTV
pushd mythtv

# Similar to 'percent' configure, but without {_target_platform} and
# {_exec_prefix} etc... MythTV no longer accepts the parameters that the
# configure macro passes, so we do this manually.
./configure \
    --qmake=%{_bindir}/qmake-qt5                \
    --prefix=%{_prefix}                         \
    --libdir=%{_libdir}                         \
    --libdir-name=%{_lib}                       \
    --mandir=%{_mandir}                         \
%if ! %{with vdpau}
    --disable-vdpau                             \
%endif
%if ! %{with vaapi}
    --disable-vaapi                             \
%endif
    --python=%{__python3}                       \
    --enable-libvpx                             \
    --enable-libmp3lame                         \
    --enable-libx264                            \
    --enable-libx265                            \
    --enable-libxvid                            \
%if !%{with perl}
    --without-bindings=perl                     \
%endif
%if !%{with php}
    --without-bindings=php                      \
%endif
%if %{without python}
    --without-bindings=python                   \
%endif
    --extra-cflags="%{optflags} -fomit-frame-pointer -fno-devirtualize" \
    --extra-cxxflags="%{optflags} -fomit-frame-pointer -fno-devirtualize" \
%ifarch %{ix86}
    --cpu=i686 --tune=i686 --enable-mmx \
%endif
%if %{with proc_opt}
    --enable-proc-opt \
%endif
%if %{with debug}
    --compile-type=debug
%else
    --compile-type=release
%endif

# Make
%make_build V=1
popd

# Prepare to build the plugins
    mkdir fakeroot
    temp=`pwd`/fakeroot
    make -C mythtv install INSTALL_ROOT=$temp
    export LD_LIBRARY_PATH=$temp%{_libdir}:$LD_LIBRARY_PATH

# Next, we build the plugins
%if %{with plugins}
pushd mythplugins

# Fix things up so they can find our "temp" install location for mythtv-libs
    echo "QMAKE_PROJECT_DEPTH = 0" >> settings.pro
    find . -name \*.pro \
        -exec sed -i -e "s,INCLUDEPATH += .\+/include/mythtv,INCLUDEPATH += $temp%{_includedir}/mythtv," {} \; \
        -exec sed -i -e "s,DEPLIBS = \$\${SYSROOT}\$\${LIBDIR},DEPLIBS = $temp%{_libdir}," {} \; \
        -exec sed -i -e "s,\$\${PREFIX}/include/mythtv,$temp%{_includedir}/mythtv," {} \;
    echo "INCLUDEPATH -= \$\${PREFIX}/include" >> settings.pro
    echo "INCLUDEPATH -= \$\${SYSROOT}/\$\${PREFIX}/include" >> settings.pro
    echo "INCLUDEPATH -= %{_includedir}"       >> settings.pro
    echo "INCLUDEPATH += $temp%{_includedir}"  >> settings.pro
#    echo "LIBS *= -L$temp%{_libdir}"           >> settings.pro
    echo "QMAKE_LIBDIR += $temp%{_libdir}"     >> targetdep.pro

    ./configure \
        --prefix=${temp}%{_prefix} \
        --libdir=%{_libdir} \
        --libdir-name=%{_lib} \
    %if %{with mytharchive}
        --enable-mytharchive \
    %else
        --disable-mytharchive \
    %endif
    %if %{with mythbrowser}
        --enable-mythbrowser \
    %else
        --disable-mythbrowser \
    %endif
    %if %{with mythgame}
        --enable-mythgame \
    %else
        --disable-mythgame \
    %endif
    %if %{with mythmusic}
        --enable-mythmusic \
    %else
        --disable-mythmusic \
    %endif
    %if %{with mythnews}
        --enable-mythnews \
    %else
        --disable-mythnews \
    %endif
    %if %{with mythweather}
        --enable-mythweather \
    %else
        --disable-mythweather \
    %endif
    %if %{with mythzoneminder}
        --enable-mythzoneminder \
    %else
        --disable-mythzoneminder \
    %endif
    %if %{with mythnetvision}
        --enable-mythnetvision \
    %else
        --disable-mythnetvision \
    %endif
        --python=%{__python3}

%make_build V=1
    popd
%endif

################################################################################

%install
# First, install MythTV
pushd mythtv

    make install INSTALL_ROOT=%{buildroot}

    ln -s mythtv-setup %{buildroot}%{_bindir}/mythtvsetup
    mkdir -p %{buildroot}%{_localstatedir}/lib/mythtv
    mkdir -p %{buildroot}%{_localstatedir}/lib/mythvideo
    mkdir -p %{buildroot}%{_localstatedir}/cache/mythtv
    mkdir -p %{buildroot}%{_localstatedir}/log/mythtv
    mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
    mkdir -p %{buildroot}%{_unitdir}
    mkdir -p %{buildroot}%{_sysconfdir}/mythtv


# config/init files
    echo "# to be filled in by mythtv-setup" > %{buildroot}%{_sysconfdir}/mythtv/config.xml

    ### SystemD based setup. ###
    install -p -m 0644 %{SOURCE105} %{buildroot}%{_unitdir}/
    install -p -m 0644 %{SOURCE104} %{buildroot}%{_sysconfdir}/logrotate.d/mythtv
    # Install udev rules for devices that may initialize late in the boot
    # process so they are available for mythbackend.
    mkdir -p %{buildroot}/lib/udev/rules.d/
    install -p -m 0644 %{SOURCE111} %{buildroot}/lib/udev/rules.d/

    # Systemd unit file for mythjobqueue only backends.
    install -p -m 0644 %{SOURCE112} %{buildroot}%{_unitdir}/

    # Systemd unit files for database optimization
    install -p -m 0644 %{SOURCE113} %{buildroot}%{_unitdir}/
    install -p -m 0644 %{SOURCE114} %{buildroot}%{_unitdir}/
    install -p -m 0755 contrib/maintenance/optimize_mythdb.pl \
        %{buildroot}%{_bindir}/optimize_mythdb

    # sysusers config
    install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/mythtv.conf

# Desktop entries
    mkdir -p %{buildroot}%{_datadir}/pixmaps
    mkdir -p %{buildroot}%{_datadir}/applications
    for file in %{desktop_applications}; do
      install -p $file.png %{buildroot}%{_datadir}/pixmaps/$file.png
      desktop-file-install \
        --dir %{buildroot}%{_datadir}/applications    \
        --add-category Application        \
        --add-category AudioVideo         \
        $file.desktop
    done

    mkdir -p %{buildroot}%{_libdir}/mythtv/plugins

    mkdir -p %{buildroot}%{_datadir}/mythtv/build/
    install -p -m 644 settings.pro %{buildroot}%{_datadir}/mythtv/build/

popd

# Clean up some stuff we don't want to include
rm -f %{buildroot}%{_libdir}/libmythqjson.prl \
      %{buildroot}%{_libdir}/libmythzmq.la    \
      %{buildroot}%{_libdir}/pkgconfig/libmythzmq.pc

# MythPlugins
%if %{with plugins}
pushd mythplugins

    make install INSTALL_ROOT=%{buildroot}

%if %{with mythmusic}
    mkdir -p %{buildroot}%{_localstatedir}/lib/mythmusic
%endif
%if %{with mythgame}
    mkdir -p %{buildroot}%{_datadir}/mythtv/games/nes/{roms,screens}
    mkdir -p %{buildroot}%{_datadir}/mythtv/games/snes/{roms,screens}
    mkdir -p %{buildroot}%{_datadir}/mythtv/games/PC/screens
    mkdir -p %{buildroot}%{_datadir}/mame
    ln -s ../../mame %{buildroot}%{_datadir}/mythtv/games/xmame
    mkdir -p %{buildroot}%{_datadir}/mame/flyers
    ln -s snap %{buildroot}%{_datadir}/mythtv/games/xmame/screens
    mkdir -p %{buildroot}%{_sysconfdir}/mythgame
    cp -a mythgame/gamelist.xml %{buildroot}%{_sysconfdir}/mythgame/
    ln -s ../../../../../%{_sysconfdir}/mythgame/ \
        %{buildroot}%{_datadir}/mythtv/games/PC/gamelist.xml
%endif
popd
# And back to the build/install root
%endif

# Fixes ERROR: ambiguous python shebang
find %{buildroot}%{_datadir}/mythtv/ -type f -name "*.py" -exec sed -i '1s:#!/usr/bin/env python$:#!%{__python3}:' {} ';'
find %{buildroot}%{_datadir}/mythtv/ -type f -name "*.py" -exec sed -i '1s:#!/usr/bin/python$:#!%{__python3}:' {} ';'

# Install firewalld configs
mkdir -p %{buildroot}%{fw_services}
install -pm 0644 %{SOURCE115} %{buildroot}%{fw_services}/
install -pm 0644 %{SOURCE116} %{buildroot}%{fw_services}/

%pre common
%sysusers_create_compat %{SOURCE3}

%post backend
    %systemd_post mythbackend.service
    %systemd_post mythjobqueue.service
    %systemd_post mythdb-optimize.service
    %{?firewalld_reload}

%preun backend
    %systemd_preun mythbackend.service
    %systemd_preun mythjobqueue.service
    %systemd_preun mythdb-optimize.service

%postun backend
    %systemd_postun_with_restart mythbackend.service
    %systemd_postun_with_restart mythjobqueue.service
    %systemd_postun_with_restart mythdb-optimize.service

################################################################################

%files
%doc ChangeLog
%license mythtv/PACKAGE-LICENSING

%files docs
%doc mythtv/README*
%doc mythtv/AUTHORS
%doc mythtv/database
%doc mythtv/keybindings.txt
%doc mythtv/contrib

%files common
%dir %{_datadir}/mythtv
%{_bindir}/mythccextractor
%{_bindir}/mythcommflag
%{_bindir}/mythpreviewgen
%{_bindir}/mythtranscode
%{_bindir}/mythmetadatalookup
%{_bindir}/mythutil
%{_datadir}/mythtv/mythconverg*.pl
%{_datadir}/mythtv/*.xml
%{_datadir}/mythtv/locales/
%{_datadir}/mythtv/metadata/
%{_datadir}/mythtv/hardwareprofile/
%{_sysusersdir}/mythtv.conf
%attr(0775,-,mythtv) %dir %{_sysconfdir}/mythtv
%attr(0664,-,mythtv) %config(noreplace) %{_sysconfdir}/mythtv/config.xml

%files backend
%{_bindir}/mythbackend
%{_bindir}/mythexternrecorder
%{_bindir}/mythfilldatabase
%{_bindir}/mythfilerecorder
%{_bindir}/mythjobqueue
%{_bindir}/mythmediaserver
%{_bindir}/mythreplex
%{_bindir}/optimize_mythdb
%{_datadir}/mythtv/backend-config/
%attr(-,mythtv,mythtv) %dir %{_localstatedir}/lib/mythtv
%attr(-,mythtv,mythtv) %dir %{_localstatedir}/cache/mythtv
%{_unitdir}/mythbackend.service
%{_unitdir}/mythjobqueue.service
%{_unitdir}/mythdb-optimize.service
%{_unitdir}/mythdb-optimize.timer
/lib/udev/rules.d/99-mythbackend.rules
%config(noreplace) %{_sysconfdir}/logrotate.d/mythtv
%attr(-,mythtv,mythtv) %dir %{_localstatedir}/log/mythtv
%{_datadir}/mythtv/internetcontent/
%{_datadir}/mythtv/html/
%{_datadir}/mythtv/externrecorder/
%{fw_services}/mythtv-webbackend.xml

%files setup
%{_bindir}/mythtv-setup
%{_bindir}/mythtvsetup
%{_datadir}/applications/*mythtv-setup.desktop

%files frontend
%{_bindir}/mythavtest
%{_bindir}/mythfrontend
%{_bindir}/mythlcdserver
%{_bindir}/mythscreenwizard
%{_bindir}/mythshutdown
%{_bindir}/mythwelcome
%dir %{_libdir}/mythtv
%dir %{_libdir}/mythtv/plugins
%dir %{_datadir}/mythtv/i18n
%dir %{_datadir}/mythtv/fonts
%{_datadir}/mythtv/fonts/*.ttf
%{_datadir}/mythtv/fonts/*.otf
%{_datadir}/mythtv/fonts/*.txt
%{_datadir}/mythtv/i18n/mythfrontend_*.qm
%{_datadir}/applications/*mythfrontend.desktop
%{_datadir}/pixmaps/myth*.png
%{_datadir}/mythtv/metadata/
# Myth Video is now Video Gallery
%attr(0775,mythtv,mythtv) %{_localstatedir}/lib/mythvideo
%{fw_services}/mythtv-webfrontend.xml

%files base-themes
%{_datadir}/mythtv/themes/

%files libs
%{_libdir}/libmyth-%{major_rel}.so.*
%{_libdir}/libmythbase-%{major_rel}.so.*
%{_libdir}/libmythfreemheg-%{major_rel}.so.*
%{_libdir}/libmythmetadata-%{major_rel}.so.*
%{_libdir}/libmythprotoserver-%{major_rel}.so.*
%{_libdir}/libmythservicecontracts-%{major_rel}.so.*
%{_libdir}/libmythtv-%{major_rel}.so.*
%{_libdir}/libmythui-%{major_rel}.so.*
%{_libdir}/libmythupnp-%{major_rel}.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%dir %{_datadir}/mythtv/build
%{_datadir}/mythtv/build/settings.pro

%files -n mythffmpeg
%{_bindir}/mythffmpeg
%{_bindir}/mythffprobe
%{_libdir}/libmythav*.so.*
%{_libdir}/libmythpostproc.so.*
%{_libdir}/libmythswscale.so.*
%{_libdir}/libmythswresample.so.*

%if %{with perl}
%files -n perl-MythTV
%{perl_vendorlib}/MythTV.pm
%dir %{perl_vendorlib}/MythTV
%{perl_vendorlib}/MythTV/*.pm
%{perl_vendorlib}/IO/Socket/INET/MythTV.pm
%exclude %{perl_vendorarch}/auto/MythTV/.packlist
%endif

%if %{with php}
%files -n php-MythTV
%{_datadir}/mythtv/bindings/php/*
%endif

%if %{with python}
%files -n %{py_prefix}-MythTV
%{_bindir}/mythpython
%{_bindir}/mythwikiscripts
%{python3_sitelib}/MythTV/
%{python3_sitelib}/%{distinfo}
%endif

%if %{with plugins}
%files -n mythplugins

%if %{with mytharchive}
%files -n mytharchive
%doc mythplugins/mytharchive/AUTHORS
%doc mythplugins/mytharchive/COPYING
%doc mythplugins/mytharchive/README
%doc mythplugins/mytharchive/TODO
%{_bindir}/mytharchivehelper
%{_libdir}/mythtv/plugins/libmytharchive.so
%{_datadir}/mythtv/archivemenu.xml
%{_datadir}/mythtv/archiveutils.xml
%{_datadir}/mythtv/mytharchive
%{_datadir}/mythtv/i18n/mytharchive_*.qm
%endif

%if %{with mythbrowser}
%files -n mythbrowser
%doc mythplugins/mythbrowser/AUTHORS
%doc mythplugins/mythbrowser/README
%{_libdir}/mythtv/plugins/libmythbrowser.so
%{_datadir}/mythtv/i18n/mythbrowser_*.qm
%endif

%if %{with mythgame}
%files -n mythgame
%dir %{_sysconfdir}/mythgame
%config(noreplace) %{_sysconfdir}/mythgame/gamelist.xml
%{_libdir}/mythtv/plugins/libmythgame.so
%dir %{_datadir}/mythtv/games
%{_datadir}/mythtv/games/*
%{_datadir}/mame/screens
%dir %{_datadir}/mame/flyers
%{_datadir}/mythtv/game_settings.xml
%{_datadir}/mythtv/i18n/mythgame_*.qm
%endif

%if %{with mythmusic}
%files -n mythmusic
%doc mythplugins/mythmusic/AUTHORS
%doc mythplugins/mythmusic/COPYING
%doc mythplugins/mythmusic/README
%{_libdir}/mythtv/plugins/libmythmusic.so
%attr(0775,mythtv,mythtv) %{_localstatedir}/lib/mythmusic
%{_datadir}/mythtv/musicmenu.xml
%{_datadir}/mythtv/music_settings.xml
%{_datadir}/mythtv/i18n/mythmusic_*.qm
%endif

%if %{with mythnews}
%files -n mythnews
%doc mythplugins/mythnews/AUTHORS
%doc mythplugins/mythnews/README
%{_libdir}/mythtv/plugins/libmythnews.so
%{_datadir}/mythtv/mythnews
%{_datadir}/mythtv/i18n/mythnews_*.qm
%endif

%if %{with mythweather}
%files -n mythweather
%doc mythplugins/mythweather/AUTHORS
%doc mythplugins/mythweather/COPYING
%doc mythplugins/mythweather/README
%{_libdir}/mythtv/plugins/libmythweather.so
%{_datadir}/mythtv/i18n/mythweather_*.qm
%{_datadir}/mythtv/weather_settings.xml
%dir %{_datadir}/mythtv/mythweather
%{_datadir}/mythtv/mythweather/*
%endif

%if %{with mythzoneminder}
%files -n mythzoneminder
%{_libdir}/mythtv/plugins/libmythzoneminder.so
%{_datadir}/mythtv/zonemindermenu.xml
%{_bindir}/mythzmserver
%{_datadir}/mythtv/i18n/mythzoneminder_*.qm
%endif

%if %{with mythnetvision}
%files -n mythnetvision
%doc mythplugins/mythnetvision/AUTHORS
%doc mythplugins/mythnetvision/ChangeLog
%doc mythplugins/mythnetvision/README
%{_bindir}/mythfillnetvision
%{_libdir}/mythtv/plugins/libmythnetvision.so
%{_datadir}/mythtv/mythnetvision
%{_datadir}/mythtv/netvisionmenu.xml
%{_datadir}/mythtv/i18n/mythnetvision_*.qm
%endif

%endif

################################################################################

%changelog
* Fri Dec 12 2025 Andrew Bauer <zonexpertconsulting@outlook.com> - 35.0-11.45.20251203git187b4cc6ca
- update to latest fixes/35
- qt5-webkit no longer available in latest epel. Disable Mythbrowser plugin.

* Fri Dec 12 2025 Nicolas Chauvet <kwizart@gmail.com> - 35.0-10.33.20250810git931474b3a0
- Rebuilt for libbluray

* Wed Sep 10 2025 Andrew Bauer <zonexpertconsulting@outlook.com> - 35.0-9.33.20250810git931474b3a0
- Add sysusers support. Fixes RFBZ#7312

* Thu Sep 04 2025 Sérgio Basto <sergio@serjux.com> - 35.0-8.33.20250810git931474b3a0
- Rebuild for x264

* Sat Aug 30 2025 Andrew Bauer <zonexpertconsulting@outlook.com> - v35.0-7.33.20250810git931474b3a0
- Fix failure to build with normalized .dist-info folder name

* Sat Aug 16 2025 Andrew Bauer <zonexpertconsulting@outlook.com> - v35.0-6.33.20250810git931474b3a0
- Update to lastest fixes/35

* Sun Jul 27 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 35.0-5.2.20250302gitec351fd5c4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri May 30 2025 Leigh Scott <leigh123linux@gmail.com> - 35.0-4.2.20250302gitec351fd5c4
- Rebuild for new flac .so version

* Fri Mar 07 2025 Andrew Bauer <zonexpertconsulting@outlook.com> - v35.0-3.2.20250302gitec351fd5c4
- Remove version requirement for mythweb

* Mon Mar 03 2025 Andrew Bauer <zonexpertconsulting@outlook.com> - v35.0-2.2.20250302gitec351fd5c4
- Change mythweb runtime requirement to recommends

* Sun Mar 02 2025 Andrew Bauer <zonexpertconsulting@outlook.com> - v35.0-1.2.20250302gitec351fd5c4
- Update to lastest fixes/35

* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 34.0-6.28.20240704gitc63d023aa8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Nov 23 2024 Leigh Scott <leigh123linux@gmail.com> - 34.0-5.28.20240704gitc63d023aa8
- Rebuild for new x265

* Mon Sep 09 2024 Andrew Bauer <zonexpertconsulting@outlook.com> - v34.0-4.28.20240704gitc63d023aa8
- Update to lastest fixes/34

* Thu Jun 13 2024 Leigh Scott <leigh123linux@gmail.com> - 34.0-3.21.20240325gitd6398e090f
- Rebuilt for Python 3.13

* Mon May 13 2024 Andrew Bauer <zonexpertconsulting@outlook.com> - v34.0-1.21.20240325gitd6398e090f
- Update to lastest fixes/34
- Adjust firewalld config, fixes RFBZ 6922

* Sat Apr 06 2024 Leigh Scott <leigh123linux@gmail.com> - 34.0-2.10.20240220gita88dd47ba4
- Rebuild for new x265 version

* Fri Mar 01 2024 Andrew Bauer <zonexpertconsulting@outlook.com> - 34.0-1.10.20240220gita88dd47ba4
- 34.0 release
- Updates to lastest fixes/34

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 33.1-4.24.20240101git6b442547f2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 15 2024 Andrew Bauer <zonexpertconsulting@outlook.com> - 33.1-3.24.20240101gitg6b442547f
- fix typo in release tag

* Tue Jan 02 2024 Andrew Bauer <zonexpertconsulting@outlook.com> - 33.1-1.24.20240101gitg6b442547f
- Update to latest fixes/33
- update space_in_GB.patch to fix bz 6833

* Tue Jul 25 2023 Andrew Bauer <zonexpertconsulting@outlook.com> - 33.1-1.15.20230725gitg402c6d775
- Update to latest fixes/33 to fix ftbs on 6.5 kernel
- recommend gnome-shell-extension-no-overview for mythfrontend

* Mon Jul 24 2023 Andrew Bauer <zonexpertconsulting@outlook.com> - 33.1-1.14.20230714gitggbeaf2bacb
- Update to latest fixes/33
- add firewalld config for new web frontend
- adjust runtime requirements

* Sat Jul 08 2023 Leigh Scott <leigh123linux@gmail.com> - 33.1-2.4.20230219gitc273ed0f9a
- Rebuilt for Python 3.12

* Sun Feb 26 2023 Andrew Bauer <zonexpertconsulting@outlook.com> - 33.1-1.4.20230219gitgc273ed0f9
- Update to latest fixes/33
- remove support for rhel7
- mythtv no longer needs fftw

* Sun Dec 04 2022 Andrew Bauer <zonexpertconsulting@outlook.com> - 32.0-6.76.20221129gitg44f88ed46
- Update to latest fixes/32
- Take a minimalist approach with devel subpackage dependencies by removing most. See bz 6501

* Tue Nov 01 2022 Richard Shaw <hobbes1069@gmail.com> - 32.0-5.67.20221020gitba52c13223
- Update to 32.0.67.20221020gitba52c13223 from branch fixes/32
- Move git checkout in update script to use https as the git protocol seems to be down.

* Sun Aug 07 2022 Andrew Bauer <zonexpertconsulting@outlook.com> - 32.0-3.44.20220625gitg4cf469cbb
- python-mysql has been deprecated. Build against python-mysqlclient instead

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 32.0-2.44.20220625git4cf469cbbf
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Sat Jun 25 2022 Andrew Bauer <zonexpertconsulting@outlook.com> - 32.0-1.44.20220625gitg4cf469cbb
- Update to latest fixes/32, fixes rpmfusion bz#6327

* Tue Jun 21 2022 Paul Howarth <paul@city-fan.org> - 32.0-3.36.20220605git7077a824d2
- Perl 5.36 rebuild

* Sun Jun 12 2022 Sérgio Basto <sergio@serjux.com> - 32.0-2.36.20220605git7077a824d2
- Mass rebuild for x264-0.164

* Wed Jun 08 2022 Andrew Bauer <zonexpertconsulting@outlook.com> - 32.0-1.36.20220605gitg7077a824d
- Update to latest fixes/32

* Thu May 12 2022 Andrew Bauer <zonexpertconsulting@outlook.com> - 32.0-1.30.20220120gitg26079f815
- Update to latest fixes/32
- Add python setuptools, soundtouch, libzip, and expat build dependencies

* Sat Jan 22 2022 Andrew Bauer <zonexpertconsulting@outlook.com> - 31.0-25.167.20220120gitg4f7953f6e
- Update to latest fixes/31
- Reenable libcec on el8

* Tue Dec 14 2021 Andrew Bauer <zonexpertconsulting@outlook.com> - 31.0-24.167.20211108git25f1bb1d12
- Don't require mariadb. Let end user choose the db engine.

* Tue Dec 14 2021 Andrew Bauer <zonexpertconsulting@outlook.com> - 31.0-23.167.20211108git25f1bb1d12
- RHBZ 1838780 mariadb lacks mysql provides on el8

* Sat Dec 11 2021 Andrew Bauer <zonexpertconsulting@outlook.com> - 31.0-22.167.20211108git25f1bb1d12
- Update to latest fixes/31

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 31.0-21.158.20210610git0680b37c68
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Sérgio Basto <sergio@serjux.com> - 31.0-20.158.20210710git0680b37c68
- Mass rebuild for x264-0.163

* Tue Jun 29 2021 Andrew Bauer <zonexpertconsulting@outlook.com> - 31.0-17.147.20210629git0680b37c68
- Update to latest fixes/31
- Don't require lame binary on el8

* Tue Jun 15 2021 Leigh Scott <leigh123linux@gmail.com> - 31.0-18.147.20210615git05c16580e1
- Rebuild for python-3.10

* Wed Apr 21 2021 Andrew Bauer <zonexpertconsulting@outlook.com> - 31.0-17.147.20210421git05c16580e1
- Update to latest fixes/31.
- Auto compute the version string soley from git describe

* Wed Apr 14 2021 Leigh Scott <leigh123linux@gmail.com> - 31.0-16.139.20210226gitb6ddf202a4
- Rebuild for new x265

* Fri Feb 26 2021 Andrew Bauer <zonexpertconsulting@outlook.com> - 31.0-15.139.20210226gitb6ddf202a4
- Update to latest fixes/31.

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 31.0-14.130.20210108git016630a35c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 28 2021 Sérgio Basto <sergio@serjux.com> - 31.0-13.130.20210108git016630a35c
- Disable libcec on el8

* Sun Jan 17 2021 Sérgio Basto <sergio@serjux.com> - 31.0-12.130.20210108git016630a35c
- Update to 31.0.130.20210108git016630a35c from branch fixes/31
- Restore helper script update_fixes.sh
- Fixing el7 build, we can't enable libvpx on el7
- Fixing el7 build, libmythbluray are not used yet
  https://code.mythtv.org/cgit/mythtv/commit/?id=7a913df1ad2b44567c79cb248d3c40e6c3a6c347
  Bluray java is only build on el7, disabling it for now.

* Mon Dec 07 2020 Sérgio Basto <sergio@serjux.com>
- Fix for rfbz #5843

* Fri Nov 27 2020 Sérgio Basto <sergio@serjux.com> - 31.0-11.20201031giteb3c84de5f
- Mass rebuild for x264-0.161

* Sat Oct 31 2020 Richard Shaw <hobbes1069@gmail.com> - 31.0-10.20201031giteb3c84de5f
- Update to latest fixes/31.

* Sat Aug 29 2020 Richard Shaw <hobbes1069@gmail.com> - 31.0-9.20200829gitab0c38a476
- Update to latest fixes/v31.

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 31.0-8.20200527gitfc90482281
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 Sérgio Basto <sergio@serjux.com> - 31.0-7.20200527gitfc90482281
- Mass rebuild for x264

* Thu Jul 02 2020 Paul Howarth <paul@city-fan.org> - 31.0-6.20200527gitfc90482281
- Perl 5.32 rebuild

* Sun May 31 2020 Leigh Scott <leigh123linux@gmail.com> - 31.0-5.20200527gitfc90482281
- Rebuild for new x265 version

* Sat May 30 2020 Leigh Scott <leigh123linux@gmail.com> - 31.0-4.20200527gitfc90482281
- Rebuild for python-3.9

* Wed May 27 2020 Richard Shaw <hobbes1069@gmail.com> - 31.0-3.20200527gitfc90482281
- Update to latest fixes/31, fc90482281.
- Update from fixes/31 and clean up spec file conditionals.
- Remove duplicate libmythavutil.so from mythtv-libs as it's already in mythffmpeg.

* Wed May 27 2020 Richard Shaw <hobbes1069@gmail.com> - 31.0-2
- Remove duplicate libavutil library in mythtv-libs.

* Sat Apr 11 2020 Leigh Scott <leigh123linux@gmail.com> - 31.0-2
- Rebuild for new libcdio version

* Mon Mar 23 2020 Richard Shaw <hobbes1069@gmail.com> - 31.0-1
- Update to v31.0.
- Remove/Obsolete mythgallery package as it is no longer.
- Remove/Obsolete mythnetvision as it is buggy.

* Sun Feb 23 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 30.0-17.20191226gita27754ae7f
- Rebuild for x265

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 30.0-16.20191226gita27754ae7f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 26 2019 Richard Shaw <hobbes1069@gmail.com> - 30.0-15.20191226gita27754ae7f
- Update to latest v30 fixes.
- Clean up spec file and remove sysvinit sources.

* Tue Dec 17 2019 Leigh Scott <leigh123linux@gmail.com> - 30.0-14.20190904git5cde0578d8
- Mass rebuild for x264

* Thu Nov 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 30.0-13.20190904git5cde0578d8
- Rebuild for new x265

* Sun Sep 29 2019 Richard Shaw <hobbes1069@gmail.com> - 30.0-12.20190904git5cde0578d8
- Fix packaging for backend only systems.

* Wed Sep 04 2019 Richard Shaw <hobbes1069@gmail.com> - 30.0-11.20190904git5cde0578d8
- Update to v30.0-69-g5cde0578d8.
- Initial update for Python 3 compatibility using upstream pull request.

* Sun Aug 11 2019 Antonio Trande <sagitter@fedoraproject.org> - 30.0-10.20190601git6bd8cd4993
- Use Python3 on Fedora 31+

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 30.0-9.20190601git6bd8cd4993
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 02 2019 Nicolas Chauvet <kwizart@gmail.com> - 30.0-8.20190601git6bd8cd4993
- Rebuilt for x265

* Sat Jun 01 2019 Richard Shaw <hobbes1069@gmail.com> - 30.0-7.20190601git6bd8cd4993
- Update to fixes/30 commit 6bd8cd4993.

* Mon Apr 08 2019 Richard Shaw <hobbes1069@gmail.com> - 30.0-6.20190404git8e50fcf60b
- Updated to fixes/30 commit 8e50fcf60b.

* Mon Apr 08 2019 Nicolas Chauvet <kwizart@gmail.com> - 30.0-5.20190214gitb774c4140b
- Fix multilibs deps

* Tue Mar 12 2019 Sérgio Basto <sergio@serjux.com> - 30.0-4.20190214gitb774c4140b
- Mass rebuild for x264

* Wed Mar 06 2019 Richard Shaw <hobbes1069@gmail.com> - 30.0-3.20190214gitb774c4140b
- Add hdhomerun-devel as build requirement as it is no longer bundled.

* Sat Mar 02 2019 Nicolas Chauvet <kwizart@gmail.com> - 30.0-2.20190214gitb774c4140b
- Rebuilt for x265

* Thu Feb 14 2019 Richard Shaw <hobbes1069@gmail.com> - 30.0-1
- Update to 30.0 with latest fixes/30.

* Wed Dec 19 2018 Nicolas Chauvet <kwizart@gmail.com> - 29.1-30.53.20181105git9f0acf372d
- Mythweb is noarch

* Thu Dec 13 2018 Nicolas Chauvet <kwizart@gmail.com> - 29.1-29.53.20181105git9f0acf372d
- Rework dependencies for el7
- Fix python shebang

* Sat Dec 08 2018 Antonio Trande <sagitter@fedoraproject.org> - 29.1-28.53.20181105git9f0acf372d
- Fix python package's name

* Sat Dec 08 2018 Antonio Trande <sagitter@fedoraproject.org> - 29.1-27.53.20181105git9f0acf372d
- Rebuild for ffmpeg-3.4.5 on el7
- Rebuild for x264-0.148 on el7
- Rebuild for x265-2.9 on el7
- Use ldconfig_scriptlets
- Force python2- prefix

* Thu Nov 08 2018 Sérgio Basto <sergio@serjux.com> - 29.1-26.53.20181105git9f0acf372d
- Update to 29.1.53.20181105git9f0acf372d from branch fixes/29

* Fri Oct 05 2018 Sérgio Basto <sergio@serjux.com> - 29.1-25.39.20181004git74fff5c285
- Update to 29.1.39.20181004git74fff5c285 from branch fixes/29
- Fixes ERROR: ambiguous python shebang in F30
- Rework sources to avoid upload a new snapshot with 100MB, for every commit.
- Revert upstream commit b9c5f8b2ff983343d2545ec87022d18fcf65fe1f to fix build.

* Thu Oct 04 2018 Sérgio Basto <sergio@serjux.com> - 29.1-24.36.20180907.gdde16d475a
- Mass rebuild for x264 and/or x265

* Sun Sep 30 2018 Leigh Scott <leigh123linux@googlemail.com> - 29.1-23.36.20180907.gdde16d475a
- Require genisoimage and wodim as mkisofs and cdrecord virtual provides were removed

* Sat Sep 08 2018 Richard Shaw <hobbes1069@gmail.com> - 29.1-22.36.20180907.gdde16d475a
- Update to v29.1.36.20180907.gdde16d475a from branch fixes/29

* Wed Jul 25 2018 Leigh Scott <leigh123linux@googlemail.com> - 29.1-21.30.20180709.g2a0dadb37c
- Define python2 path to configure

* Sat Jul 21 2018 Richard Shaw <hobbes1069@gmail.com> - 29.1-20.30.20180709.g2a0dadb37c
- Update to v29.1.30.20180709.g2a0dadb37c from branch fixes/29

* Sun Jun 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 29.1-19.21.20180529.g1777cc4425
- Rebuild for new libass version

* Thu May 31 2018 Richard Shaw <hobbes1069@gmail.com> - 29.1-18.21.20180529.g1777cc4425
- Update to v29.1.21.20180529.g1777cc4425 from branch fixes/29
- This update includes fixes for the backend crashes with gcc 8.

* Thu May 10 2018 Sérgio Basto <sergio@serjux.com> - 29.1-17.19.20180510.g0849e99596
- Update to v29.1.19.20180510.g0849e99596 from branch fixes/29

* Thu May 10 2018 Richard Shaw <hobbes1069@gmail.com> - 29.1-16.20180509.18.g5f20e4f3f7
- Update to v29.1-18-g5f20e4f3f7 from branch fixes/29

* Fri Mar 09 2018 Sérgio Basto <sergio@serjux.com> - 29.1-15.20180228.8.g925ceea0fb
- Fixes nothing provides mythnetvision needed by mythplugins on epel7

* Sat Mar 03 2018 Richard Shaw <hobbes1069@gmail.com> - 29.1-14.20180228.8.g925ceea0fb
- Update to v29.1-8-g925ceea0fb from branch fixes/29.
- Update logrotate config, fixes RFBZ#4133.

* Wed Feb 28 2018 Leigh Scott <leigh123linux@googlemail.com> - 29.1-13.20180201.77.g9b7b962834
- Rebuilt for new x265

* Fri Feb 02 2018 Nicolas Chauvet <kwizart@gmail.com> - 29.1-12.20180201.77.g9b7b962834
- Update to 29.1

* Fri Feb 02 2018 Nicolas Chauvet <kwizart@gmail.com> - 29.0-11.20180111.77.g771115f47d
- Clean-up conditionals
- Remove vendor entry for desktop files
- Remove ppc conditional for cflags and use corrects ldflags

* Sat Jan 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 29.0-10.20180111.77.g771115f47d
- Rebuild for new libcdio and libvpx

* Sat Jan 20 2018 Sérgio Basto <sergio@serjux.com> - 29.0-9.20180111.77.g771115f47d
- fix rfbz #4684, Use mariadb-connector-c-devel instead of mysql-devel or
  mariadb-devel

* Tue Jan 16 2018 Richard Shaw <hobbes1069@gmail.com> - 29.0-8.20180111.77.g771115f47d
- Update to v29.0-77-g771115f47d from branch fixes/29

* Mon Jan 15 2018 Nicolas Chauvet <kwizart@gmail.com> - 29.0-7.20171226.71.g339b08e467
- Rebuilt for VA-API 1.0.0

* Sun Dec 31 2017 Sérgio Basto <sergio@serjux.com> - 29.0-6.20171226.71.g339b08e467
- Update to v29.0-71-g339b08e467 from branch fixes/29.

* Sun Dec 31 2017 Sérgio Basto <sergio@serjux.com> - 29.0-5
- Mass rebuild for x264 and x265

* Mon Nov 13 2017 Richard Shaw <hobbes1069@gmail.com> - 29.0-4
- Update to v29.0-57-gd743ef49a8.

* Wed Nov  1 2017 Richard Shaw <hobbes1069@gmail.com> - 29.0-3
- Update to v29.0-49-g75f05119b7.

* Mon Oct 23 2017 Richard Shaw <hobbes1069@gmail.com> - 29.0-2
- Update to v29.0-47-g83b32140f0.

* Sat Sep 16 2017 Richard Shaw <hobbes1069@gmail.com> - 29.0-1
- Update to new release, 29.0.

* Wed Sep  6 2017 Richard Shaw <hobbes1069@gmail.com> - 0.28.1-8
- Update to latest fixes/0/28, v0.28.1-45-g73cf7474ad.

* Sun Aug  6 2017 Richard Shaw <hobbes1069@gmail.com> - 0.28.1-6
- Update to latest fixes/0.28, v0.28.1-38-geef6a48.

* Mon Jun 19 2017 Paul Howarth <paul@city-fan.org> - 0.28.1-5
- Perl 5.26 rebuild

* Thu Jun  1 2017 Richard Shaw <hobbes1069@gmail.com> - 0.28.1-4
- Add patch from upstream to fix ppc bug.

* Mon Apr 24 2017 Richard Shaw <hobbes1069@gmail.com> - 0.28.1-3
- Update to latest fixes/0.28.
- Exclude ppc64 and ppc64le due to failed builds:
  https://code.mythtv.org/trac/ticket/13049

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.28.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Mar 14 2017 Richard Shaw <hobbes1069@gmail.com> - 0.28.1-1
- Update to latest upstream release.
- Move bundled ffmpeg libraries to mythffmpeg package, fixes RFBZ#4430.

* Tue Feb 07 2017 Xavier Bachelot <xavier@bachelot.org> - 0.28-13
- Only Recommends: xmltv on Fedora.

* Sun Jan 22 2017 Richard Shaw <hobbes1069@gmail.com> - 0.28-12
- Update to latest fixes/0.28 from git.
- Remove SysV conditionals as EL 7 has systemd and EL 6 is not supported.
- Update default permissions for /etc/mythtv and move user/group creation
  to the common package, fixes RFBZ#4414.
- Change some dependencies from Requires to Recommends, fixes RFBZ#4415.

* Sat Jan 21 2017 Xavier Bachelot <xavier@bachelot.org> - 0.28-11
- Fix build on EL7.

* Sun Nov 27 2016 Richard Shaw <hobbes1069@gmail.com> - 0.28-10
- Update to latest fixes/0.28 from git.
- Add patch for libcec 4, fixes RFBZ#4345.

* Thu Nov 17 2016 Adrian Reber <adrian@lisas.de> - 0.28-9
- Rebuilt for libcdio-0.94

* Wed Oct 19 2016 Richard Shaw <hobbes1069@gmail.com> - 0.28-8
- Update to lastest fixes/0.28 from git.

* Sun Sep 11 2016 Sérgio Basto <sergio@serjux.com> - 0.28-7
- Update to latest fixes/0.28, rfbz#4241

* Sun Sep 11 2016 Sérgio Basto <sergio@serjux.com> - 0.28-6
- Change mythtv.spec to use %%bcond
- Add BuildRequires: perl-generators, since F25 we have buildroot without Perl

* Thu Sep 08 2016 Sérgio Basto <sergio@serjux.com> - 0.28-5
- Rebuild again, previous perl-MythTV-0.28-4 does not provide perl(MythTV) !

* Mon Aug 01 2016 Sérgio Basto <sergio@serjux.com> - 0.28-4
-
  https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jun 13 2016 Richard Shaw <hobbes1069@gmail.com> - 0.28-3
- Update to lastest fixes/0.28 from git.

* Mon May 23 2016 Richard Shaw <hobbes1069@gmail.com> - 0.28-2
- Update to lastest fixes/0.28 from git.

* Tue Apr 12 2016 Richard Shaw <hobbes1069@gmail.com> - 0.28-1
- Update to latst upstream release.

* Mon Apr  4 2016 Richard Shaw <hobbes1069@gmail.com> - 0.27.6-3
- Update to latst upstream release.

* Fri Feb 19 2016 Richard Shaw <hobbes1069@gmail.com> - 0.27.6-2
- Update to latst upstream release.

* Tue Feb  2 2016 Richard Shaw <hobbes1069@gmail.com> - 0.27.6-1
- Update to latest upstream release.

* Thu Jan 14 2016 Richard Shaw <hobbes1069@gmail.com> - 0.27.5-4
- Update to latest upstream release.

* Mon Nov 16 2015 Richard Shaw <hobbes1069@gmail.com> - 0.27.5-3
- Update to latest upstream release.

* Mon Jul  6 2015 Richard Shaw <hobbes1069@gmail.com> - 0.27.5-1
- Update to latest upstream release.
- Move udisks requirement to the libs package where it's actually used.
- Add systemd mythtv database optimization service and timer.

* Tue May 26 2015 Richard Shaw <hobbes1069@gmail.com> - 0.27.4-6
- Update to latest bugfix release.
- Add conditional for udisks for Fedora 22+ (BZ#3660).

* Tue Apr  7 2015 Richard Shaw <hobbes1069@gmail.com> - 0.27.4-5
- Update to latest bugfix release.
- Fix owner on /etc/mythtv (BZ#3558).
- Add systemd unit file for mythjobqueue only backends (BZ#3571).

* Mon Mar  2 2015 Richard Shaw <hobbes1069@gmail.com> - 0.27.4-4
- Update to latest bugfix release.
- Add mesa-vdpau-drivers to requirements as it is usable on ATI/AMD video cards.

* Sun Jan  4 2015 Richard Shaw <hobbes1069@gmail.com> - 0.27.4-3
- Update to latest bugfix release.
- Change systemd dependency from network.target to network-online.target, fixes
  BZ#3482.

* Tue Nov 04 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.27.4-2
- Rebuilt for vaapi 0.36

* Mon Oct 13 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27.3-2.1
- Update to latest fixes.
- Add patch for schedules direct service change.
- Fix systemd conditional in spec file.

* Sun Jul 27 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27.3-1
- Update to new upstream release.

* Mon May 26 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27.1-1
- Update to new upstream release.

* Wed May  7 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27-7
- Update to latest fixes, v0.27-222-g583f448.

* Sat Mar 22 2014 Sérgio Basto <sergio@serjux.com> - 0.27-6
- Rebuilt for x264 and add BR: bzip2-devel

* Tue Mar 11 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27-5
- Update to latest fixes v0.27-178-g6b14852.
- Rebuild for x264.

* Mon Jan  6 2014 Richard Shaw <hobbes1069@gmail.com> - 0.27-4
- Update to latest fixes v0.27-130-gfac84fa.
- Add libcdio-paranoia to build requirements for CD audio.

* Mon Dec  2 2013 Richard Shaw <hobbes1069@gmail.com> - 0.27-3
- Update to latest fixes, v0.27-109-gcb744f8.
- Disable mythlogserver as it is only really useful for developers.
- Fix version reporting (--version).

* Tue Nov 05 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.27-2
- Rebuilt for x264/FFmpeg

* Wed Oct 30 2013 Richard Shaw <hobbes1069@gmail.com> - 0.27-1
- Update to release 0.27.

* Mon Aug 26 2013 Richard Shaw <hobbes1069@gmail.com> - 0.26.1-2
- Update to latest bugfix release.
- Add udisks as a requirement as it is required for ejecting cd/dvds.

* Thu Aug 22 2013 Richard Shaw <hobbes1069@gmail.com> - 0.26.1-1
- Update to latest bugfix release.
- Add patch for new libva 1.2.1 version in rawhide.

* Sat Jul 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.26.0-10
- Rebuilt for x264

* Mon May 06 2013 Richard Shaw <hobbes1069@gmail.com> - 0.26.0-9
- Update to latest fixes/0.26, v0.26.0-153-gb02d25a.
- Fixes long standing issue with transcoding on EL.
  http://code.mythtv.org/trac/ticket/2077

* Sat Apr 27 2013 Richard Shaw <hobbes1069@gmail.com> - 0.26.0-8
- Update to latest fixes/0.26, v0.26.0-149-g5f45c0b.

* Tue Feb 26 2013 Richard Shaw <hobbes1069@gmail.com> - 0.26.0-7
- Update to latest fixes/0.26, v0.26.0-111-g3944ca9.
- Add patch for mythlogserver segfault.
- Add patch for includes in bundled ffmpeg.
- Add conditionals for mariadb replacing mysql in rawhide (F19).

* Sun Jan 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.26.0-5
- Rebuilt for ffmpeg/x264

* Sat Dec 22 2012 Richard Shaw <hobbes1069@gmail.com> - 0.26.0-4
- Update to latest upstream release.

* Tue Dec  4 2012 Richard Shaw <hobbes1069@gmail.com> - 0.26.0-3
- Update to latest upstream release.

* Fri Nov 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.26.0-2
- Rebuilt for x264

* Sun Oct 28 2012 Richard Shaw <hobbes1069@gmail.com> - 0.26.0-1
- Update to latest upstream release.
- Remove mysql.txt as it is no longer used.
- Fix lib -> lib64 replacement command to be more accurate and support mythzmq
- Add mythzmq stuff

* Wed Sep 05 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.25.2-3
- Rebuilt for x264 ABI 125

* Sat Aug 25 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25.2-2
- Update to latest fixes/0.25.
- Fix mythbackend looking in the wrong directory for config.xml (BZ#2450).

* Mon Jul 16 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25.2-1
- Patch HLS for adapative x264 profile.
- Make sure mythbackend starts after time has synced.
- Update to latest fixes/0.25.

* Fri Jul 06 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25.1-2
- Patch for PHP 5.4 warnings.

* Tue Jun 05 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25.1-1
- Update to latest fixes/0.25.
- Move mythweb to a stand alone package.

* Fri May 11 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25-7
- Update to latest 0.25/fixes.

* Fri May 04 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25-6
- Add Bonjour (Airplay) support.
- Fix user creation for packages that create directories owned by mythtv user.
  Fixes BZ#2309.
- Update to latest 0.25/fixes.

* Sun Apr 29 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25-5
- Update to latest 0.25/fixes.
- Really fix logrotate this time.
- Add pmount to mytharchive requirements.

* Sat Apr 21 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25-3
- Removed obsolete build requirement for arts-devel.
- Re-add %%clean since it's still needed for mythweb.
- Update logrotate config for systemd.

* Wed Apr 18 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25-2
- Update to latest fixes/0.25.
- Change --logfile to --logpath for init files.
- Obsolete mythvideo in spec file.

* Tue Mar 20 2012 Richard Shaw <hobbes1069@gmail.com> - 0.25-1
- Update to latest release 0.25.

* Sat Mar 03 2012 Richard Shaw <hobbes1069@gmail.com> - 0.24.2-2
- Remove transcode as build requirement.
- Misc. spec file cleanup.

* Mon Feb 06 2012 Richard Shaw <hobbes1069@gmail.com> - 0.24.2-1
- Update to latest version.
- Update mythbackend systemd service file for better compatibilty with devices
  that take time to initialize due to firmware loading.
- Add dependency m2vrequantiser for mytharchive.
- Patched for building with gcc 4.7 (rawhide/Fedora 17).

* Mon Dec 12 2011 Richard Shaw <hobbes1069@gmail.com> - 0.24.1-6
- Fix %%post to make sure group membership gets set for the mythtv user.
- Fix ownership of mythtv directories.
- Update to latest 0.24.1-fixes, git revision 40f3bae.

* Mon Nov 21 2011 Richard Shaw <hobbes1069@gmail.com> - 0.24.1-5
- Fix typo in spec file causing mythtv user to not be created (#2051).
- Change mythbackend systemd type to "simple" and other fixes (#2016).
- Update to latest 0.24.1-fixes, git revision f5fd11fa54.
- Readd contrib directory (#1924).

* Fri Oct 28 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.24.1-4
- Fix for glibc bug rhbz#747377
! Reminder:
- Changes default user for mythbackend from root to mythtv on
  Fedora 16+. See http://rpmfusion.org/Package/mythtv for additonal information.

* Thu Oct 20 2011 Richard Shaw <hobbes1069@gmail.com> - 0.24.1-3
- Update to latest 0.24.1-fixes, git revision e89d6a9f7e.
- Fixes BZ#1993, FTBFS on Fedora 16.
- Moves from sysv init to systemd unit file for mythbackend on Fedora 16+
  See http://rpmfusion.org/Package/mythtv for additonal information.
- Changes default user for mythbackend from root to mythtv on
  Fedora 16+. See http://rpmfusion.org/Package/mythtv for additonal information.

* Mon May 30 2011 Jarod Wilson <jarod@wilsonet.com> 0.24.1-2
- Drop dependency on mythtv-themes, since upstream is no longer tarring
  them up, in preference of people using the built-in theme downloader.
- Update to 0.24-fixes, git revision 3657f313ac

* Tue May 17 2011 Jarod Wilson <jarod@wilsonet.com> 0.24.1-1
- Update to 0.24.1 stable update release

* Thu Mar 24 2011 Jarod Wilson <jarod@wilsonet.com> 0.24-7
- Update to 0.24 fixes, git revision 464fa28373
- Remove i810 and openchrome detritus

* Mon Feb 28 2011 Jarod Wilson <jarod@wilsonet.com> 0.24-6
- Update to 0.24 fixes, git revision 4af46b1f5d
- Fix mythtv version output to properly show git revision

* Sun Jan 30 2011 Jarod Wilson <jarod@wilsonet.com> 0.24-5
- Update to 0.24 fixes, git revision 8921ded85a (rpmfbz#1605, #1585)
- Add BR: libcdio-devel for forthcoming improved BD support
- Fix issue with calling setfacl on non-existent devices (rpmfbz#1604)

* Sun Jan 16 2011 Jarod Wilson <jarod@wilsonet.com> 0.24-4
- Update to 0.24 fixes, git revision 945c67317

* Fri Nov 26 2010 Jarod Wilson <jarod@wilsonet.com> 0.24-3
- Update to release-0-24-fixes, svn revision 27355

* Mon Nov 22 2010 Jarod Wilson <jarod@wilsonet.com> 0.24-2
- Update to release-0-24-fixes, svn revision 27317
- Add preview image fixup patch from ticket #9256
- Add alsa passthru device patches from trunk r27306 and r27307

* Wed Nov 10 2010 Jarod Wilson <jarod@wilsonet.com> 0.24-1
- Update to 0.24 release

* Wed Nov 03 2010 Jarod Wilson <jarod@wilsonet.com> 0.24-0.2.rc2
- Update to svn trunk, revision 27095 (post-rc2)
- Add Obsoletes/Provides for nuked mythmovies
- Restore run-with-non-root-backend-capable initscript from F13 branch

* Tue Oct 26 2010 Jarod Wilson <jarod@wilsonet.com> 0.24-0.2.rc1
- Update to svn trunk, revision 26998 (which is actually post-0.24-rc1)

* Thu Sep 23 2010 Jarod Wilson <jarod@wilsonet.com> 0.24-0.1.svn.r26482
- Update to svn trunk, revision 26482

* Wed Sep 01 2010 Jarod Wilson <jarod@wilsonet.com> 0.24-0.1.svn.r26065
- Update to svn trunk, revision 26065

* Sun Aug 29 2010 Jarod Wilson <jarod@wilsonet.com> 0.24-0.1.svn.r25946
- Update to svn trunk, revision 25985
- Patch in Qt 4.7 build fix patches from mythtv trac ticket #8572

* Sun Aug 29 2010 Jarod Wilson <jarod@wilsonet.com> 0.24-0.1.svn.r25946
- Update to svn trunk, revision 25946
- Add new crystalhd dependency

* Sun Aug 15 2010 Jarod Wilson <jarod@wilsonet.com> 0.24-0.1.svn.r25695
- Update to svn trunk, revision 25695
- Account for qt/qt-webkit split on F14

* Fri Aug 13 2010 Jarod Wilson <jarod@wilsonet.com> 0.24-0.1.svn.r25638
- Update to svn trunk, revision 25638
- Big resync with mythtv scm rpm spec, fixes a lot of build issues
  that have cropped up from recent code churn

* Thu Apr 01 2010 Jarod Wilson <jarod@wilsonet.com> 0.24-0.1.svn.r23902
- Update to svn trunk, revision 23902
- Starts tracking 0.24-bound svn trunk, now that 0.23 has branched
