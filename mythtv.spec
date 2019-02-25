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
# --without crystalhd       Disable Crystal HD support
# --without perl            Disable building of the perl bindings
# --without php             Disable building of the php bindings
# --without python          Disable building of the python bindings
#
# # All plugins get built by default, but you can disable them as you wish:
#
# --without mytharchive
# --without mythbrowser
# --without mythgallery
# --without mythgame
# --without mythmusic
# --without mythnetvision
# --without mythnews
# --without mythweather
# --without mythzoneminder
#

################################################################################

# A list of which applications we want to put into the desktop menu system
%define desktop_applications mythfrontend mythtv-setup

# MythTV Version string -- preferably the output from git describe
%define githash b774c4140b2b9e148ccf699d1ad746bc4c84289c
%define shorthash %(c=%{githash}; echo ${c:0:10})
%define vers_string v30.0-15-gb774c4140b
%define rel_date 20190214
%define rel_string .%{rel_date}git%{shorthash}

%define branch fixes/30

# Harden build as mythbackend is long running.
%global _hardened_build 1

#
# Basic descriptive tags for this package:
#
Name:           mythtv
Version:        30.0
Release:        1%{?rel_string}%{?dist}
Summary:        A digital video recorder (DVR) application

# The primary license is GPLv2+, but bits are borrowed from a number of
# projects... For a breakdown of the licensing, see PACKAGE-LICENSING.
License:        GPLv2+ and LGPLv2+ and LGPLv2 and (GPLv2 or QPL) and (GPLv2+ or LGPLv2+)
URL:            http://www.mythtv.org/
Source0:        https://github.com/MythTV/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         https://github.com/MythTV/%{name}/compare/v%{version}..%{shorthash}.patch
Patch1:         %{name}-space_in_GB.patch


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
%bcond_without crystalhd
%bcond_without sdnotify
%bcond_without perl
%bcond_without php
%bcond_without python
%bcond_without pulseaudio

# All plugins get built by default, but you can disable them as you wish
%bcond_without plugins
%bcond_without mytharchive
%bcond_without mythbrowser
%bcond_without mythgallery
%bcond_without mythgame
%bcond_without mythmusic
%bcond_without mythnews
%bcond_without mythweather
%bcond_without mythzoneminder
%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without mythnetvision
%else
%bcond_with mythnetvision
%endif

# Python2 prefix for building on rhel
%if 0%{?rhel} && 0%{?rhel} < 8
%global py_prefix python
%endif

%if 0%{?fedora} && 0%{?fedora} > 30
%global py_prefix python3
%else
%global py_prefix python2
%endif


################################################################################
#
### THE BELOW IS NOW AUTOMATED BY SCRIPTS IN SCM ###
#
# From the mythtv git repository with the appropriate branch checked out:
# Example: git diff -p --stat v0.26.0 > mythtv-0.26-fixes.patch
# Also update ChangeLog with git log v0.28..HEAD > ChangeLog
# and update define vers_string to v0.28-52-ge6a60f7 with git describe

Source10:  %{name}-PACKAGE-LICENSING
Source11:  %{name}-ChangeLog
Source101: mythbackend.sysconfig
Source102: mythbackend.init
Source103: %{name}.logrotate.sysv
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

# Global MythTV and Shared Build Requirements

# Use systemd
BuildRequires:  systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

BuildRequires:  gcc-c++ lzo-devel
BuildRequires:  perl-generators
BuildRequires:  desktop-file-utils
BuildRequires:  qt5-qtbase-devel >= 5.2
BuildRequires:  qt5-qtscript-devel >= 5.2
BuildRequires:  qt5-qtwebkit-devel >= 5.2
BuildRequires:  freetype-devel >= 2
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  mariadb-connector-c-devel
%else
BuildRequires:  mariadb-devel >= 5
%endif
%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:  libcec-devel >= 1.7
%endif
BuildRequires:  libvpx-devel
BuildRequires:  lm_sensors-devel
BuildRequires:  lirc-devel
BuildRequires:  nasm
Buildrequires:  yasm-devel

# X, and Xv video support
BuildRequires:  libXmu-devel
BuildRequires:  libXv-devel
BuildRequires:  libXvMC-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
BuildRequires:  mesa-libGLU-devel
%ifarch %arm
BuildRequires:  mesa-libGLES-devel
%endif
BuildRequires:  xorg-x11-proto-devel
%ifarch %{ix86} x86_64
BuildRequires:  xorg-x11-drv-intel-devel
BuildRequires:  xorg-x11-drv-openchrome-devel
%endif

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
BuildRequires:  jack-audio-connection-kit-devel
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
BuildRequires:  libavc1394-devel
BuildRequires:  libiec61883-devel
BuildRequires:  libraw1394-devel

