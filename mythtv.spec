# Specfile for building MythTV and MythPlugins RPMs from a subversion checkout.
#
# by:   Chris Petersen <rpm@forevermore.net>
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
#     http://cvs.rpmfusion.org/viewvc/rpms/mythtv/devel/?root=free
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
# --without crystalhd       Disable Crystal HD support (disabled, currently broken)
# --without perl            Disable building of the perl bindings
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

# The vendor name we should attribute the aforementioned entries to
%define desktop_vendor RPMFusion

# Git revision and branch ID
# 0.25 release: git tag v0.25.1
%define _gitrev v0.26.0-0-g6c3ae8
%define branch fixes/0.26

# Mythtv and plugins from github.com
%global githash1 g6c3ae81
%global githash2 d2f9798

#
# Basic descriptive tags for this package:
#
Name:           mythtv
Summary:        A digital video recorder (DVR) application
URL:            http://www.mythtv.org/
Group:          Applications/Multimedia

# Version/Release info
Version:        0.26.0
%if "%{branch}" == "master"
Release:        0.1.git.%{_gitrev}%{?dist}
%else
Release:        1%{?dist}
%endif

# The primary license is GPLv2+, but bits are borrowed from a number of
# projects... For a breakdown of the licensing, see PACKAGE-LICENSING.
License:        GPLv2+ and LGPLv2+ and LGPLv2 and (GPLv2 or QPL) and (GPLv2+ or LGPLv2+)

################################################################################

# Set "--with proc_opt" to let mythtv autodetect your CPU and run its
# processor-specific optimizations.  It seems to cause compile problems on many
# systems (particularly x86_64), so it is classified by the MythTV developers
# as "use at your own risk."
%define with_proc_opt      %{?_with_proc_opt:      1} %{!?_with_proc_opt:      0}

# Set "--with debug" to enable MythTV debug compile mode
%define with_debug         %{?_with_debug:         1} %{?!_with_debug:         0}

# The following options are enabled by default.  Use --without to disable them
%define with_vdpau         %{?_without_vdpau:      0} %{?!_without_vdpau:      1}
%define with_vaapi         %{?_without_vaapi:      0} %{?!_without_vaapi:      1}

%if 0%{?rhel}
%define with_crystalhd     %{?_without_crystalhd:  1} %{?!_without_crystalhd:  0}
%else
%define with_crystalhd     %{?_without_crystalhd:  0} %{?!_without_crystalhd:  1}
%endif

%define with_perl          %{?_without_perl:       0} %{!?_without_perl:       1}
%define with_php           %{?_without_php:        0} %{!?_without_php:        1}
%define with_python        %{?_without_python:     0} %{!?_without_python:     1}
%define with_pulseaudio    %{?_without_pulseaudio: 0} %{!?_without_pulseaudio: 1}

# FAAC is non-free, so we disable it by default
%define with_faac          %{?_with_faac:          1} %{?!_with_faac:          0}

# All plugins get built by default, but you can disable them as you wish
%define with_plugins        %{?_without_plugins:        0} %{!?_without_plugins:         1}
%define with_mytharchive    %{?_without_mytharchive:    0} %{!?_without_mytharchive:     1}
%define with_mythbrowser    %{?_without_mythbrowser:    0} %{!?_without_mythbrowser:     1}
%define with_mythgallery    %{?_without_mythgallery:    0} %{!?_without_mythgallery:     1}
%define with_mythgame       %{?_without_mythgame:       0} %{!?_without_mythgame:        1}
%define with_mythmusic      %{?_without_mythmusic:      0} %{!?_without_mythmusic:       1}
%define with_mythnews       %{?_without_mythnews:       0} %{!?_without_mythnews:        1}
%define with_mythweather    %{?_without_mythweather:    0} %{!?_without_mythweather:     1}
%define with_mythzoneminder %{?_without_mythzoneminder: 0} %{!?_without_mythzoneminder:  1}
%define with_mythnetvision  %{?_without_mythnetvision:  0} %{!?_without_mythnetvision:   1}

################################################################################

# https://github.com/MythTV/mythtv/tarball/v0.25
Source0:   MythTV-%{name}-v%{version}-0-%{githash1}.tar.gz

Patch0:    mythtv-0.26-fixes.patch

Source10:  PACKAGE-LICENSING
Source11:  ChangeLog
Source101: mythbackend.sysconfig
Source102: mythbackend.init
Source103: mythtv.logrotate.sysv
Source104: mythtv.logrotate.sysd
Source105: mythbackend.service
Source106: mythfrontend.png
Source107: mythfrontend.desktop
Source108: mythtv-setup.png
Source109: mythtv-setup.desktop
Source111: 99-mythbackend.rules


