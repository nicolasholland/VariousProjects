# basic stuff
sudo apt update
sudo apt install git curl vim

# conda stuff
INSTALL=Miniconda3-py39_4.9.2-Linux-x86_64.sh
PY39=https://repo.anaconda.com/miniconda/${INSTALL}
curl ${PY39}
sh ${INSTALL}
. ~/.bashrc

# chinese stuff
sudo apt-get install ibus-pinyin
ibus restart

# my stuff
git clone https://github.com/nicolasholland/VariousProjects

