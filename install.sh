# Script to install honeypots module provided by python. Can also be done using pip3 install honeypots

git clone https://github.com/qeeqbox/honeypots
cd honeypots
cp -r honeypots /usr/local/lib/python3.8/dist-packages
cd ../
rm -rf honeypots