# Global MythTV and Shared Build Requirements

%if 0%{?fedora} >= 16
# Use systemd
BuildRequires:  systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# For sysv -> systemd transition
Requires(post): systemd-sysv
%else
# Use SysV
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  freetype-devel >= 2
BuildRequires:  gcc-c++
BuildRequires:  mysql-devel >= 5
BuildRequires:  qt-webkit-devel
BuildRequires:  qt-devel >= 4.6
BuildRequires:  phonon-devel
BuildRequires:  libuuid-devel

BuildRequires:  lm_sensors-devel
BuildRequires:  lirc-devel
BuildRequires:  nasm, yasm-devel

# X, and Xv video support
BuildRequires:  libXmu-devel
BuildRequires:  libXv-devel
BuildRequires:  libXvMC-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  xorg-x11-proto-devel
%ifarch %{ix86} x86_64
BuildRequires:  xorg-x11-drv-intel-devel
BuildRequires:  xorg-x11-drv-openchrome-devel
%endif

# OpenGL video output and vsync support
BuildRequires:  libGL-devel, libGLU-devel

# Misc A/V format support
%if %{with_faac}
BuildRequires:  faac-devel
%endif
BuildRequires:  fftw-devel >= 3
BuildRequires:  flac-devel >= 1.0.4
BuildRequires:  gsm-devel
BuildRequires:  lame-devel
BuildRequires:  libdca-devel
BuildRequires:  libdvdnav-devel
BuildRequires:  libdvdread-devel >= 0.9.4
BuildRequires:  libcdio-devel
# nb: libdvdcss will be dynamically loaded if installed
#BuildRequires:  libfame-devel >= 0.9.0
BuildRequires:  libogg-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel >= 1.0
BuildRequires:  taglib-devel >= 1.6
BuildRequires:  x264-devel
BuildRequires:  xvidcore-devel >= 0.9.1

# Audio framework support
BuildRequires:  SDL-devel
BuildRequires:  sox-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  jack-audio-connection-kit-devel
%if %{with_pulseaudio}
BuildRequires:  pulseaudio-libs-devel
%endif
BuildRequires:  avahi-compat-libdns_sd-devel

# Bluray support
BuildRequires:  libxml2-devel
#BuildRequires:  libudf-devel

# Subtitle support
BuildRequires:  libass-devel

# Need dvb headers to build in dvb support
BuildRequires: kernel-headers

# FireWire cable box support
BuildRequires:  libavc1394-devel
BuildRequires:  libiec61883-devel
BuildRequires:  libraw1394-devel

%if %{with_vdpau}
BuildRequires: libvdpau-devel
%endif

%if %{with_vaapi}
BuildRequires: libva-devel
%endif

%if %{with_crystalhd}
BuildRequires: libcrystalhd-devel
%endif

# API Build Requirements

%if %{with_perl}
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

%if %{with_php}
# No php specific requirements yet.
%endif

%if %{with_python}
BuildRequires:  python-devel
BuildRequires:  MySQL-python
BuildRequires:  python-urlgrabber
%endif

# Plugin Build Requirements

%if %{with_plugins}

%if %{with_mythgallery}
BuildRequires:  libexif-devel >= 0.6.9
%endif

%if %{with_mythgame}
BuildRequires:  zlib-devel
%endif

%if %{with_mythnews}
%endif

BuildRequires: ncurses-devel


%if %{with_mythweather}
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

%if %{with_mythzoneminder}
%endif

%if %{with_mythnetvision}
BuildRequires:  python-pycurl
BuildRequires:  python-lxml
BuildRequires:  python-oauth
%endif

%endif

################################################################################
# Requirements for the mythtv meta package

Requires:  mythtv-libs        = %{version}-%{release}
Requires:  mythtv-backend     = %{version}-%{release}
Requires:  mythtv-base-themes = %{version}-%{release}
Requires:  mythtv-common      = %{version}-%{release}
Requires:  mythtv-docs        = %{version}-%{release}
Requires:  mythtv-frontend    = %{version}-%{release}
Requires:  mythtv-setup       = %{version}-%{release}
Requires:  perl-MythTV        = %{version}-%{release}
Requires:  php-MythTV         = %{version}-%{release}
Requires:  python-MythTV      = %{version}-%{release}
Requires:  mythplugins        = %{version}-%{release}
Requires:  mythweb            = %{version}
Requires:  mythffmpeg         = %{version}-%{release}
Requires:  mysql-server >= 5, mysql >= 5
Requires:  xmltv

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
Group:     Documentation
BuildArch: noarch

%description docs
The MythTV documentation, database initialization file
and miscellaneous other bits and pieces.

################################################################################