BuildRequires: %{py_prefix}-future
%if 0%{?fedora} || 0%{?rhel} > 7
# For ttvdb.py, not available in EPEL
BuildRequires: %{py_prefix}-requests
BuildRequires: %{py_prefix}-requests-cache
%else
BuildRequires: python-requests
%endif

%if %{with vdpau}
BuildRequires:  libvdpau-devel
%endif

%if %{with vaapi}
BuildRequires:  libva-devel
%endif

%if %{with crystalhd}
BuildRequires:  libcrystalhd-devel
%endif

%if %{with sdnotify}
BuildRequires:  systemd-devel
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
BuildRequires:  %{py_prefix}-devel
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  %{py_prefix}-mysql
BuildRequires:  %{py_prefix}-urlgrabber
%else
BuildRequires:  python-urlgrabber
BuildRequires:  MySQL-python
%endif
%endif

# Plugin Build Requirements

%if %{with plugins}

%if %{with mythgallery}
BuildRequires:  libexif-devel >= 0.6.9
%endif

%if %{with mythgame}
BuildRequires:  zlib-devel
%endif

%if %{with mythnews}
%endif

BuildRequires: ncurses-devel


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
Requires:  mythweb                    = %{version}
Requires:  mythffmpeg%{?_isa}         = %{version}-%{release}
Requires:  mysql-compat-server >= 5
Requires:  mysql >= 5
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

%{?el7:BuildRequires: epel-rpm-macros}
Requires:  freetype%{?_isa} >= 2
Requires:  lame%{?_isa}
Requires:  qt5-qtbase-mysql%{?_isa}
Requires:  udisks2%{?_isa}

%description libs
Common library code for MythTV and add-on modules (development)
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

################################################################################

%package devel
Summary:   Development files for mythtv

Requires:  mythtv-libs%{?_isa} = %{version}-%{release}

Requires:  freetype-devel%{?_isa} >= 2
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  mariadb-connector-c-devel
%else
BuildRequires:  mariadb-devel >= 5
%endif
Requires:  qt5-qtbase-devel%{?_isa} >= 5.2
Requires:  qt5-qtscript-devel%{?_isa} >= 5.2
Requires:  qt5-qtwebkit-devel%{?_isa} >= 5.2
Requires:  lm_sensors-devel%{?_isa}
Requires:  lirc-devel%{?_isa}

# X, and Xv video support
Requires:  libXmu-devel%{?_isa}
Requires:  libXv-devel%{?_isa}
Requires:  libXvMC-devel%{?_isa}
Requires:  libXxf86vm-devel%{?_isa}
# Reminder this one is noarch
Requires:  xorg-x11-proto-devel

# OpenGL video output and vsync support
Requires:  mesa-libGL-devel%{?_isa}
Requires:  mesa-libGLU-devel%{?_isa}

# Misc A/V format support
Requires:  fftw-devel%{?_isa} >= 3
Requires:  flac-devel%{?_isa} >= 1.0.4
Requires:  gsm-devel%{?_isa}
Requires:  lame-devel%{?_isa}
Requires:  libdca-devel%{?_isa}
Requires:  libdvdnav-devel%{?_isa}
Requires:  libdvdread-devel%{?_isa} >= 0.9.4
Requires:  libfame-devel%{?_isa} >= 0.9.0
Requires:  libogg-devel%{?_isa}
Requires:  libtheora-devel%{?_isa}
Requires:  libvorbis-devel%{?_isa} >= 1.0
Requires:  mjpegtools-devel%{?_isa} >= 1.6.1
Requires:  taglib-devel%{?_isa} >= 1.5
Requires:  x264-devel%{?_isa}
Requires:  x265-devel%{?_isa}
Requires:  xvidcore-devel%{?_isa} >= 0.9.1

# Audio framework support
Requires:  alsa-lib-devel%{?_isa}
Requires:  jack-audio-connection-kit-devel%{?_isa}
%if %{with pulseaudio}
Requires:  pulseaudio-libs-devel%{?_isa}
%endif

# Need dvb headers for dvb support
Requires:  kernel-headers%{?_isa}

# FireWire cable box support
Requires:  libavc1394-devel%{?_isa}
Requires:  libiec61883-devel%{?_isa}
Requires:  libraw1394-devel%{?_isa}

%if %{with vdpau}
Requires: libvdpau-devel%{?_isa}
%endif

%if %{with vaapi}
Requires: libva-devel%{?_isa}
%endif

