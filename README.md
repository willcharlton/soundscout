# Setup instructions for running PyDejaVu on raspberry pi

It is strongly suggested that you make a virtual environment while this project is in development.

Currently this project is only being developed for python 3.4.3.

```
pip install virtualenvwrapper
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc # make sure you have the helper scripts every time you start a new bash terminal
source ~/.bashrc

cd /tmp
wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
tar zxvf Python-3.4.3
cd Python-3.4.3
./configure --prefix /usr # already where other python versions are located on pi
make
make test
sudo make install


# scipy needs these
sudo apt-get install gfortran liblapack-dev


# TODO: DON"T KNOW ABOUT THIS COMMENT: you're going to use cmake for this project in its current state
sudo apt-get install cmake

# scipy needs openblas
# installation instructions for ubuntu - https://hunseblog.wordpress.com/2014/09/15/installing-numpy-and-openblas/
# tested on Ubuntu machine and proven ~Will
git clone https://github.com/xianyi/OpenBLAS
cd OpenBLAS
make FC=gfortran
sudo make PREFIX=/opt/openblas install
# this might require `sudo` or and `sudo vi /etc/ld.so.conf.d/openblas.conf`
echo "/opt/openblas/lib" > /etc/ld.so.conf.d/openblas.conf
sudo ldconfig

# get portaudio
# http://portaudio.com/docs/v19-doxydocs/compile_linux.html
sudo apt-get install libasound-dev # tested on piB+

# get PyAudio
sudo apt-get install python-pyaudio # tested on piB+

# get matplotlib
git clone --depth 1 git://github.com/matplotlib/matplotlib.git
cd matplotlib
python setup.py install

# found I had to upgrade my version of `distribute` before installing dejavu
easy_install -U distribute

# get PyDejavu
pip install https://github.com/worldveil/dejavu/zipball/master
