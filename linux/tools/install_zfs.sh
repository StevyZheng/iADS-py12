#!/usr/bin/env bash

tar xzf spl-0.6.5.6.tar.gz
tar xzf zfs-0.6.5.6.tar.gz
cd spl-0.6.5.6
./configure
make -j20 && make install
cd ../zfs-0.6.5.6
./configure
make -j20 && make install
modprobe zfs