%if %{with crystalhd}
Requires: libcrystalhd-devel%{?_isa}
%endif

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
Requires:  lame%{?_isa}
Requires:  perl(XML::Simple)
Requires:  mythtv-common%{?_isa}       = %{version}-%{release}
Requires:  mythtv-base-themes%{?_isa}  = %{version}-%{release}
Requires:  mysql%{?_isa} >= 5
Requires:  %{py_prefix}-MythTV       = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} > 7
Recommends: libaacs%{?_isa}
%else
Requires: libaacs%{?_isa}
%endif
%{?fedora:Requires:  google-droid-sans-mono-fonts}
%{?fedora:Recommends:  mesa-vdpau-drivers%{?_isa}}
Provides:  mythtv-frontend-api%{?_isa} = %{mythfeapiver}

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
Requires:   lame%{?_isa}
Requires:   mythtv-common%{?_isa} = %{version}-%{release}
Requires:   mythtv-libs%{?_isa}   = %{version}-%{release}
Requires:   mythtv-setup%{?_isa}
Requires:   %{py_prefix}-future
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:   %{py_prefix}-requests
Requires:   %{py_prefix}-requests-cache
%else
Requires:   python-requests
%endif

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

%description setup
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the setup software for configuring the
mythtv backend.

################################################################################

%package common
Summary: Common components needed by multiple other MythTV components
# For ttvdb.py
Requires: %{py_prefix}-future
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:   %{py_prefix}-requests
Requires:   %{py_prefix}-requests-cache
%else
Requires:   python-requests
%endif

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
Summary:        Python2 bindings for MythTV
%if 0%{?fedora} > 30
%{?python_provide:%python_provide python3-%{name}}
%else
%{?python_provide:%python_provide python2-%{name}}
%{?python_provide:%python_provide python2-MythTV}
%endif
BuildArch:      noarch

%if 0%{?fedora} || 0%{?rhel} > 7
Requires:       %{py_prefix}-mysql
Requires:       %{py_prefix}-lxml
%else
Requires:       MySQL-python
Requires:       python-lxml
%endif

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
%if %{with mythgallery}
Requires:  mythgallery%{?_isa}    = %{version}-%{release}
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
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:  %{py_prefix}-mysql
Requires:  %{py_prefix}-pillow
%else
Requires:  MySQL-python
Requires:  python-pillow
%endif
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
%if %{with mythgallery}

%package -n mythgallery
Summary:   A gallery/slideshow module for MythTV
Requires:  mythtv-frontend-api%{?_isa} = %{mythfeapiver}

%description -n mythgallery
A gallery/slideshow module for MythTV.

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
# This is packaged in adobe's yum repo
#Requires:  flash-plugin

%description -n mythnetvision
A MythTV module that supports searching and browsing of Internet video
on demand content.

%endif
################################################################################

# End of plugins
%endif

################################################################################

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

# Remove compiled python file
#find -name *.pyc -exec rm -f {} \;

# Remove exe permissions
find . -type f -name "*.cpp" -exec chmod 0644 '{}' \;

# Install ChangeLog
install -m 0644 %{SOURCE11} ./ChangeLog

pushd mythtv

# Set the mythtv --version string
cat > EXPORTED_VERSION <<EOF
SOURCE_VERSION=%{vers_string}
BRANCH=%{branch}
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

#pushd mythplugins
#sed -i "s|mysql\/mysql.h|mariadb\/mysql.h|g" configure mythzoneminder/mythzmserver/zmserver.h mythmusic/contrib/import/itunes/it2m.h
#popd


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
%if ! %{with crystalhd}
    --disable-crystalhd                         \
%endif
%if ! %{with vaapi}
    --disable-vaapi                             \
%endif
    --enable-bdjava                             \
%if 0%{?fedora} > 30
    --python=%{__python3}                       \
%else
    --python=%{__python2}                       \
%endif
    --enable-libmp3lame                         \
    --enable-libx264                            \
    --enable-libx265                            \
    --enable-libxvid                            \
    --enable-libvpx                             \
%if !%{with perl}
    --without-bindings=perl                     \
%endif
%if !%{with php}
    --without-bindings=php                      \
%endif
%if !%{with python}
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
    %if %{with mythgallery}
        --enable-mythgallery \
        --enable-exif \
        --enable-new-exif \
    %else
        --disable-mythgallery \
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
        --enable-opengl \
%if 0%{?fedora} > 30    
    --python=%{__python3}      \
%else
    --python=%{__python2}      \
%endif
        --enable-fftw

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
%if %{with mythgallery}
    mkdir -p %{buildroot}%{_localstatedir}/lib/pictures
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

# Fixes ERROR: ambiguous python shebang in F30
%if 0%{?fedora} > 30
find %{buildroot}%{_datadir}/mythtv/ -type f -name "*.py" -exec sed -i '1s:#!/usr/bin/env python$:#!%{__python3}:' {} ';'
find %{buildroot}%{_datadir}/mythtv/ -type f -name "*.py" -exec sed -i '1s:#!/usr/bin/python$:#!%{__python3}:' {} ';'
%else
find %{buildroot}%{_datadir}/mythtv/ -type f -name "*.py" -exec sed -i '1s:#!/usr/bin/env python$:#!%{__python2}:' {} ';'
find %{buildroot}%{_datadir}/mythtv/ -type f -name "*.py" -exec sed -i '1s:#!/usr/bin/python$:#!%{__python2}:' {} ';'
%endif