%package libs
Summary:   Library providing mythtv support
Group:     System Environment/Libraries
Provides:  libmyth = %{version}-%{release}
Obsoletes: libmyth < %{version}-%{release}

Requires:  freetype >= 2
Requires:  lame
Requires:  qt4 >= 4.6
Requires:  qt4-MySQL

%description libs
Common library code for MythTV and add-on modules (development)
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

################################################################################

%package devel
Summary:   Development files for mythtv
Group:     Development/Libraries
Provides:  libmyth-devel = %{version}-%{release}
Obsoletes: libmyth-devel < %{version}-%{release}

Requires:  mythtv-libs = %{version}-%{release}

Requires:  freetype-devel >= 2
Requires:  mysql-devel >= 5
Requires:  qt4-devel >= 4.6
Requires:  lm_sensors-devel
Requires:  lirc-devel

# X, and Xv video support
Requires:  libXmu-devel
Requires:  libXv-devel
Requires:  libXvMC-devel
Requires:  libXxf86vm-devel
Requires:  mesa-libGLU-devel
Requires:  xorg-x11-proto-devel

# OpenGL video output and vsync support
Requires:  libGL-devel, libGLU-devel

# Misc A/V format support
%if %{with_faac}
Requires:  faac-devel
%endif
Requires:  fftw-devel >= 3
Requires:  flac-devel >= 1.0.4
Requires:  gsm-devel
Requires:  lame-devel
Requires:  libdca-devel
Requires:  libdvdnav-devel
Requires:  libdvdread-devel >= 0.9.4
Requires:  libfame-devel >= 0.9.0
Requires:  libogg-devel
Requires:  libtheora-devel
Requires:  libvorbis-devel >= 1.0
Requires:  mjpegtools-devel >= 1.6.1
Requires:  taglib-devel >= 1.5
Requires:  transcode >= 0.6.8
Requires:  x264-devel
Requires:  xvidcore-devel >= 0.9.1

# Audio framework support
Requires:  alsa-lib-devel
Requires:  jack-audio-connection-kit-devel
%if %{with_pulseaudio}
Requires:  pulseaudio-libs-devel
%endif

# Need dvb headers for dvb support
Requires:  kernel-headers

# FireWire cable box support
Requires:  libavc1394-devel
Requires:  libiec61883-devel
Requires:  libraw1394-devel

%if %{with_vdpau}
Requires: libvdpau-devel
%endif

%if %{with_vaapi}
Requires: libva-devel
%endif

%if %{with_crystalhd}
Requires: libcrystalhd-devel
%endif

%description devel
This package contains the header files and libraries for developing
add-ons for mythtv.

################################################################################

%package base-themes
Summary: Core user interface themes for mythtv
Group:   Applications/Multimedia

# Replace an old ATRMS package
Provides:   mythtv-theme-gant
Obsoletes:  mythtv-theme-gant

%description base-themes
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv-docs package for more information.

This package contains the base themes for the mythtv user interface.

################################################################################

%package frontend
Summary:   Client component of mythtv (a DVR)
Group:     Applications/Multimedia
Requires:  freetype, lame
Requires:  perl(XML::Simple)
Requires:  mythtv-common       = %{version}-%{release}
Requires:  mythtv-base-themes  = %{version}
Requires:  python-MythTV
Provides:  mythtv-frontend-api = %{mythfeapiver}
Obsoletes: mythvideo           < %{version}-%{release}
Provides:  mythvideo           = %{version}-%{release}

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
Group:      Applications/Multimedia
Requires:   lame
Requires:   mythtv-common = %{version}-%{release}
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
Group:     Applications/Multimedia
Requires:  freetype
Requires:  mythtv-backend = %{version}-%{release}
Requires:  mythtv-base-themes = %{version}

%description setup
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains only the setup software for configuring the
mythtv backend.

################################################################################

%package common
Summary: Common components needed by multiple other MythTV components
Group: Applications/Multimedia
# mythpmovies is now DOA, but we need this for upgrade path preservation.
Provides: mythmovies = %{version}-%{release}
Obsoletes: mythmovies < %{version}-%{release}

%description common
MythTV provides a unified graphical interface for recording and viewing
television programs.  Refer to the mythtv package for more information.

This package contains components needed by multiple other MythTV components.

################################################################################
################################################################################

%package -n mythffmpeg
Summary: MythTV build of FFmpeg
Group: Applications/Multimedia

%description -n mythffmpeg
Several MythTV utilities interact with FFmpeg, which changes its parameters
often enough to make it a hassle to support the variety of versions used by
MythTV users.  This is a snapshot of the FFmpeg code so that MythTV utilities
can interact with a known verion.

################################################################################

