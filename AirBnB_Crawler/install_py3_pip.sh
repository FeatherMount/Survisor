sudo yum groupinstall 'Development Tools'
wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz
tar zxvf Python-3.4.2.tgz
cd Python-3.4.2
sudo yum install gcc
./configure --prefix=/opt/python3
make
sudo yum install openssl-devel
sudo make install
sudo ln -s /opt/python3/bin/python3 /usr/bin/python3
git clone https://github.com/mysql/mysql-connector-python.git
cd mysql-connector-python
sudo python3 setup.py install