%pre common
# Add the "mythtv" user, with membership in the audio and video group
getent group mythtv >/dev/null || groupadd -r mythtv
getent passwd mythtv >/dev/null || \
    useradd -r -g mythtv -d %{_localstatedir}/lib/mythtv -s /sbin/nologin \
    -c "mythbackend user" mythtv
# Make sure the mythtv user is in the audio and video group for existing
# or new installs.
usermod -a -G audio,video mythtv
exit 0

%pre -n mythmusic
# Add the "mythtv" user, with membership in the audio and video group
getent group mythtv >/dev/null || groupadd -r mythtv
getent passwd mythtv >/dev/null || \
    useradd -r -g mythtv -d %{_localstatedir}/lib/mythtv -s /sbin/nologin \
    -c "mythbackend user" mythtv
# Make sure the mythtv user is in the audio and video group for existing
# or new installs.
usermod -a -G audio,video mythtv
exit 0

%ldconfig_scriptlets libs
%ldconfig_scriptlets -n mythffmpeg

%post backend
    %systemd_post mythbackend.service
    %systemd_post mythjobqueue.service
    %systemd_post mythdb-optimize.service

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
%doc mythtv/UPGRADING
%doc mythtv/AUTHORS
%license mythtv/COPYING
%doc mythtv/FAQ
%doc mythtv/database mythtv/keys.txt
%doc mythtv/contrib

%files common
%dir %{_datadir}/mythtv
%{_bindir}/mythccextractor
%{_bindir}/mythcommflag
%{_bindir}/mythpreviewgen
%{_bindir}/mythtranscode
%{_bindir}/mythwikiscripts
%{_bindir}/mythmetadatalookup
%{_bindir}/mythutil
%{_datadir}/mythtv/mythconverg*.pl
%{_datadir}/mythtv/locales/
%{_datadir}/mythtv/metadata/
%{_datadir}/mythtv/hardwareprofile/
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
%{_datadir}/mythtv/MXML_scpd.xml
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

%files setup
%{_bindir}/mythtv-setup
%{_bindir}/mythtvsetup
%{_datadir}/mythtv/setup.xml
%{_datadir}/applications/*mythtv-setup.desktop

%files frontend
%{_datadir}/mythtv/CDS_scpd.xml
%{_datadir}/mythtv/CMGR_scpd.xml
%{_datadir}/mythtv/MFEXML_scpd.xml
%{_datadir}/mythtv/MSRR_scpd.xml
%{_datadir}/mythtv/devicemaster.xml
%{_datadir}/mythtv/deviceslave.xml
%{_datadir}/mythtv/setup.xml
%{_bindir}/mythavtest
%{_bindir}/mythfrontend
%{_bindir}/mythlcdserver
%{_bindir}/mythscreenwizard
%{_bindir}/mythshutdown
%{_bindir}/mythwelcome
%dir %{_libdir}/mythtv
%{_libdir}/mythtv/filters/
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

%files base-themes
%{_datadir}/mythtv/themes/

%files libs
%exclude %{_libdir}/libmythav*.so.*
%exclude %{_libdir}/libmythpostproc.so.*
%exclude %{_libdir}/libmythswscale.so.*
%exclude %{_libdir}/libmythswresample.so.*
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%dir %{_datadir}/mythtv/build
%{_datadir}/mythtv/build/settings.pro

%files -n mythffmpeg
%{_bindir}/mythffmpeg
%{_bindir}/mythffprobe
%{_bindir}/mythffserver
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
%if 0%{?fedora} > 30
%{python3_sitelib}/MythTV/
%{python3_sitelib}/MythTV-*.egg-info
%else
%{python2_sitelib}/MythTV/
%{python2_sitelib}/MythTV-*.egg-info
%endif
%endif

%if %{with plugins}
%files -n mythplugins
%doc mythplugins/COPYING

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
%doc mythplugins/mythbrowser/COPYING
%doc mythplugins/mythbrowser/README
%{_libdir}/mythtv/plugins/libmythbrowser.so
%{_datadir}/mythtv/i18n/mythbrowser_*.qm
%endif

%if %{with mythgallery}
%files -n mythgallery
%doc mythplugins/mythgallery/AUTHORS
%doc mythplugins/mythgallery/COPYING
%doc mythplugins/mythgallery/README
%{_libdir}/mythtv/plugins/libmythgallery.so
%{_datadir}/mythtv/i18n/mythgallery_*.qm
%attr(0775,mythtv,mythtv) %{_localstatedir}/lib/pictures
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
%doc mythplugins/mythnews/COPYING
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
