#!/bin/bash
sudo apt-get update
sudo apt-get install build-essential
sudo apt-get install git
git clone git://github.com/mongodb/mongo-python-driver.git pymongo
cd pymongo/
sudo python3 setup.py install
sudo apt-get install python3-setuptools
sudo easy_install3 pip
cd ..
mkdir zlib
cd zlib/
wget http://zlib.net/zlib-1.2.8.tar.gz
tar xfv zlib-1.2.8.tar.gz 
cd zlib-1.2.8/
./configure 
make
sudo make install
sudo pip3 install beautifulsoup4
sudo pip3 install lxml
cd ~
git clone https://github.com/mysql/mysql-connector-python.git
cd mysql-connector-python
