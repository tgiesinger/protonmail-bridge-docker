#!/bin/bash
set -ex

# Repack deb (remove unnecessary dependencies)
mkdir deb
wget -i /PACKAGE -O /deb/protonmail.deb
cd deb
ar x -v protonmail.deb
mkdir control
tar zxvf control.tar.gz -C control
# Drop only the GUI dependencies and keep the rest of the official list, so
# new runtime libraries added upstream (e.g. libfido2-1) are still installed.
GUI_DEPS="libxcb-cursor0|libegl1|libopengl0|libgl1|libpulse-mainloop-glib0|fonts-dejavu"
DEPS=$(sed -n 's/^Depends: //p' control/control | tr ',' '\n' | sed 's/^ *//' | grep -Ev "^(${GUI_DEPS})( |$)" | paste -sd, - | sed 's/,/, /g')
sed -i "s/^Depends: .*$/Depends: ${DEPS}/" control/control
grep "^Depends:" control/control
cd control
tar zcvf ../control.tar.gz .
cd ../

ar rcs -v /protonmail.deb debian-binary control.tar.gz data.tar.gz