%if %{with_perl}

%package -n perl-MythTV
Summary:        Perl bindings for MythTV
Group:          Development/Languages
BuildArch:      noarch

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(DBD::mysql)
Requires:       perl(Net::UPnP)
Requires:       perl(Net::UPnP::ControlPoint)

%description -n perl-MythTV
Provides a perl-based interface to interacting with MythTV.

%endif

################################################################################

%if %{with_php}

%package -n php-MythTV
Summary:        PHP bindings for MythTV
Group:          Development/Languages
BuildArch:      noarch

%description -n php-MythTV
Provides a PHP-based interface to interacting with MythTV.

%endif

################################################################################

%if %{with_python}

%package -n python-MythTV
Summary:        Python bindings for MythTV
Group:          Development/Languages
BuildArch:      noarch

Requires:       MySQL-python
Requires:       PyXML
Requires:       python-lxml

%description -n python-MythTV
Provides a python-based interface to interacting with MythTV.

%endif

################################################################################

%if %{with_plugins}

# Meta package for all mythtv plugins
%package -n mythplugins

Summary:  Main MythTV plugins
Group:    Applications/Multimedia

Requires:  mythmusic      = %{version}-%{release}
Requires:  mythweather    = %{version}-%{release}
Requires:  mythgallery    = %{version}-%{release}
Requires:  mythgame       = %{version}-%{release}
Requires:  mythnews       = %{version}-%{release}
Requires:  mythbrowser    = %{version}-%{release}
Requires:  mytharchive    = %{version}-%{release}
Requires:  mythzoneminder = %{version}-%{release}
Requires:  mythnetvision  = %{version}-%{release}

%description -n mythplugins
This is a consolidation of all the official MythTV plugins that used to be
distributed as separate downloads from mythtv.org.

################################################################################
%if %{with_mytharchive}

%package -n mytharchive
Summary:   A module for MythTV for creating and burning DVDs
Group:     Applications/Multimedia

Requires:  mythtv-frontend-api = %{mythfeapiver}
Requires:  MySQL-python
Requires:  cdrecord >= 2.01
Requires:  dvd+rw-tools >= 5.21.4.10.8
Requires:  dvdauthor >= 0.6.11
Requires:  ffmpeg >= 0.4.9
Requires:  mjpegtools >= 1.6.2
Requires:  mkisofs >= 2.01
Requires:  python >= 2.3.5
Requires:  python-imaging
Requires:  transcode >= 1.0.2
Requires:  pmount

%description -n mytharchive
MythArchive is a new plugin for MythTV that lets you create DVDs from
your recorded shows, MythVideo files and any video files available on
your system.

%endif
################################################################################
%if %{with_mythbrowser}

%package -n mythbrowser
Summary:   A small web browser module for MythTV
Group:     Applications/Multimedia
Requires:  mythtv-frontend-api = %{mythfeapiver}

%description -n mythbrowser
MythBrowser is a full fledged web-browser (multiple tabs) to display
webpages in full-screen mode. Simple page navigation is possible.
Starting with version 0.13 it also has full support for mouse driven
navigation (right mouse opens and clos es the popup menu).

MythBrowser also contains a BookmarkManager to manage the website
links in a simple mythplugin.

%endif
################################################################################
%if %{with_mythgallery}

%package -n mythgallery
Summary:   A gallery/slideshow module for MythTV
Group:     Applications/Multimedia
Requires:  mythtv-frontend-api = %{mythfeapiver}

%description -n mythgallery
A gallery/slideshow module for MythTV.

%endif
################################################################################
%if %{with_mythgame}

%package -n mythgame
Summary:   A game frontend (xmame, nes, snes, pc) for MythTV
Group:     Applications/Multimedia
Requires:  mythtv-frontend-api = %{mythfeapiver}

%description -n mythgame
A game frontend (xmame, nes, snes, pc) for MythTV.

%endif
################################################################################
%if %{with_mythmusic}

%package -n mythmusic
Summary:   The music player add-on module for MythTV
Group:     Applications/Multimedia
Requires:  mythtv-frontend-api = %{mythfeapiver}

%description -n mythmusic
Music add-on for mythtv.

%endif
################################################################################
%if %{with_mythnews}

%package -n mythnews
Summary:   An RSS news feed plugin for MythTV
Group:     Applications/Multimedia
Requires:  mythtv-frontend-api = %{mythfeapiver}

%description -n mythnews
An RSS news feed reader plugin for MythTV.

%endif
################################################################################
%if %{with_mythweather}

%package -n mythweather
Summary:   A MythTV module that displays a weather forecast
Group:     Applications/Multimedia
Requires:  mythtv-frontend-api = %{mythfeapiver}
Requires:  perl(XML::SAX::Base)

