# RPM packaged LibreOffice Online

## Current Status
* Builds correctly on Fedora and CentOS
* Tests disabled, they seem to require privileges outside of what rpmbuild grants
* Works 95% of the time (the other 5% is the "unexpected connection error")
* Some internals are unlabeled/missing (LoKit version, some js includes)

## General Information
The [LibreOffice Online](https://github.com/LibreOffice/online) repository is meant to be built by hand, I guess due to it's complicated nature, I have hacked it a bit in order to package it as an rpm and moved around some files so it fits in with what CentOS/Fedora generally expect.

## Requirements
* CentOS (tested on 7) / Fedora (tested on 23)
* libcmis (included)
* libe-book (included)
* libpagemaker (included)
* libwps (included)
* poco (included)
* libreoffice (included)

## Changes from original repo
* Werror for shadow has been disabled, breaks the build
* When building loleaflet, npm goes online, updates and rebuilds the shrinkpack
* loleaflet move to /usr/share/loolwsd/file_root
* jails moved to /usr/share/loolwsd/jails
* systemplate moved to /usr/share/loolwsd/systemplate
* all options in unit file removed (forces read from /etc/loolwsd/loolwsd.xml)
* Pointers changed for LibreOffice 5.2 at /usr/lib64
* Pointers changed for Poco at /usr/lib64

## Help!
Pulls are not only welcome, they're encouraged. Please give a hand to get this working 100% of the time!
