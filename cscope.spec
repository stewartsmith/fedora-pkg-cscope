Summary: C source code tree search and browse tool 
Name: cscope
Version: 15.5
Release: 6 
Source0: http://unc.dl.sourceforge.net/sourceforge/cscope/cscope-15.5.tar.gz 
URL: http://cscope.sourceforge.net
License: BSD 
Group: Development/Tools 
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildRequires: pkgconfig ncurses-devel flex bison m4

%define cscope_share_path %{_datadir}/cscope
%define xemacs_lisp_path %{_datadir}/xemacs/site-packages/lisp
%define emacs_lisp_path %{_datadir}/emacs/site-lisp

Patch0:cscope-15.5-ocs.patch
Patch1:cscope-15.5-findassign.patch
Patch2:cscope-15.5-ocs-dash_s_fix.patch
Patch3:cscope-15.5-xcscope-man.patch
Patch4:cscope-15.5-inverted.patch
Patch5:cscope-15.5-resize.patch

%description
cscope is a mature, ncurses based, C source code tree browsing tool.  It 
allows users to search large source code bases for variables, functions,
macros, etc, as well as perform general regex and plain text searches.  
Results are returned in lists, from which the user can select individual 
matches for use in file editing.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT %{name}-%{version}.files
make DESTDIR=$RPM_BUILD_ROOT install 
mkdir -p $RPM_BUILD_ROOT/var/lib/cs
mkdir -p $RPM_BUILD_ROOT%{cscope_share_path}
cp -a contrib/xcscope/xcscope.el $RPM_BUILD_ROOT%{cscope_share_path}
cp -a contrib/xcscope/cscope-indexer $RPM_BUILD_ROOT%{_bindir}
for dir in %{xemacs_lisp_path} %{emacs_lisp_path} ; do
  mkdir -p $RPM_BUILD_ROOT$dir
  ln -s %{cscope_share_path}/xcscope.el $RPM_BUILD_ROOT$dir
  touch $RPM_BUILD_ROOT$dir/xcscope.elc
  echo "%ghost $dir/xcscope.el*" >> %{name}-%{version}.files
done


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}-%{version}.files
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{cscope_share_path}
%{cscope_share_path}/xcscope.el
%{_mandir}/man1/*
%dir /var/lib/cs
%doc AUTHORS COPYING ChangeLog README TODO

%triggerin -- xemacs
ln -sf %{cscope_share_path}/xcscope.el %{xemacs_lisp_path}/xcscope.el

%triggerin -- emacs
ln -sf %{cscope_share_path}/xcscope.el %{emacs_lisp_path}/xcscope.el

%triggerun -- xemacs
[ $2 -gt 0 ] && exit 0
rm -f %{xemacs_lisp_path}/xcscope.el

%triggerun -- emacs
[ $2 -gt 0 ] && exit 0
rm -f %{emacs_lisp_path}/xcscope.el

%changelog
* Mon Nov 22 2004 Neil Horman <nhorman@redhat.com>
- added cscope-1.5.-resize patch to allow terminal
  resizing while cscope is running

* Tue Oct 5  2004 Neil Horman <nhorman@redhat.com>
- modified cscope-15.5.-inverted patch to be upstream
  friendly

* Tue Sep 28 2004 Neil Horman <nhorman@redhat.com>
- fixed inverted index bug (bz 133942)
 
* Mon Sep 13 2004 Frank Ch. Eigler <fche@redhat.com>
- bumped release number to a plain "1"

* Fri Jul 16 2004 Neil Horman <nhorman@redhat.com>
- Added cscope-indexer helper and xcscope lisp addon
- Added man page for xcscope
- Added triggers to add xcscope.el pkg to (x)emacs
- Thanks to Ville, Michael and Jens for thier help :)

* Fri Jul 2 2004 Neil Horman <nhorman@redhat.com>
- Added upstream ocs fix
- Added feature to find symbol assignments
- Changed default SYSDIR directory to /var/lib/cs
- Incoproated M. Schwendt's fix for ocs -s 

* Fri Jun 18 2004 Neil Horman <nhorman@redhat.com>
- built the package
