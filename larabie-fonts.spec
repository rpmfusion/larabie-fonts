%define fontname larabie

%define common_desc \
Larabie Fonts offer hundreds of free fonts for personal and commercial use in\
TrueType format. They consist of three collections: "decorative", "straight",\
"uncommon" fonts, created by Ray Larabie.

Summary:       A Collection of High Quality TrueType Fonts
Name:          %{fontname}-fonts
Version:       0
Release:       0.3.20011216%{?dist}
License:       Larabie Fonts License
Group:         User Interface/X
URL:           http://www.larabiefonts.com/
# Although all the fonts in this tarball can be downloaded
# one-by-one from the above website, the website does not
# offer a collective file of fonts. This tarball provides a 
# good collection and is borrowed from Ubuntu:
# File downloaded from:
# https://launchpad.net/ubuntu/jaunty/+source/ttf-larabie/1:20011216-1.1
Source0:       ttf-%{fontname}_20011216.orig.tar.gz
# This file sorts the fonts into families. Extracted from the build
# scripts of Ubuntu (same location as above):
Source1:       %{name}.sort
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
BuildRequires: fontpackages-devel

%description
%common_desc

%package common
Summary:       Common files for %{name}
Group:         User Interface/X
Requires:      fontpackages-filesystem

%description common
%common_desc

This package consists of files used by other %{name} packages.

%package -n %{fontname}-decorative-fonts
Summary:       Larabie TrueType Decorative Fonts
Group:         User Interface/X
Requires:      %{name}-common = %{version}-%{release}
Obsoletes:     %{fontname}-fonts-deco < 0-0.3.20011216
Provides:      %{fontname}-fonts-deco = 0-0.3.20011216

%description -n %{fontname}-decorative-fonts
%common_desc

This package contains the "decorative" ones of his fonts, which are great for 
headlines and other decorations.

%package -n %{fontname}-straight-fonts
Summary:       Larabie TrueType Straight Fonts
Group:         User Interface/X
Requires:      %{name}-common = %{version}-%{release}
Obsoletes:     %{fontname}-fonts-straight < 0-0.3.20011216
Provides:      %{fontname}-fonts-straight = 0-0.3.20011216

%description -n %{fontname}-straight-fonts
%common_desc

This package contains the "straight"er ones of his fonts, which are suitable 
for everyday use. 

%package -n %{fontname}-uncommon-fonts
Summary:       Larabie TrueType Uncommon Fonts
Group:         User Interface/X
Requires:      %{name}-common = %{version}-%{release}
Obsoletes:     %{fontname}-fonts-uncommon < 0-0.3.20011216
Provides:      %{fontname}-fonts-uncommon = 0-0.3.20011216

%description -n %{fontname}-uncommon-fonts
%common_desc

This package contains less common fonts which are beautiful for special 
decorations and headlines.


%prep
%setup -q -n ttf-%{fontname}-20011216

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
install -m 0755 -d              %{buildroot}%{_fontdir}/decorative
install -m 0755 -d              %{buildroot}%{_fontdir}/straight
install -m 0755 -d              %{buildroot}%{_fontdir}/uncommon
install -pm 0644 deco/*.ttf     %{buildroot}%{_fontdir}/decorative
install -pm 0644 straight/*.ttf %{buildroot}%{_fontdir}/straight
install -pm 0644 uncommon/*.ttf %{buildroot}%{_fontdir}/uncommon

%clean
rm -rf %{buildroot}

%files common
%defattr(-,root,root,-)
%doc READ_ME.TXT
%dir %{_fontdir}


%_font_pkg -n decorative decorative/*.ttf
%dir %{_fontdir}/decorative

%_font_pkg -n straight straight/*.ttf
%doc straight/*.txt
%dir %{_fontdir}/straight

%_font_pkg -n uncommon uncommon/*.ttf
%doc uncommon/*.txt
%dir %{_fontdir}/uncommon

%changelog
* Wed Jan 21 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0-0.3.20011216
- Update package to meet new font packaging and naming guidelines

* Sun Nov 30 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0-0.2.20011216
- Added the source download location as a comment.
- Preserve timestamps for the fonts.
- Removed the meta-package.
- Extracted the relevant parts from the Ubuntu's build script

* Mon Nov 24 2008 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0-0.1.20011216
- Initial release.