#!/bin/sh

tar xzf zfs.tgz
rpm -ivh zfs/spl/*.rpm
rpm -ivh zfs/zfs/*.rpm
reboot



