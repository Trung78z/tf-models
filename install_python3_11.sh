#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

sudo apt-get update
sudo apt-get install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev libbz2-dev

wget -qO- https://www.python.org/ftp/python/3.11.11/Python-3.11.11.tar.xz | tar -xJ

cd Python-3.11.11
./configure --enable-optimizations

make -j$(nproc)

sudo make altinstall