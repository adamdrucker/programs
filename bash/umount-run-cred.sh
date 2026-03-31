#!/bin/bash

# for some dumb reason, Fedora 41 does not clean up these /run/credentials
# directories and mount points for systemd services. it clutters up my
# duf report. this should umount anything, then remove the directories.

RUNDIR=/run/credentials

for i in $(ls $RUNDIR); do sudo umount $RUNDIR/$i; done

if [ $? -eq 0 ]; then
sudo rmdir $RUNDIR/*
fi