%description -n mythweather
A MythTV module that displays a weather forecast.

%endif
################################################################################
%if %{with_mythzoneminder}

%package -n mythzoneminder
Summary:   A module for MythTV for camera security and surveillance
Group:     Applications/Multimedia
Requires:  mythtv-frontend-api = %{mythfeapiver}

%description -n mythzoneminder
MythZoneMinder is a plugin to interface to some of the features of
ZoneMinder. You can use it to view a status window similar to the
console window in ZM. Also there are screens to view live camera shots
and replay recorded events.

%endif
################################################################################
%if %{with_mythnetvision}

%package -n mythnetvision
Summary:   A MythTV module for Internet video on demand
Group:     Applications/Multimedia
Requires:  mythtv-frontend-api = %{mythfeapiver}
Requires:  mythbrowser = %{version}-%{release}
Requires:  python-MythTV = %{version}-%{release}
Requires:  python-pycurl
Requires:  python >= 2.5
Requires:  python-lxml
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
%setup -q -n MythTV-%{name}-%{githash2}

# Replace static lib paths with %{_lib} so we build properly on x86_64
# systems, where the libs are actually in lib64.
    if [ "%{_lib}" != "lib" ]; then
         find \( -name 'configure' -o -name '*pro' -o -name 'Makefile' \) -exec sed -r -i -e 's,/lib\b,/%{_lib},g' {} \+
    fi

%patch0 -p1 -b .mythtv

# Install ChangeLog
install -m 0644 %{SOURCE11} .

pushd mythtv

# Drop execute permissions on contrib bits, since they'll be %doc
    find contrib/ -type f -exec chmod -x "{}" \;
