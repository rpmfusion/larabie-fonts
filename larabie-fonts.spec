%define decodir     %{_datadir}/fonts/%{name}-deco
%define straightdir %{_datadir}/fonts/%{name}-straight
%define uncommondir %{_datadir}/fonts/%{name}-uncommon
%define catalogue   %{_sysconfdir}/X11/fontpath.d

Summary:       A Collection of High Quality TrueType Fonts
Name:          larabie-fonts
Version:       0
Release:       0.2.20011216%{?dist}
License:       Larabie Fonts License
Group:         User Interface/X
URL:           http://www.larabiefonts.com/
# Although all the fonts in this tarball can be downloaded
# one-by-one from the above website, the website does not
# offer a collective file of fonts. This tarball provides a 
# good collection and is borrowed from Ubuntu:
# File downloaded from:
# https://launchpad.net/ubuntu/jaunty/+source/ttf-larabie/1:20011216-1.1
Source0:       ttf-larabie_20011216.orig.tar.gz
# This file sorts the fonts into families. Extracted from the build
# scripts of Ubuntu (same location as above):
Source1:       %{name}.sort
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
BuildRequires: xorg-x11-font-utils


%description
Larabie Fonts offer hundreds of free fonts for personal and 
commercial use in TrueType format. This is a meta-package 
to install "decorative", "straight", "uncommon" TrueType
font collections, created by Ray Larabie.

%package deco
Summary:       Larabie TrueType Decorative Fonts
Group:         User Interface/X

%description deco
Decorative freeware TrueType fonts from Ray Larabie. 
This package contains the "decorative" ones of his fonts,
which are great for headlines and other decorations.

%package straight
Summary:       Larabie TrueType Straight Fonts
Group:         User Interface/X

%description straight
Useful freeware TrueType fonts from Ray Larabie. This 
package contains the "straight"er ones of his fonts,
which are suitable for everyday use. 

%package uncommon
Summary:       Larabie TrueType Uncommon Fonts
Group:         User Interface/X

%description uncommon
Less common freeware TrueType fonts from Ray Larabie. 
This package contains fonts which are beautiful for 
special decorations and headlines.


%prep
%setup -q -n ttf-larabie-20011216
#patch0 -p1

SORTFILE=%{SOURCE1}
groups=`cut -f2 $SORTFILE | sort -u`
basedir=`pwd`

#
# Create Directories for fonts
#
for group in $groups; do
        if [ ! -d $group ]; then
                mkdir $group
        fi
done

#
# Extract font .zip files
#
for nam in *.zip; do
        group=`grep "^$nam[[:space:]]" $SORTFILE | cut -f2`
        if [ -z $group ]; then
                echo Font $nam is unsorted.
        else
                unzip -j -L -u -qq $nam -d $group -x read_me.txt
        fi
done

#
# Rename some problematic files
#
mv deco/let*seat.ttf deco/let_seat.ttf
mv uncommon/chr*32*.ttf uncommon/chr32.ttf

#
# Fix permission and EOL encoding issues.
#
for txtfile in straight/*.txt uncommon/*.txt; do
  sed 's/\r//' "$txtfile" > tmpfile
  touch -r "$txtfile" tmpfile
  mv -f tmpfile "$txtfile"
done


%build
echo "Nothing to build."


%install
rm -rf %{buildroot}
# fonts
install -m 0755 -d              %{buildroot}%{decodir}
install -m 0755 -d              %{buildroot}%{straightdir}
install -m 0755 -d              %{buildroot}%{uncommondir}
install -pm 0644 deco/*.ttf     %{buildroot}%{decodir}
install -pm 0644 straight/*.ttf %{buildroot}%{straightdir}
install -pm 0644 uncommon/*.ttf %{buildroot}%{uncommondir}

# catalogue
install -m 0755 -d             %{buildroot}%{catalogue}
ln -sf ../../../%{decodir}     %{buildroot}%{catalogue}
ln -sf ../../../%{straightdir} %{buildroot}%{catalogue}
ln -sf ../../../%{uncommondir} %{buildroot}%{catalogue}

# generate fonts.dir and fonts.scale
mkfontdir   %{buildroot}%{decodir}
mkfontscale %{buildroot}%{decodir}
mkfontdir   %{buildroot}%{straightdir}
mkfontscale %{buildroot}%{straightdir}
mkfontdir   %{buildroot}%{uncommondir}
mkfontscale %{buildroot}%{uncommondir}


%clean
rm -rf %{buildroot}


%post deco
if [ -x /usr/bin/fc-cache ]; then
  %{_bindir}/fc-cache %{_datadir}/fonts || :
fi

%postun deco
if [ "$1" = "0" ]; then
  if [ -x /usr/bin/fc-cache ]; then
    %{_bindir}/fc-cache %{_datadir}/fonts || :
  fi
fi

%post straight
if [ -x /usr/bin/fc-cache ]; then
  %{_bindir}/fc-cache %{_datadir}/fonts || :
fi

%postun straight
if [ "$1" = "0" ]; then
  if [ -x /usr/bin/fc-cache ]; then
    %{_bindir}/fc-cache %{_datadir}/fonts || :
  fi
fi

%post uncommon
if [ -x /usr/bin/fc-cache ]; then
  %{_bindir}/fc-cache %{_datadir}/fonts || :
fi

%postun uncommon
if [ "$1" = "0" ]; then
  if [ -x /usr/bin/fc-cache ]; then
    %{_bindir}/fc-cache %{_datadir}/fonts || :
  fi
fi


%files deco
%defattr(-,root,root,-)
%doc READ_ME.TXT
%{decodir}
%{catalogue}/%{name}-deco

%files straight
%defattr(-,root,root,-)
%doc READ_ME.TXT straight/*.txt
%{straightdir}
%{catalogue}/%{name}-straight

%files uncommon
%defattr(-,root,root,-)
%doc READ_ME.TXT uncommon/*.txt
%{uncommondir}
%{catalogue}/%{name}-uncommon

%changelog
* Sun Nov 30 2008 Orcan Ogetbil <orcanbahri [AT] yahoo [DOT] com> - 0-0.2.20011216
- Added the source download location as a comment.
- Preserve timestamps for the fonts.
- Removed the meta-package.
- Extracted the relevant parts from the Ubuntu's build script

* Mon Nov 24 2008 Orcan Ogetbil <orcanbahri [AT] yahoo [DOT] com> - 0-0.1.20011216
- Initial release.
