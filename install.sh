#!/bin/bash
mkdir /etc/assisht
cp assisht.py /usr/local/bin
chmod +x /usr/local/bin/assisht.py
echo 'assisht: config files ready'
echo 'assisht: using pip to install requirements...'
pip install -r requirements.txt