# And drop execute bit on theme html files
    chmod -x themes/default/htmls/*.html

# Nuke Windows and Mac OS X build scripts
    rm -rf contrib/Win32 contrib/OSX

# Put perl bits in the right place and set opt flags
    sed -i -e 's#perl Makefile.PL#%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"#' \
        bindings/perl/Makefile

# Install other source files
    cp -a %{SOURCE10} .
    cp -a %{SOURCE106} %{SOURCE107} %{SOURCE108} %{SOURCE109} .

# Make sure we use -O2 and not -O3
    sed -i '/speed_cflags=/d' configure

# Prevent all of those nasty installs to ../../../../../bin/whatever
#    echo "QMAKE_PROJECT_DEPTH = 0" >> mythtv.pro
#    echo "QMAKE_PROJECT_DEPTH = 0" >> settings.pro
#    chmod 644 settings.pro

popd



################################################################################

%build

# First, we build MythTV
pushd mythtv

# Similar to 'percent' configure, but without {_target_platform} and
# {_exec_prefix} etc... MythTV no longer accepts the parameters that the
# configure macro passes, so we do this manually.
./configure \
    --prefix=%{_prefix}                         \
    --libdir=%{_libdir}                         \
    --libdir-name=%{_lib}                       \
    --mandir=%{_mandir}                         \
    --enable-iptv                               \
    --enable-pthreads                           \
    --enable-ffmpeg-pthreads                    \
    --enable-joystick-menu                      \
    --enable-audio-alsa                         \
    --enable-audio-oss                          \
    --enable-audio-jack                         \
    --enable-libfftw3                           \
    --enable-x11 --x11-path=%{_includedir}      \
    --enable-xv                                 \
    --enable-opengl-video                       \
    --enable-xrandr                             \
    --enable-lirc                               \
    --enable-ivtv                               \
    --enable-firewire                           \
    --enable-dvb                                \
%if %{with_faac}
    --enable-libfaac --enable-nonfree           \
%endif
    --enable-libmp3lame                         \
    --enable-libx264                            \
    --enable-libtheora --enable-libvorbis       \
    --enable-libxvid                            \
%if %{with_vdpau}
    --enable-vdpau				\
%endif
%if %{with_vaapi}
    --enable-vaapi				\
%endif
%if %{with_crystalhd}
    --enable-crystalhd				\
%endif
%if !%{with_perl}
    --without-bindings=perl                     \
%endif
%if !%{with_php}
    --without-bindings=php                      \
%endif
%if !%{with_python}
    --without-bindings=python                   \
%endif
%ifarch ppc
    --extra-cflags="%{optflags} -maltivec -fomit-frame-pointer" \
    --extra-cxxflags="%{optflags} -maltivec -fomit-frame-pointer" \
%else
    --extra-cflags="%{optflags} -fomit-frame-pointer" \
    --extra-cxxflags="%{optflags} -fomit-frame-pointer" \
%endif
%ifarch %{ix86}
    --cpu=i686 --tune=i686 --enable-mmx \
%endif
%if %{with_proc_opt}
    --enable-proc-opt \
%endif
%if %{with_debug}
    --compile-type=debug                        \
%else
    --compile-type=release                      \
%endif
    --enable-debug

# Insert rpm version-release for mythbackend --version output
    echo 'SOURCE_VERSION="%{version}-%{release} (%_gitrev)"' > VERSION
    echo 'BRANCH="%{branch}"'                               >> VERSION

# Make
    make %{?_smp_mflags}

# Prepare to build the plugins
    popd
    mkdir fakeroot
    temp=`pwd`/fakeroot
    make -C mythtv install INSTALL_ROOT=$temp
    export LD_LIBRARY_PATH=$temp%{_libdir}:$LD_LIBRARY_PATH

# Next, we build the plugins
%if %{with_plugins}
pushd mythplugins

# Fix things up so they can find our "temp" install location for mythtv-libs
    echo "QMAKE_PROJECT_DEPTH = 0" >> settings.pro
    find . -name \*.pro \
        -exec sed -i -e "s,INCLUDEPATH += .\+/include/mythtv,INCLUDEPATH += $temp%{_includedir}/mythtv," {} \; \
        -exec sed -i -e "s,DEPLIBS = \$\${LIBDIR},DEPLIBS = $temp%{_libdir}," {} \; \
        -exec sed -i -e "s,\$\${PREFIX}/include/mythtv,$temp%{_includedir}/mythtv," {} \;
    echo "INCLUDEPATH -= \$\${PREFIX}/include" >> settings.pro
    echo "INCLUDEPATH -= \$\${SYSROOT}/\$\${PREFIX}/include" >> settings.pro
    echo "INCLUDEPATH -= %{_includedir}"       >> settings.pro
    echo "INCLUDEPATH += $temp%{_includedir}"  >> settings.pro
    echo "INCLUDEPATH += %{_includedir}"       >> settings.pro
    echo "LIBS *= -L$temp%{_libdir}"           >> settings.pro
    echo "QMAKE_LIBDIR += $temp%{_libdir}"     >> targetdep.pro

    ./configure \
        --prefix=${temp}%{_prefix} \
        --libdir=%{_libdir} \
        --libdir-name=%{_lib} \
    %if %{with_mytharchive}
        --enable-mytharchive \
    %else
        --disable-mytharchive \
    %endif
    %if %{with_mythbrowser}
        --enable-mythbrowser \
    %else
        --disable-mythbrowser \
    %endif
    %if %{with_mythgallery}
        --enable-mythgallery \
        --enable-exif \
        --enable-new-exif \
    %else
        --disable-mythgallery \
    %endif
    %if %{with_mythgame}
        --enable-mythgame \
    %else
        --disable-mythgame \
    %endif
    %if %{with_mythmusic}
        --enable-mythmusic \
    %else
        --disable-mythmusic \
    %endif
    %if %{with_mythnews}
        --enable-mythnews \
    %else
        --disable-mythnews \
    %endif
    %if %{with_mythweather}
        --enable-mythweather \
    %else
        --disable-mythweather \
    %endif
    %if %{with_mythzoneminder}
        --enable-mythzoneminder \
    %else
        --disable-mythzoneminder \
    %endif
    %if %{with_mythnetvision}
        --enable-mythnetvision \
    %else
        --disable-mythnetvision \
    %endif
        --enable-opengl \
        --enable-fftw \
#        --enable-sdl

    make %{?_smp_mflags}

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
    %if 0%{?fedora} >= 16
    mkdir -p %{buildroot}%{_unitdir}
    %else
    mkdir -p %{buildroot}%{_sysconfdir}/init.d
    mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
    %endif
    mkdir -p %{buildroot}%{_sysconfdir}/mythtv


# Fix permissions on executable python bindings
#    chmod +x %{buildroot}%{python_sitelib}/MythTV/Myth*.py

# config/init files
    echo "# to be filled in by mythtv-setup" > %{buildroot}%{_sysconfdir}/mythtv/config.xml

    ### SystemD based setup. ###
    %if 0%{?fedora} >= 16
    install -p -m 0644 %{SOURCE105} %{buildroot}%{_unitdir}/
    install -p -m 0644 %{SOURCE104} %{buildroot}%{_sysconfdir}/logrotate.d/mythtv
    # Install udev rules for devices that may initialize late in the boot
    # process so they are available for mythbackend.
    mkdir -p %{buildroot}/lib/udev/rules.d/
    install -p -m 0644 %{SOURCE111} %{buildroot}/lib/udev/rules.d/

    ### SysV based setup. ###
    %else
    install -p -m 0755 %{SOURCE102} %{buildroot}%{_sysconfdir}/init.d/mythbackend
    install -p -m 0644 %{SOURCE101} %{buildroot}%{_sysconfdir}/sysconfig/mythbackend
    install -p -m 0644 %{SOURCE103} %{buildroot}%{_sysconfdir}/logrotate.d/mythtv
    %endif

# Desktop entries
    mkdir -p %{buildroot}%{_datadir}/pixmaps
    mkdir -p %{buildroot}%{_datadir}/applications
    for file in %{desktop_applications}; do
      install -p $file.png %{buildroot}%{_datadir}/pixmaps/$file.png
      desktop-file-install --vendor %{desktop_vendor} \
        --dir %{buildroot}%{_datadir}/applications    \
        --add-category X-Fedora-Extra     \
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
%if %{with_plugins}
pushd mythplugins

    make install INSTALL_ROOT=%{buildroot}

%if %{with_mythmusic}
    mkdir -p %{buildroot}%{_localstatedir}/lib/mythmusic
%endif
%if %{with_mythgallery}
    mkdir -p %{buildroot}%{_localstatedir}/lib/pictures
%endif
%if %{with_mythgame}
    mkdir -p %{buildroot}%{_datadir}/mythtv/games/nes/{roms,screens}
    mkdir -p %{buildroot}%{_datadir}/mythtv/games/snes/{roms,screens}
#   mkdir -p %{buildroot}%{_datadir}/mythtv/games/mame/{roms,screens,flyers,cabs}
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


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%pre backend
# Add the "mythtv" user, with membership in the audio and video group
getent group mythtv >/dev/null || groupadd -r mythtv
getent passwd mythtv >/dev/null || \
    useradd -r -g mythtv -d %{_localstatedir}/lib/mythtv -s /sbin/nologin \
    -c "mythbackend user" mythtv
# Make sure the mythtv user is in the audio and video group for existing
# or new installs.
usermod -a -G audio,video mythtv
exit 0

%pre frontend
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

%post backend
%if 0%{?fedora} >= 16
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%else
/sbin/chkconfig --add mythbackend
%endif


%preun backend
%if 0%{?fedora} >= 16
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable mythbackend.service > /dev/null 2>&1 || :
    /bin/systemctl stop mythbackend.service > /dev/null 2>&1 || :
fi
%else
if [ $1 = 0 ]; then
    /sbin/service mythbackend stop > /dev/null 2>&1
    /sbin/chkconfig --del mythbackend
fi
%endif

%postun backend
%if 0%{?fedora} >= 16
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart mythbackend.service >/dev/null 2>&1 || :
fi
%else
if [ "$1" -ge "1" ] ; then
    /sbin/service mythbackend condrestart >/dev/null 2>&1 || :
fi
%endif

%if 0%{?fedora} >= 16
%triggerun -- mythtv < 0.24.1-3
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save mythbackend >/dev/null 2>&1 ||:

# If the package is allowed to autostart:
/bin/systemctl --no-reload enable mythbackend.service >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del mythbackend >/dev/null 2>&1 || :
/bin/systemctl try-restart mythbackend.service >/dev/null 2>&1 || :
%endif

################################################################################

%files
%doc ChangeLog mythtv/PACKAGE-LICENSING

%files docs
%doc mythtv/README*
%doc mythtv/UPGRADING
%doc mythtv/AUTHORS
%doc mythtv/COPYING
%doc mythtv/FAQ
%doc mythtv/database mythtv/keys.txt
# Do we really need the API documentation?
#%doc mythtv/docs/*.html mythtv/docs/*.png
#%doc mythtv/docs/*.txt
%doc mythtv/contrib

%files common
%dir %{_datadir}/mythtv
%{_bindir}/mythccextractor
%{_bindir}/mythcommflag
%{_bindir}/mythmetadatalookup
%{_bindir}/mythutil
%{_bindir}/mythlogserver
%{_bindir}/mythpreviewgen
%{_bindir}/mythtranscode
%{_bindir}/mythwikiscripts
%{_datadir}/mythtv/mythconverg*.pl
%{_datadir}/mythtv/locales/
%{_datadir}/mythtv/metadata/
%{_datadir}/mythtv/hardwareprofile/
%attr(-,mythtv,mythtv)
%dir %{_sysconfdir}/mythtv
%config(noreplace) %{_sysconfdir}/mythtv/config.xml

%files backend
%{_bindir}/mythbackend
%{_bindir}/mythfilldatabase
%{_bindir}/mythjobqueue
%{_bindir}/mythmediaserver
%{_bindir}/mythreplex
%{_datadir}/mythtv/MXML_scpd.xml
%{_datadir}/mythtv/backend-config/
%attr(-,mythtv,mythtv) %dir %{_localstatedir}/lib/mythtv
%attr(-,mythtv,mythtv) %dir %{_localstatedir}/cache/mythtv
%if 0%{?fedora} >=16
%{_unitdir}/mythbackend.service
/lib/udev/rules.d/99-mythbackend.rules
%else
%{_sysconfdir}/init.d/mythbackend
%config(noreplace) %{_sysconfdir}/sysconfig/mythbackend
%endif
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
#%%{_bindir}/mythmessage
%{_bindir}/mythlcdserver
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
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%exclude %{_libdir}/*.a
%dir %{_datadir}/mythtv/build
%{_datadir}/mythtv/build/settings.pro

%files -n mythffmpeg
%{_bindir}/mythffmpeg

%if %{with_perl}
%files -n perl-MythTV
%{perl_vendorlib}/MythTV.pm
%dir %{perl_vendorlib}/MythTV
%{perl_vendorlib}/MythTV/*.pm
%dir %{perl_vendorlib}/IO/Socket
%dir %{perl_vendorlib}/IO/Socket/INET
%{perl_vendorlib}/IO/Socket/INET/MythTV.pm
%exclude %{perl_vendorarch}/auto/MythTV/.packlist
%endif

%if %{with_php}
%files -n php-MythTV
%{_datadir}/mythtv/bindings/php/*
%endif

%if %{with_python}
%files -n python-MythTV
%{_bindir}/mythpython
%{python_sitelib}/MythTV/
%{python_sitelib}/MythTV-*.egg-info
%endif

%if %{with_plugins}
%files -n mythplugins
%doc mythplugins/COPYING

%if %{with_mytharchive}
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

%if %{with_mythbrowser}
%files -n mythbrowser
%doc mythplugins/mythbrowser/AUTHORS
%doc mythplugins/mythbrowser/COPYING
%doc mythplugins/mythbrowser/README
%{_libdir}/mythtv/plugins/libmythbrowser.so
%{_datadir}/mythtv/i18n/mythbrowser_*.qm
%endif

%if %{with_mythgallery}
%files -n mythgallery
%doc mythplugins/mythgallery/AUTHORS
%doc mythplugins/mythgallery/COPYING
%doc mythplugins/mythgallery/README
%{_libdir}/mythtv/plugins/libmythgallery.so
%{_datadir}/mythtv/i18n/mythgallery_*.qm
%attr(0775,mythtv,mythtv) %{_localstatedir}/lib/pictures
%endif

%if %{with_mythgame}
%files -n mythgame
%dir %{_sysconfdir}/mythgame
%config(noreplace) %{_sysconfdir}/mythgame/gamelist.xml
%{_libdir}/mythtv/plugins/libmythgame.so
%dir %{_datadir}/mythtv/games
%{_datadir}/mythtv/games/*
%dir %{_datadir}/mame/screens
%dir %{_datadir}/mame/flyers
%{_datadir}/mythtv/game_settings.xml
%{_datadir}/mythtv/i18n/mythgame_*.qm
%endif

%if %{with_mythmusic}
%files -n mythmusic
%doc mythplugins/mythmusic/AUTHORS
%doc mythplugins/mythmusic/COPYING
%doc mythplugins/mythmusic/README
%{_libdir}/mythtv/plugins/libmythmusic.so
%attr(0775,mythtv,mythtv) %{_localstatedir}/lib/mythmusic
%{_datadir}/mythtv/mythmusic/
%{_datadir}/mythtv/musicmenu.xml
%{_datadir}/mythtv/music_settings.xml
%{_datadir}/mythtv/i18n/mythmusic_*.qm
%endif

%if %{with_mythnews}
%files -n mythnews
%doc mythplugins/mythnews/AUTHORS
%doc mythplugins/mythnews/COPYING
%doc mythplugins/mythnews/README
%{_libdir}/mythtv/plugins/libmythnews.so
%{_datadir}/mythtv/mythnews
%{_datadir}/mythtv/i18n/mythnews_*.qm
%endif

%if %{with_mythweather}
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

%if %{with_mythzoneminder}
%files -n mythzoneminder
%{_libdir}/mythtv/plugins/libmythzoneminder.so
%{_datadir}/mythtv/zonemindermenu.xml
%{_bindir}/mythzmserver
%{_datadir}/mythtv/i18n/mythzoneminder_*.qm
%endif

%if %{with_mythnetvision}
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

* Fri Mar 03 2012 Richard Shaw <hobbes1069@gmail.com> - 0.24.2-2
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

* Sun Oct 20 2011 Richard Shaw <hobbes1069@gmail.com> - 0.24.1-3
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
