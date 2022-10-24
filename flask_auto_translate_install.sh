whoami=`whoami`

# Remove because aws ec2 always root, but root is not good
#if [ $(id -u) -eq 0 ]; then
#  echo "Please not run as root"
#  exit
#fi

# apt
sudo apt update

# required PPA
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10 -y

sudo apt -y install python3-pip
sudo pip3 install --upgrade pip

sudo pip3 install virtualenv

# deb
version=$(cat version)
sed -i "s/__version__.*/__version__ = \"$version\"/" Flask_Auto_Translate/__init__.py

python3 setup.py bdist_wheel
rm dist/Flask_Auto_Translate/*.whl
mv dist/Flask_Auto_Translate*.whl dist/Flask_Auto_Translate/
sudo mv requirements.txt dist/Flask_Auto_Translate
sudo mv dist/ /opt/
sudo mv flask_auto_translate.service /etc/systemd/system/

virtualenv --python=python3.10 /opt/Flask_Auto_Translate/venv
/opt/Flask_Auto_Translate/venv/bin/pip3 install --force-reinstall /opt/Flask_Auto_Translate/Flask_Auto_Translate*
/opt/Flask_Auto_Translate/venv/bin/pip3 install -r /opt/Flask_Auto_Translate/requirements.txt

vim /opt/Flask_Auto_Translate/flask_auto_translate_config.ini
cd /opt/Flask_Auto_Translate
export FLASK_APP=Flask_Auto_Translate.app

# service
sudo sed -i "s/User=.*/User=$whoami/" /etc/systemd/system/flask_auto_translate.service
sudo systemctl daemon-reload
sudo systemctl enable flask_auto_translate.service
sudo systemctl restart flask_auto_translate.service
echo 'Flask Auto Translate server installation finished'
