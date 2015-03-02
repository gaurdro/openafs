#!/bin/bash

if [[ -x /usr/bin/rpm ]] && /usr/bin/rpm --quiet -q kernel-headers; then
        exec /usr/bin/rpm -q --qf '%%define kversion %{version}-%{release}\n' kernel-headers
else

KVERSIONSTR=$(grep LINUX_VERSION_CODE /usr/include/linux/version.h)
KVERSIONNO=${KVERSIONSTR##* }
KVERSION1=$(( $KVERSIONNO >> 16 ))
KVERSION1R=$(( $KVERSIONNO - ( $KVERSION1 << 16 ) ))
KVERSION2=$(( $KVERSION1R >> 8 ))
KVERSION3=$(( $KVERSION1R - ( $KVERSION2 << 8 ) ))

RVERSION=$(grep 'RHEL_RELEASE ' /usr/include/linux/version.h | cut -d'"' -f2)
RHELMAJORSTR=$(grep RHEL_MAJOR /usr/include/linux/version.h)
RHELMAJOR=${RHELMAJORSTR##* }

printf "%%define kversion %d.%d.%d-%s.el%d\n" $KVERSION1 $KVERSION2 $KVERSION3 $RVERSION $RHELMAJOR

fi
